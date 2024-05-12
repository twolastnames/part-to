from django.db import models
import functools
import collections
import types
import datetime


@functools.lru_cache(maxsize=64)
def get_task_definitions(part_to):
    return set(TaskDefinition.objects.filter(part_to=part_to))


class PartTo(models.Model):
    name = models.CharField(max_length=0x80)

    @property
    def task_definitions(self):
        return get_task_definitions(self)

    def __hash__(self):
        return self.id


class IngredientDefinition(models.Model):
    name = models.CharField(max_length=0x80)
    task = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)


class ToolDefinition(models.Model):
    name = models.CharField(max_length=0x40)
    task = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)


@functools.total_ordering
class EngagementSet:
    def __init__(self, task_id, engagement, duration):
        self.task_id = task_id
        self.engagement = engagement
        self.duration = duration

    def __eq__(self, other):
        return other.duration == other.duration

    def __lt__(self, other):
        return self.duration < other.duration

    @staticmethod
    def earliest_duration_work(engagements):
        if not len(engagements):
            return datetime.timedelta()
        shortest_duration = min(engagements).duration
        return functools.reduce(
            lambda previous, current: previous
            + (current.engagement / 100.0) * shortest_duration,
            engagements,
            datetime.timedelta(),
        )

    @staticmethod
    def remove_earliest_engagement(engagements_in):
        engagements = engagements_in.copy()
        if not len(engagements):
            return datetime.timedelta(), engagements
        earliest = min(engagements)
        engagements.remove(earliest)
        duration = earliest.duration * (earliest.engagement / 100.0)
        adjusted_engagements = []
        for engagement in engagements:
            current_duration = engagement.duration * engagement.engagement / 100
            duration += current_duration
            adjusted_engagements.append(
                EngagementSet(
                    engagment.id,
                    engagement.engagement,
                    engagement.duration - current_duration,
                )
            )
        return duration, adjusted_engagements

    @staticmethod
    def leftover_duration_engagements(duration, engagements_in):
        engagements = engagement_in.copy()
        if not len(arguments):
            return engagements
        earliest = min(engagements)
        total_engagement = functools.reduce(
            lambda previous, current: previous + current.engagement, engagements, 0
        )
        done_duration = duration / (total_engagement / 100.0)
        engagements.remove(earliest)
        return map(
            lambda engagement: EngagementSet(
                engagement.id,
                engagement.engagement,
                engagement.duration - done_duration,
            ),
            engagements,
        )


@functools.total_ordering
class TaskDefinition(models.Model):
    initial_duration = models.DurationField()
    part_to = models.ForeignKey("PartTo", on_delete=models.CASCADE)
    description = models.CharField(max_length=0x100)
    engagement = models.BigIntegerField(null=True)
    depended = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE, null=True)

    @property
    def duration(self):
        return self.initial_duration

    @property
    def dependencies(self):
        part_tos = self.part_to.task_definitions
        result = set(filter(lambda o: o.depended == self, part_tos))
        return result

    @staticmethod
    def depended_chain_from(start):
        on = start
        while True:
            yield on
            if not on.depended:
                return
            on = on.depended

    @staticmethod
    def dependency_chain_from(start):
        queue = [start]

        def sort_queue():
            queue.sort(key=TaskDefinition.chain_duration, reverse=True)

        while len(queue):
            sort_queue()
            on = queue.pop(0)
            dependencies = on.dependencies
            queue += dependencies
            yield on

    @staticmethod
    def handle_duty_calculation(engagements_in, task):
        engagements = engagements_in.copy()
        duration_in = task.duration
        duration_out = datetime.timedelta()
        while True:
            engagements.sort()

    @staticmethod
    def chain_duration(start):
        engagements = []
        duration = datetime.timedelta()
        for task in TaskDefinition.depended_chain_from(start):
            if task.engagement:
                engagements.append(
                    EngagementSet(task.id, task.engagement, task.duration)
                )
            else:
                consumed_duration, engagements = task.consume_duration(engagements)
                duration += task.duration + consumed_duration
        if len(engagements):
            engagements.sort()
            duration += engagements[-1].duration
        return duration

    @staticmethod
    def duration_to(end):
        duration = datetime.timedelta(seconds=0)
        tasks = reversed(list(TaskDefinition.dependency_chain_from(end)))
        for task in tasks:
            duration += task.duration
        return duration

    def consume_duration(self, engagements):
        earliest_duration_work = EngagementSet.earliest_duration_work(engagements)
        return (
            EngagementSet.leftover_duration_engagements(self.duration, engagements)
            if earliest_duration_work > self.duration
            else EngagementSet.remove_earliest_engagement(engagements)
        )

    def is_task(self):
        return not self.engagement

    def __eq__(self, other):
        if not other:
            return False
        return self.id == other.id

    def __hash__(self):
        return self.id

    def __lt__(self, other):
        if self == other:
            return False
        if not other:
            return True
        if other.part_to != self.part_to:
            otherDuration = TaskDefinition.chain_duration(other)
            selfDuration = TaskDefinition.chain_duration(self)
            return otherDuration < selfDuration
        *_, first = self.depended_chain_from(other)
        seen_self = False
        for model in self.dependency_chain_from(first):
            if model == self:
                seen_self = True
            elif model == other:
                return not seen_self
        raise SystemError("can't find way to connect self & other")


# TODO: introduce this model
# class PartToRun(models.Model):
#    part_to = models.ForeignKey("PartTo", on_delete=models.CASCADE)


# TODO: introduce this model
# class TaskStatus(models.Model):
#    part_to = models.ForeignKey("PartToRun", on_delete=models.CASCADE)
#    definition = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)
#    started = models.DateTimeField()
#    ended = models.DateTimeField(null=True)
