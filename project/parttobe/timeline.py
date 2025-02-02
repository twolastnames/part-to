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
        self.container = kwargs["container"] if "container" in kwargs else None
        self.before = kwargs["before"] if "before" in kwargs else None
        self.after = kwargs["after"] if "after" in kwargs else None
        self.engagement = kwargs["engagement"] if "engagement" in kwargs else 1.0

    def weight(self):
        return self.duration * self.engagement

    def split(self, duration):
        task2 = (
            type(self)(
                self.id,
                self.duration - duration,
                engagement=self.engagement,
            ),
        )
        task1 = (
            type(self)(
                self.id,
                duration,
                after=task2,
                engagement=self.engagement,
            ),
        )
        task2.before = task1
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
            self.insert(chunk)
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

    def insert(self, chunk):
        chunk.container = self
        if not self.chunks:
            self.chunks.append(chunk)
            return None
        if (chunk.weight() == 1.0 - self.weight()) and (
            chunk.duration == self.duration
        ):
            self.chunks.append(chunk)
            return self
        if(self.weight() >= 1.0) {

        }

    def pop_mutable(self):
        task = [chunk for chunk in self.chunks if hasattr(chunk, 'scale_duration')]
        self.chunks = [chunk for chunk in self.chunks if not hasattr(chunk, 'scale_duration')]
        return task[0] if task else None


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
    def __init__(self, definitions):
        if len(definitions) == 0:
            return
        for definition in definitions:
            if hasattr(definition, "scale_duration"):
                continue
            self._add_duty(definition)
        for definition in definitions:
            if not hasattr(definition, "scale_duration"):
                continue
            self._add_task(definition)

    def _insert(self, chunks, before=None, after=None):
        self.one = _TimeWindow(chunks, before=before, after=after)

    def _add_duty(self, definition):
        if not hasattr(self, "one"):
            self.one = _TimeWindow([definition])
            return
        for window in self._chain(reversed=True):
            self._insert([definition])

    def _add_task(self, definition):
        if not hasattr(self, "one"):
            self.one = _TimeWindow([definition])
            return
        # window = self._get_first()
        # while window.after:
        for window in self._chain():
            print("wwww", window, definition)
            if definition.dependent and definition.dependent in window:
                print("bbbbb0")
                if window.before:
                    print("bbbbb")
                    window.before.insert(definition)
                else:
                    print("bbbbb2")
                    self._insert([definition], window.before, window)
                return
            elif definition in window.dependents:
                print("aaaaaa0")
                if window.after:
                    print("aaaaaa")
                    window.after.insert(definition)
                else:
                    print("aaaaaa1")
                    self._insert([definition], window, window.after)
                return
            # window = window.after
        if self._get_first():
            self.one = self._get_first().insert(definition)
            return
        self._insert(definition)
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

    def _get_first(self):
        on = self.one
        while on and on.before:
            on = on.before
        return on

    def _get_last(self):
        on = self.one
        while on and on.after:
            on = on.after
        return on

    def _chain(self, reversed=False, start=None):
        window = (
            start if start else (self._get_last() if reversed else self._get_first())
        )
        while window:
            yield window
            window = window.before if reversed else window.after

    def __repr__(self):
        return "][".join([repr(window) for window in self._chain()])

    def __iter__(self):
        duration = 0.0
        active = set()
        if not hasattr(self, "one"):
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
