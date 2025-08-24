from dataclasses import dataclass
import functools
from datetime import timedelta
from uuid import uuid4


class TimeOverfill(RuntimeError):
    pass


@functools.total_ordering
class Definition:
    def __init__(self, id, duration, engagement):
        self.id = id
        self.duration = timedelta(seconds=duration)
        self.engagement = engagement if engagement != 0.0 else None
        self.dependeds = []

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return "[id={}:duration={}:engagement={}]".format(
            self.id, self.duration, self.engagement
        )

    def __eq__(self, other):
        if not hasattr(other, "id"):
            return False
        if not other.id:
            return False
        return self.id == other.id


def _dependeds_from_many(definition):
    if not definition.dependeds:
        return []
    return definition.dependeds


def _define(definition):
    if not definition:
        return None
    if not hasattr(definition, "dependeds"):
        definition.dependeds = []
    if hasattr(definition, "engagement") and (
        definition.engagement != 0.0 and definition.engagement is not None
    ):
        return _Duty(
            str(definition.id),
            float(definition.duration.seconds),
            engagement=(
                (float(definition.engagement) / 100.0)
                if isinstance(definition.engagement, int)
                else definition.engagement
            ),
            dependeds=[_define(one) for one in _dependeds_from_many(definition)],
        )
    else:
        return _Task(
            str(definition.id),
            float(definition.duration.seconds),
            engagement=1.0,
            dependeds=[_define(one) for one in _dependeds_from_many(definition)],
        )


def _dependencies_from_defineds(defineds):
    dependencies = {}
    for definition in defineds:
        for depended in definition.dependeds:
            if depended not in dependencies:
                dependencies[depended] = set()
            dependencies[depended].add(definition)
    return dependencies


@functools.total_ordering
class _Chunk:
    def __init__(self, id, duration, **kwargs):
        self.id = id
        self.duration = duration
        self.container = kwargs["container"] if "container" in kwargs else None
        self.dependeds = kwargs["dependeds"] if "dependeds" in kwargs else None
        self.engagement = kwargs["engagement"] if "engagement" in kwargs else 1.0

    @property
    def weight(self):
        return self.duration * self.engagement

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not other:
            return False
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    @property
    def insignificant(self):
        return self.duration < 0.01

    def split(self, duration):
        task2 = type(self)(
            self.id,
            self.duration - duration,
            engagement=self.engagement,
            dependeds=self.dependeds,
        )
        task1 = type(self)(
            self.id,
            duration,
            after=task2,
            engagement=self.engagement,
            dependeds=self.dependeds,
        )
        return (task1, task2)

    def __repr__(self):
        return "Chunk-id={}:duration={}:engagement={}".format(
            self.id, self.duration, self.engagement
        )


class _Task(_Chunk):

    def change_engagement(self, engagement):
        return _Task(
            self.id,
            self.weight / (engagement if engagement >= 0.01 else 0.01),
            dependeds=self.dependeds,
            engagement=engagement,
        )

    def scale_duration(self, duration):
        return self.change_engagement(self.weight / duration)

    def merge(self, *tasks):
        duration = (
            sum([task.change_engagement(1.0).duration for task in tasks])
            + self.change_engagement(1.0).duration
        )
        return _Task(self.id, duration, dependeds=self.dependeds, engagement=1.0)


class _Duty(_Chunk):
    pass


class _TaskPlacer:
    def __call__(self, target, task, seen_duties=None):
        self.task = task.change_engagement(1.0)
        self.on = target
        if self.task.insignificant:
            return self.on
        while self.on and self.task:
            if seen_duties is not None:
                seen_duties |= set(self.on.duties)
            if self.on.task and not self.next_on:
                return self.extend_nodes()
            if self.on.task:
                self.on = self.next_on
                continue
            self.scaled = self.task.change_engagement(1.0 - self.on.engagement)
            if self.scaled.duration == self.on.duration:
                self.on.append_chunk(self.scaled)
                return self.on
            elif self.scaled.duration > self.on.duration:
                self.continue_task()
            elif self.scaled.duration < self.on.duration:
                return self.finish_task()
            if self.task.insignificant:
                return self.on
            if not self.next_on:
                return self.extend_nodes()
            self.on = self.next_on
        raise RuntimeError("Internal Error: Did not place task like it should")

    def prepend_task(self):
        one, two = self.scaled.split(self.scaled.duration - self.on.duration)
        self.on.append_chunk(two)
        self.task = one.change_engagement(1.0)


class _TaskPrepender(_TaskPlacer):
    def continue_task(self):
        self.prepend_task()

    def finish_task(self):
        one, two = self.on.split(self.on.duration - self.scaled.duration)
        two.append_chunk(self.scaled)
        return self.on.replace(one, two)

    @property
    def next_on(self):
        return self.on.before

    def extend_nodes(self):
        return self.on.add_before(self.task.change_engagement(1.0))


class _TaskPostpender(_TaskPlacer):
    def continue_task(self):
        one, two = self.scaled.split(self.on.duration - 0)
        self.on.append_chunk(one)
        self.task = two.change_engagement(1.0)

    def finish_task(self):
        one, two = self.on.split(self.scaled.duration - 0)
        one.append_chunk(self.scaled)
        return self.on.replace(one, two)

    @property
    def next_on(self):
        return self.on.after

    def extend_nodes(self):
        window = _TimeWindow([self.task.change_engagement(1.0)], self.on.pop_queue)
        window.before = self.on
        self.on.after = window
        return window


class FrontloaderState:
    def __init__(self, target):
        self.last_on_checked = None
        self.completed = set()
        self.dependencies = {}
        for window in target.start_from():
            for chunk in window.chunks:
                for depended in chunk.dependeds:
                    if depended not in self.dependencies:
                        self.dependencies[depended] = set()
                    self.dependencies[depended].add(chunk)
        self.loose_tasks = [
            window.pop_task() for window in target.start_from() if window.task
        ]

    def clean_duties(self, on):
        if not on.before:
            return
        if on.before != self.last_on_checked:
            self.clean_duties(on.before)
        for chunk in on.before.chunks:
            if chunk in on.chunks:
                continue
            self.completed.add(chunk)
        self.last_on_checked = on.before

    @property
    def ready(self):
        if len(self.loose_tasks) > 0:
            task = self.loose_tasks[0]
            if task in self.dependencies:
                dependencies = self.dependencies[task]
                left = dependencies.intersection(self.completed)
                if len(left) == len(dependencies):
                    return task
            if task not in self.dependencies:
                return task


class _TimeWindow:
    def __init__(self, chunks=[], pop_queue=[], id=uuid4()):
        self.chunks = [chunk for chunk in chunks if not chunk.insignificant]
        self.id = id
        self.before = None
        self.after = None
        self.popped_duration = None
        self.pop_queue = pop_queue

    @property
    def insignificant(self):
        return self.duration < 0.01

    @property
    def dependeds(self):
        found = set()
        for chunk in self.chunks:
            if hasattr(chunk, "depended") and chunk.depended:
                found.add(chunk.depended)
        return found

    @property
    def duration(self):
        if self.popped_duration:
            return self.popped_duration
        if not self.chunks:
            return 0.0
        return self.chunks[0].duration

    def __contains__(self, chunk):
        return chunk.id in [chunk.id for chunk in self.chunks]

    def __getitem__(self, index):
        on = self.first
        compare = 0
        while on:
            if index == compare:
                return on
            compare += 1
            on = on.after
        return None

    def normalize_inserted(self):
        chunk_ids = set([chunk.id for chunk in self.chunks])
        pre_chunks = [chunk for chunk in self.chunks if chunk.depended.id in chunk_ids]
        ready = [chunk for chunk in self.chunks if chunk.depended.id not in chunk_ids]
        self.chunks = []
        for duty in ready:
            if hasattr(pre, "scale_duration"):
                continue
            if duty.duration == lowest:
                self.append_chunk(duty)
                continue
            chunk, pre = duty.split(lowest)
            self.append_chunk(chunk)
            pre_chunks.append(pre)

        tasks = [duty for pre in ready if hasattr(pre, "scale_duration")]
        for task in tasks:
            pass

    @property
    def first(self):
        on = self
        while on and on.before:
            on = on.before
        return on

    @property
    def last(self):
        on = self
        while on and on.after:
            on = on.after
        return on

    @property
    def task(self):
        for chunk in self.chunks:
            if hasattr(chunk, "scale_duration"):
                return chunk
        return None

    @property
    def duties(self):
        for chunk in self.chunks:
            if chunk != self.task:
                yield chunk

    @property
    def actions(self):
        result = []
        if self.task:
            result.append(self.task)
        result.extend(self.duties)
        return set(result)

    @property
    def weight(self):
        return sum([self.duration * duty.engagement for duty in self.duties])

    def remove_task(self):
        self.chunks = [
            chunk for chunk in self.chunks if not hasattr(chunk, "scale_duration")
        ]
        return self

    def expand_for(self, defineds, completeds_in=None):
        completeds = completeds_in if completeds_in else set()
        dependends = set()
        seen_dependeds = set()
        dependeds = []
        for on in defineds:
            for depended in on.dependeds:
                if depended not in completeds:
                    if depended not in seen_dependeds:
                        seen_dependeds.add(depended)
                        dependeds.append(depended)
                dependends.add(on)
        ready_dependeds = [
            defined
            for defined in defineds
            if not (set(defined.dependeds) - completeds) or not defined.dependeds
        ]
        defineds_hash = {defined: defined for defined in defineds}
        readies = [
            (defineds_hash[ready] if ready in defineds_hash else ready)
            for ready in ready_dependeds
        ]

        ready_duties = [
            duty for duty in readies if not hasattr(duty, "change_engagement")
        ]
        ready_tasks = [task for task in readies if hasattr(task, "change_engagement")]
        pass
        active_task = None
        for task in ready_tasks:
            if self.after and task == self.after.task:
                active_task = task
        if not active_task and ready_tasks:
            active_task = ready_tasks[0]
        if active_task:
            engagement = sum([duty.engagement for duty in ready_duties])
            active_task = active_task.change_engagement(1.0 - engagement)
        for_window = [active_task] + ready_duties if active_task else ready_duties
        duration = min([chunk.duration for chunk in for_window])
        comparable = set(for_window)
        leftovers = [chunk for chunk in defineds if chunk not in comparable]
        for chunk in for_window:
            if chunk.duration == duration:
                completeds.add(chunk)
                self.chunks.append(chunk)
            else:
                one, two = chunk.split(duration)
                self.chunks.append(one)
                leftovers.append(two)
        if leftovers:
            next_target = self.back()
            return next_target.expand_for(leftovers, completeds)
        return self

    def back(self):
        if not self.before:
            self.before = _TimeWindow([], self.pop_queue)
            self.before.after = self
        return self.before

    def forward(self):
        if not self.after:
            self.after = _TimeWindow([], self.pop_queue)
            self.after.before = self
        return self.after

    def add_before(self, chunk):
        if chunk.insignificant:
            return self
        return self.back().add(chunk)

    def prepend(self, chunk):
        for on in self:
            if on.has_id(chunk.id):
                if not hasattr(chunk, "scale_duration") or not on.before:
                    return on.add_before(chunk)
                return on.before.prepend_task(chunk)
            if not on.after:
                return on.add(chunk)
                if hasattr(chunk, "scale_duration"):
                    return on.prepend_task(chunk)
                else:
                    return on.add(chunk)
        raise "Internal error: should have prepended chunk"

    @property
    def ids(self):
        seen = set()
        for on in self:
            for chunk in on.chunks:
                seen.add(chunk.id)
        return seen

    def __iter__(self):
        on = self.first
        while on:
            yield on
            on = on.after

    def __reversed__(self):
        on = self.last
        while on:
            yield on
            on = on.before

    def find_all(self, checker):
        on = self.first
        while on:
            if checker(on):
                yield on
            on = on.after

    def find_chain_around(self, checker):
        on = self
        while on:
            if not checker(on):
                break
            on = on.before
        while on and on != self:
            yield on
            on = on.after
        while on:
            if checker(on):
                yield on
                on = on.after

    def find(self, checker):
        on = self.first
        while on:
            if checker(on):
                return on
            if on and on.after:
                on = on.after
            else:
                break
        return None

    def shared_ids(self, ids):
        return {id for id in ids if self.has_id(id)}

    def has_id(self, id):
        for chunk in self.chunks:
            if type(id) != str and hasattr(id, "__contains__") and chunk.id in id:
                return True
            if chunk.id == id:
                return True
        return False

    def get_partner(self, chunk):
        return self.find(lambda window: self.has_id(chunk.id))

    def prepend_task(self, task):
        return _TaskPrepender()(self, task)

    def pop_next_task(self):
        on = self
        while on:
            if on.task:
                return on.pop_task()
            on = on.after

    def start_window(self, id):
        if not self.has_id(id):
            raise RuntimeError("expected id {} in window {}".format(id, self))
        on = self
        while on.before:
            if not on.before.has_id(id):
                break
            on = on.before
        return on

    def start_from(self, reverse=False):
        on = self
        while on:
            yield on
            on = on.before if reverse else on.after

    @property
    def full_task_weight(self):
        if not self.task:
            return 0
        total = 0
        for on in self.start_from():
            if on.task != self.task:
                break
            total += on.task.engagement * on.task.duration
        if not self.before:
            return total
        for on in self.before.start_from(True):
            if on.task != self.task:
                break
            total += on.task.engagement * on.task.duration.total_seconds
        return total

    def fill_in_gaps(self, dependencies, active, complete):
        news = self.actions.difference(active.union(complete))
        left = active.difference(self.actions)
        active.update(news)
        complete.update(left)
        if self.task:
            return (
                self.after.fill_in_gaps(dependencies, active, complete)
                if self.after
                else self
            )
        destination = self
        on = self
        spare_weight = 0.0
        while not on.task:
            spare_weight += 100.0 - on.weight
            if not on.after:
                return self
            on = on.after
        back = on
        while True:
            if (
                on.task
                and on.task.weight < spare_weight
                and (
                    on.task not in dependencies
                    or len(complete.intersection(dependencies[on.task]))
                    == len(dependencies[on.task])
                )
            ):
                task = on.pop_task()
                target = _TaskPostpender()(on, task, active)
                return target.fill_in_gaps(dependencies, active, complete)
            if not on.after:
                return back.fill_in_gaps(dependencies, active, complete)
            on = on.after

    def frontload_tasks(self, state_in=None):
        state = state_in if state_in else FrontloaderState(self)
        state.clean_duties(self)
        ready = state.ready
        if not ready and self.after:
            return self.after.frontload_tasks(state)
        if not ready and not self.after and state.loose_tasks:
            raise RuntimeError("Internal Error: leftover task error")
        if not ready:
            return self
        target = _TaskPostpender()(self, ready, set())
        state.loose_tasks.remove(ready)
        state.completed.add(ready)
        if not target.after and state.loose_tasks:
            raise RuntimeError("Internal Error: leftover task error")
        if not target.after:
            return target
        return target.after.frontload_tasks(state)

    def place_task(self, task):
        on = self.first
        while on:
            if task.depended and task.depended.id in on.ids:
                return _TaskPrepender()(on, task)
            on = on.after
        return _TaskPrepender()(self.last, task)

    def append_chunk(self, chunk):
        if chunk.insignificant:
            return self
        self.chunks.append(chunk)
        return self

    def split(self, duration):
        splits = [chunk.split(duration) for chunk in self.chunks]
        first, second = list(zip(*splits)) if len(splits) > 0 else ([], [])
        window1 = _TimeWindow(list(first), self.pop_queue)
        window2 = _TimeWindow(list(second), self.pop_queue, self.id)
        window1.after = window2
        window2.before = window1
        if len(splits) == 0:
            window1.popped_duration = duration
            window2.popped_duration = self.duration - duration
        return (window1, window2)

    def replace(self, *nodes):
        if len(nodes) == 0:
            self.before.after = self.after
            self.after.before = self.before
            return self.after
        last = self.before
        for on in nodes:
            on.before = last
            if last:
                last.after = on
            last = on
        last.after = self.after
        if self.after:
            self.after.before = nodes[-1]
        return nodes[0]

    def pop_task(self):
        task = self.task
        if not task:
            return None
        self.popped_duration = task.duration
        for window in self:
            if (
                not window
                or not window.task
                or window.task.id != task.id
                or window == self
            ):
                continue
            window.popped_duration = window.duration
            task = task.merge(window.task)
            window.remove_task()
        self.remove_task()
        return task

    @property
    def weight(self):
        return sum([chunk.weight for chunk in self.chunks])

    @property
    def engagement(self):
        return sum([chunk.engagement for chunk in self.chunks])

    def __repr__(self):
        return "_TimeWindow-" + " | ".join([repr(chunk) for chunk in self.chunks])


class Marker:
    def __init__(self, id, till, is_done=True):
        self.id = id
        self.till = till
        self.is_done = is_done

    def __eq__(self, other):
        low = self.till - timedelta(seconds=0.000001)
        high = self.till + timedelta(seconds=0.000001)
        return (
            self.id == other.id
            and high >= other.till
            and low <= other.till
            and self.is_done == other.is_done
        )

    def __repr__(self):
        return "Marker-id={}:till={}:is_done={}".format(
            self.id, self.till, self.is_done
        )


class Timeline:
    def __init__(self, definitions):
        if len(definitions) == 0:
            return
        self.originals = {str(definition.id): definition for definition in definitions}
        defineds = [_define(definition) for definition in definitions]
        dependencies = _dependencies_from_defineds(defineds)
        self.one = _TimeWindow([]).expand_for(defineds)
        self.one = self.one.first.frontload_tasks()
        self.one = self.one.first.fill_in_gaps(dependencies, set(), set())

    def __repr__(self):
        return "][".join([repr(window) for window in self])

    def __iter__(self):
        duration = 0.0
        active = set()
        if not hasattr(self, "one"):
            return
        for window in self.one:
            local = set([chunk.id for chunk in window.chunks])
            starting = list(local - active)
            starting.sort()
            ended = list(active - local)
            ended.sort()
            for id in ended:
                active.remove(id)
                yield Marker(self.originals[id], timedelta(seconds=duration))
            for id in starting:
                active.add(id)
                yield Marker(self.originals[id], timedelta(seconds=duration), False)
            duration += window.duration
        active_list = list(active)
        active_list.sort()
        for id in active_list:
            yield Marker(self.originals[id], timedelta(seconds=duration))
