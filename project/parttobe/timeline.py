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
        self.depended = None

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


def _define(definition):
    if not definition:
        return None
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
            depended=_define(definition.depended),
        )
    else:
        return _Task(
            str(definition.id),
            float(definition.duration.seconds),
            engagement=1.0,
            depended=_define(definition.depended),
        )


@functools.total_ordering
class _Chunk:
    def __init__(self, id, duration, **kwargs):
        self.id = id
        self.duration = duration
        self.container = kwargs["container"] if "container" in kwargs else None
        self.depended = kwargs["depended"] if "depended" in kwargs else None
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
            depended=self.depended,
        )
        task1 = type(self)(
            self.id,
            duration,
            after=task2,
            engagement=self.engagement,
            depended=self.depended,
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
            self.weight / engagement,
            depended=self.depended,
            engagement=engagement,
        )

    def scale_duration(self, duration):
        return self.change_engagement(self.weight / duration)

    def merge(self, *tasks):
        duration = (
            sum([task.change_engagement(1.0).duration for task in tasks])
            + self.change_engagement(1.0).duration
        )
        return _Task(self.id, duration, depended=self.depended, engagement=1.0)


class _Duty(_Chunk):
    pass


class _TaskPlacer:
    def __call__(self, target, task):
        self.task = task.change_engagement(1.0)
        self.on = target
        while self.on and self.task:
            if self.task.insignificant:
                return self.on
            if self.on.task and not self.next_on:
                return self.extend_nodes()
            if self.on.task and self.next_on:
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
            if not self.next_on:
                return self.extend_nodes()
            self.on = self.next_on


class _TaskPrepender(_TaskPlacer):
    def continue_task(self):
        one, two = self.scaled.split(self.scaled.duration - self.on.duration)
        self.on.append_chunk(two)
        self.task = one.change_engagement(1.0)

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


class TaskFrontloader:
    def __init__(self, one, defineds):
        self.one = one
        self.defineds = defineds
        self.find_dependencies()
        self.done = set()

    def find_dependencies(self):
        self.dependencies = {}
        self.dependeds = {}
        for on in self.defineds:
            if not hasattr(on, "depended") or not on.depended:
                continue
            self.dependeds[on] = on.depended
            try:
                self.dependencies[on.depended].add(on)
            except KeyError:
                self.dependencies[on.depended] = {on}

    def pop_tasks(self):
        self.tasks = set()
        gapped = False
        for on in self.one:
            if not on.task:
                gapped = True
            elif gapped:
                self.tasks.add(on.pop_task())
            else:
                self.done.add(on.task)

    def find_duty_order(self):
        seen_duties = set()
        self.duty_order = []
        for on in self.one:
            for chunk in on.chunks:
                if chunk in seen_duties:
                    continue
                seen_duties.add(chunk)
                self.duty_order.append(chunk)

    def get_next_task_depended(self):
        ready = sorted(
            [
                task
                for task in sorted(self.tasks)
                if not (
                    task in self.dependencies
                    and (
                        (self.dependencies[task] & self.tasks)
                        or (
                            len(self.dependencies[task] & self.done)
                            != len(self.dependencies[task])
                        )
                    )
                )
            ],
            key=lambda task: -task.duration,
        )
        if len(ready) > 0:
            return ready[0]

    def __call__(self):
        self.pop_tasks()
        self.find_duty_order()
        on = self.one.first
        active_duties = set()
        while self.tasks and on:
            leftovers = active_duties.difference(on.chunks)
            active_duties = set(on.duties).union(active_duties)
            for leftover in leftovers:
                if (
                    hasattr(leftover, "change_engagement")
                    or not leftover.engagement
                    or leftover.engagement == 1.0
                ):
                    continue
                active_duties.remove(leftover)
                self.done.add(leftover)

            while self.tasks:
                task = self.get_next_task_depended()
                if not task:
                    break
                self.tasks.remove(task)
                on = self.one = _TaskPostpender()(on, task)
                self.done.add(task)
            on = on.after
        return self.one


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

    def remove_task(self):
        self.chunks = [
            chunk for chunk in self.chunks if not hasattr(chunk, "scale_duration")
        ]
        return self

    def add_before(self, chunk):
        if chunk.insignificant:
            return self
        if not self.before:
            self.before = _TimeWindow([], self.pop_queue)
            self.before.after = self
        return self.before.add(chunk)

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

    def frontload_tasks(self):
        seen = set()
        on = self
        while True:
            task = None
            if on.task or (on.task and on.task.id in seen):
                if not on.after:
                    return on
                on = on.after
                continue
            task = on.pop_next_task()
            if not task:
                return on
            seen.add(task.id)
            on = _TaskPostpender()(on, task)
            if not task:
                return on
            if not on.after:
                return on
            on = on.after

    def place_task(self, task):
        on = self.first
        seen_dependency = False
        while on.after:
            if on.id in on.dependeds:
                seen_dependency = True
            elif seen_dependency and on.task:
                return _TaskPrepender()(self, task)
            on = on.after
            continue
        return _TaskPrepender()(self.last, task)

    def add(self, chunk):
        if chunk.insignificant:
            return self
        chunk.container = self
        partner = self.get_partner(chunk)
        if partner:
            return partner.add_before(chunk)
        if not self.chunks:
            self.chunks = [chunk]
            return self
        if hasattr(chunk, "scale_duration") and self.task:
            return self.add_before(chunk)
        if hasattr(chunk, "change_engagement") and not self.task:
            return self.prepend_task(chunk)
        if not hasattr(chunk, "scale_duration") and not self.task:
            if chunk.duration == self.duration:
                self.append_chunk(chunk)
                return self
            if chunk.duration > self.duration:
                one, two = chunk.split(chunk.duration - self.duration)
                self.append_chunk(two)
                return self.prepend(one)
            if chunk.duration < self.duration:
                single, pair = self.split(self.duration - chunk.duration)
                pair.append_chunk(chunk)
                on = self.replace(single, pair)
                return on
        if not hasattr(chunk, "scale_duration") and self.task:
            if chunk.duration == self.duration:
                self.pop_queue.append(self.pop_task())
                self.append_chunk(chunk)
                return self.place_task(self.pop_queue.pop(0))
            if chunk.duration > self.duration:
                chunk1, chunk2 = chunk.split(chunk.duration - self.duration)
                self.pop_queue.append(self.pop_task())
                self.append_chunk(chunk2)
                on = self.prepend(chunk1)
                return on.place_task(self.pop_queue.pop(0))
            if chunk.duration < self.duration:
                single, pair = self.split(self.duration - chunk.duration)
                pair.append_chunk(chunk)
                self.pop_queue.append(self.pop_task())
                single.pop_task()
                pair.pop_task()
                on = self.replace(single, pair) if single.chunks else self.replace(pair)
                return on.place_task(self.pop_queue.pop(0))
        raise RuntimeError("did not know add instructions")

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
        self.originals = {definition.id: definition for definition in definitions}
        defineds = [_define(definition) for definition in definitions]
        dependends = {}
        for on in defineds:
            if hasattr(on, "depended") and on.depended:
                if on.depended not in dependends:
                    dependends[on.depended] = []
                dependends[on.depended].append(on)
        orphans = [
            defined
            for defined in defineds
            if defined.depended and defined.depended not in defineds
        ]
        inserteds = set(
            [on for on in defineds if not hasattr(on, "depended") or not on.depended]
            + orphans
        )
        to_insert = (
            [defined for defined in inserteds if defined in dependends]
            + [defined for defined in inserteds if defined not in dependends]
            + orphans
        )
        self.one = _TimeWindow([])
        while True:
            for insertable in to_insert:
                if self.one.find(lambda window: insertable.depended in window.chunks):
                    self.one = self.one.find(
                        lambda window: insertable.depended in window.chunks
                    ).add_before(insertable)
                else:
                    self.one = self.one.last.add(insertable)
            to_insert = []
            nexts = set()
            for key, value in dependends.items():
                if key in inserteds:
                    nexts.update(set(value))
                    to_insert.extend(value)
            inserteds.update(nexts)
            for key in to_insert:
                if key.depended in dependends:
                    del dependends[key.depended]
            if not to_insert:
                break
        self.one = TaskFrontloader(self.one, defineds)()
        return

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
