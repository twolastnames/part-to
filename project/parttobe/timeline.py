from dataclasses import dataclass

# @dataclass
# class Marker:
#    identifier: str
#    is_front: boolean


class TimeOverfill(RuntimeError):
    pass


def define(definition):
    if hasattr(definition, "engagement") and (
        definition.engagement != 0.0 and definition.engagement is not None
    ):
        return _Duty(str(definition.id), float(definition.duration))
    else:
        return _Task(str(definition.id), float(definition.duration), engagement=1.0)


class _Chunk:
    def __init__(self, id, duration, **kwargs):
        self.id = id
        self.duration = duration
        self.dependent = kwargs["dependent"] if "dependent" in kwargs else None
        self.engagement = kwargs["engagement"] if "engagement" in kwargs else 1.0

    def weight(self):
        return self.duration * self.engagement

    def split(self, duration):
        task2 = (
            type(self)(
                self.id,
                self.duration - duration,
                dependent=self.dependent,
                engagement=self.engagement,
            ),
        )
        task1 = (
            type(self)(
                self.id,
                duration,
                dependent=task2,
                engagement=self.engagement,
            ),
        )
        return [task1, task2]

    def __repr__(self):
        return "id={}:duration={}:engagement={}".format(
            self.id, self.duration, self.engagement
        )


class _Task(_Chunk):

    def change_engagement(self, engagement):
        return Task(
            self.id,
            self.weight() / engagement,
            dependent=self.dependent,
            engagement=engagement,
        )

    def scale_duration(self, duration):
        return self.change_engagement(self.weight() / duration)


class _Duty(_Chunk):
    pass


class _TimeWindow:
    def __init__(self, chunks=[], before=None, after=None):
        self.chunks = []
        for chunk in chunks:
            self.chunks.append(chunk)
        self.before = before
        self.after = after
        if before:
            before.after = self
        if after:
            after.before = self

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

    def append(self, chunk):
        if not self.chunks:
            self.chunks.append(chunk)
            return None

    def weight(self):
        return sum([chunk.weight() for chunk in self.chunks])

    def __repr__(self):
        return "|".join([repr(chunk) for chunk in self.chunks])


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
        return "id={}:till={}:is_done={}".format(self.id, self.till, self.is_done)


class Timeline:
    def __init__(self):
        self.one = None

    def _insert(self, chunks, before=None, after=None):
        self.one = _TimeWindow(
            chunks, before=before, after=after
        )


    def _add_duty(self, definition):
        for window in self._chain(reversed=True):
            pass

    def _add_task(self, definition):
        for window in self._chain():
            if (
                definition.dependent
                and definition.dependent in window
            ):
                self._insert(
                    [definition], window.before, window
                )
                return
            if definition in window.dependents:
                self._insert(
                    [definition], window, window.after
                )
                return
        _TimeWindow([definition], after=self.one)

 

    def add(self, definition):
        if not definition:
            return
        if not self.one:
            self._insert([definition])
            return
        if hasattr(definition, 'scale_duration'):
            return self._add_task(definition)
        self._add_duty(duration)

    def _get_first(self):
        on = self.one
        while on.before:
            on = on.before
        return on

    def _get_last(self):
        on = self.one
        while on.after:
            on = on.after
        return on

    def _chain(self, reversed=False, start=None):
        window = start if start else (self._get_last() if reversed else self._get_first())
        while window:
            yield window
            window = window.before if reversed else window.after

    def __repr__(self):
        return "][".join([repr(window) for window in self._chain()])

    def __iter__(self):
        duration = 0.0
        active = set()
        if not self.one:
            return
        for window in self._chain():
            local = set([chunk.id for chunk in window.chunks])
            starting = local - active
            ended = active - local
            for id in ended:
                active.remove(id)
                yield Marker(id, duration)
            for id in starting:
                active.add(id)
                yield Marker(id, duration, False)
            duration += window.duration
        for id in active:
            yield Marker(id, duration)
