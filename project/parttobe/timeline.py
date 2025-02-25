from dataclasses import dataclass
import functools
from datetime import timedelta
from uuid import uuid4

# @dataclass
# class Marker:
#    identifier: str
#    is_front: boolean


class TimeOverfill(RuntimeError):
    pass


def _define(definition):
    if hasattr(definition, "engagement") and (
        definition.engagement != 0.0 and definition.engagement is not None
    ):
        return _Duty(
            definition.id,
            float(definition.duration.seconds),
            engagement=definition.engagement,
            dependent=definition.dependent,
        )
    else:
        return _Task(
            definition.id,
            float(definition.duration.seconds),
            engagement=1.0,
            dependent=definition.dependent,
        )


@functools.total_ordering
class _Chunk:
    def __init__(self, id, duration, **kwargs):
        self.id = id
        self.duration = duration
        self.container = kwargs["container"] if "container" in kwargs else None
        self.dependent = kwargs["dependent"] if "dependent" in kwargs else None
        # self.before = kwargs["before"] if "before" in kwargs else None
        # self.after = kwargs["after"] if "after" in kwargs else None
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
        )
        task1 = type(self)(
            self.id,
            duration,
            after=task2,
            engagement=self.engagement,
        )
        # task2.before = task1
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
            dependent=self.dependent,
            engagement=engagement,
        )

    def scale_duration(self, duration):
        return self.change_engagement(self.weight / duration)

    def merge(self, *tasks):
        duration = sum([task.change_engagement(1.0).duration for task in tasks]) + self.change_engagement(1.0).duration
        return _Task(self.id, duration, dependent=self.dependent, engagement=1.0)


class _Duty(_Chunk):
    pass

class _TimeWindow:
    def __init__(self, chunks=[], id=uuid4()):
        self.chunks = [chunk for chunk in chunks if not chunk.insignificant]
        #for chunk in chunks:
        #    self.add(chunk)
        self.id = id
        self.before = None
        self.after = None

    @property
    def dependents(self):
        found = set()
        for chunk in self.chunks:
            if hasattr(chunk, "dependent") and chunk.dependent:
                found.add(chunk.dependent)
        return found

    @property
    def duration(self):
        if not self.chunks:
            return 0.0
        return self.chunks[0].duration

    def __contains__(self, chunk):
        return chunk.id in [chunk.id for chunk in self.chunks]

    def normalize_inserted(self):
        chunk_ids = set([chunk.id for chunk in self.chunks])
        pre_chunks = [chunk for chunk in self.chunks if chunk.depended.id in chunk_ids]
        ready = [chunk for chunk in self.chunks if chunk.depended.id not in chunk_ids]

        # lowest = min([chunk.duration for chunk in ready])
        # highest = max([chunk.duration for chunk in ready])
        # if lowest == highest and self.weight <= 1.0 and not pre_chunks:
        #    return self
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
        while on and hasattr(on, 'before') and on.before:
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

    def remove_task(self):
        self.chunks = [chunk for chunk in self.chunks if not hasattr(chunk, "scale_duration")]
        return self

    def add_before(self, chunk):
        if chunk.insignificant:
            return self
        if not self.before:
            self.before = _TimeWindow([])
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
        raise 'Internal error: should have prepended chunk'

    def __iter__(self):
        on = self.first
        while on:
            yield on
            on = on.after

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
            if on and hasattr(on, 'after'):
                on = on.after
            else:
                break
        return None

    def has_id(self, id):
        for chunk in self.chunks:
            if chunk.id == id:
                return True
        return False

    def get_partner(self, chunk):
        return self.find(lambda window: self.has_id(chunk.id))

    #def initial_add(self, chunk):
    #    id = self.id
    #    on = self.add(chunk)
    #    return on.find(lambda window: window.id == id)

    def prepend_task(self, task):
        task_left = task.change_engagement(1.0)
        on = self
        while on  and task_left:
            if task_left.insignificant:
                return on
            scaled = task_left.change_engagement(1.0 - on.engagement)
            if scaled.duration == on.duration:
                on.append_chunk(scaled)
                return on
            elif scaled.duration > on.duration:
                one, two = scaled.split(scaled.duration - self.duration)
                on.append_chunk(two)
                task_left = one.change_engagement(1.0)
            elif scaled.duration < on.duration:
                one, two = on.split(on.duration - scaled.duration)
                two.append_chunk(scaled)
                return  on.replace(one, two)
            if not on.before:
                return on.add_before(task_left)
            on = on.before

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
            scaled = chunk.change_engagement(1.0 - self.engagement)
            if scaled.duration == self.duration:
                self.append_chunk(scaled)
                return self
            if scaled.duration > self.duration:
                one, two = scaled.split(scaled.duration - self.duration)
                self.append_chunk(two)
                return self.prepend(one.change_engagement(1.0))
            if scaled.duration < self.duration:
                one, two = self.split(self.duration - scaled.duration)
                two.append_chunk(scaled)
                return  self.replace(one, two)
                #return on.prepend(scaled)
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
                task = self.pop_task()
                self.append_chunk(chunk)
                return self.prepend(task)
            if chunk.duration > self.duration:
                chunk1, chunk2 = chunk.split(chunk.duration - self.duration)
                task = self.pop_task()
                self.append_chunk(chunk2)
                on = self.prepend(chunk1)
                on = on.prepend(task)
                return on
            if chunk.duration < self.duration:
                single, pair = self.split(self.duration - chunk.duration)
                pair.append_chunk(chunk)
                task = self.pop_task()
                on = self.replace(single, pair)
                return on.prepend(task)
        raise RuntimeError("did not know add instructions")

    def append_chunk(self, chunk):
        if chunk.insignificant:
            return self
        self.chunks.append(chunk)
        return self

    def split(self, duration):
        splits = [chunk.split(duration) for chunk in self.chunks]
        first, second = list(zip(*splits))
        window1 = _TimeWindow(list(first))
        window2 = _TimeWindow(list(second), self.id)
        window1.after = window2
        window2.before = window1
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
        on.after = self.after
        return on

    def pop_task(self):
        task = self.task
        if not task:
            return None
        for window in self:
            if not window or not window.task or window.task.id != task.id or window == self:
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


class IncompatibleMarkerPairError(RuntimeError):
    pass


class Marker:
    def __init__(self, id, till, is_done=True):
        self.id = id
        self.till = till
        self.is_done = is_done

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.till == other.till
            and self.is_done == other.is_done
        )

    def __repr__(self):
        return "Marker-id={}:till={}:is_done={}".format(self.id, self.till, self.is_done)


class Timeline:
    def __init__(self, definitions):
        if len(definitions) == 0:
            return
        self.originals = {definition.id: definition for definition in definitions}
        defineds = [_define(definition) for definition in definitions]
        dependends = {
            on.dependent: on
            for on in defineds
            if hasattr(on, "dependent") and on.dependent
        }
        inserteds = set(
            [on for on in defineds if not hasattr(on, "dependent") or not on.dependent]
        )
        to_insert = list(inserteds)
        to_insert.sort()
        self.one = _TimeWindow([])
        while True:
            for insertable in to_insert:
                if self.one.find(lambda window: insertable.dependent in window.chunks):
                    self.one = self.one.find(
                        lambda window: insertable.dependent in window.chunks
                    ).add_before(insertable)
                else:
                    self.one = self.one.last.add(insertable)
            to_insert = []
            for key, value in dependends.items():
                if key in inserteds:
                    inserteds.add(value)
                    to_insert.append(value)
            for key in to_insert:
                del dependends[key.dependent]
            if not to_insert:
                return

        # self.one = _TimeWindow(list(inserteds))
        # self.one = self.one.normalize_inserted()
        # while dependends:
        #    self.one = self.one.first
        #    to_insert = [dependends[seen.id] for seen in inserteds ]
        #    for insert in to_insert:
        #        inserteds.add(insert)
        #        dependends.popitem(insert.id)
        #    self.one = self.one.last
        #    self.one.chunks = self.one.chunks + to_insert
        #    self.one = self.one.normalize_inserted()

    #        for definition in definitions:
    #            if hasattr(definition, "scale_duration"):
    #                continue
    #            self._add_duty(definition)
    #        for definition in definitions:
    #            if not hasattr(definition, "scale_duration"):
    #                continue
    #            self._add_task(definition)
    #
#    def _insert(self, chunks, before=None, after=None):
#        self.one = _TimeWindow(chunks, before=before, after=after)
#
#    def _add_duty(self, definition):
#        if not hasattr(self, "one"):
#            self.one = _TimeWindow([definition])
#            return
#        for window in self._chain(reversed=True):
#            self._insert([definition])
#
#    def _add_task(self, definition):
#        if not hasattr(self, "one"):
#            self.one = _TimeWindow([definition])
#            return
#        # window = self._get_first()
#        # while window.after:
#        for window in self._chain():
#            if hasattr(definition, "dependent") and definition.dependent in window:
#                if window.before:
#                    window.before.insert(definition)
#                else:
#                    self._insert([definition], window.before, window)
#                return
#            elif definition in window.dependents:
#                if window.after:
#                    window.after.insert(definition)
#                else:
#                    self._insert([definition], window, window.after)
#                return
#            # window = window.after
#        if self._get_first():
#            self.one = self._get_first().insert(definition)
#            return
#        self._insert(definition)
        # _TimeWindow([definition], after=self.one)

        # for window in self._chain():
        #    if definition.dependent and definition.dependent in window:
        #        self._insert([definition], window.before, window)
        #        return
        #    if definition in window.dependents:
        #        self._insert([definition], window, window.after)
        #        return

    #    def add(self, definition):
    #            if not definition:
    #                return
    #            if not self.one:
    #                self._insert([definition])
    #                return
    #            if hasattr(definition, 'scale_duration'):
    #                return self._add_task(definition)
    #            self._add_duty(duration)

    #    def _chain(self, reversed=False, start=None):
    #        window = (
    #            start if start else (self._get_last() if reversed else self._get_first())
    #        )
    #        while window:
    #            yield window
    #            window = window.before if reversed else window.after

    def __repr__(self):
        return "][".join([repr(window) for window in self._chain()])

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
