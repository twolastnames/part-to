from django.db import models
import functools
import collections
import types
import datetime
import uuid
import re


@functools.lru_cache(maxsize=64)
def get_task_definitions(part_to):
    return set(TaskDefinition.objects.filter(part_to=part_to))


class PartTo(models.Model):
    name = models.CharField(max_length=0x80)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        indexes = [models.Index(fields=["uuid"])]

    @property
    def task_definitions(self):
        return get_task_definitions(self)

    def __hash__(self):
        return self.id


class IngredientDefinition(models.Model):
    name = models.CharField(max_length=0x80)
    task = models.ForeignKey(
        "TaskDefinition",
        on_delete=models.CASCADE,
    )


class ToolDefinition(models.Model):
    name = models.CharField(max_length=0x40)
    task = models.ForeignKey(
        "TaskDefinition",
        on_delete=models.CASCADE,
    )


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
    def remove_earliest_engagement(
        engagements_in,
    ):
        engagements = engagements_in.copy()
        if not len(engagements):
            return (
                datetime.timedelta(),
                engagements,
            )
        earliest = min(engagements)
        engagements.remove(earliest)
        duration = earliest.duration * (earliest.engagement / 100.0)
        adjusted_engagements = []
        for engagement in engagements:
            current_duration = (
                engagement.duration * engagement.engagement / 100
            )
            duration += current_duration
            adjusted_engagements.append(
                EngagementSet(
                    engagement.task_id,
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
            lambda previous, current: previous + current.engagement,
            engagements,
            0,
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
    depended = models.ForeignKey(
        "TaskDefinition",
        on_delete=models.CASCADE,
        null=True,
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        indexes = [models.Index(fields=["uuid"])]

    @property
    def duration(self):
        return self.initial_duration

    @property
    def dependencies(self):
        part_tos = self.part_to.task_definitions
        result = set(
            filter(
                lambda o: o.depended == self,
                part_tos,
            )
        )
        return result

    def depended_chain_from(self):
        on = self
        while True:
            yield on
            if not on.depended:
                return
            on = on.depended

    def dependency_chain_from(self):
        queue = [self]

        def sort_queue():
            queue.sort(
                key=TaskDefinition.chain_duration,
                reverse=True,
            )

        while len(queue):
            sort_queue()
            on = queue.pop(0)
            dependencies = on.dependencies
            queue += dependencies
            yield on

    def depends_on(self, other):
        for task in self.dependency_chain_from():
            if other == task:
                return True
        return False

    def duties(self):
        for task in self.depended_chain_from():
            if not task.is_task():
                yield

    def weight(self):
        return (
            self.duration
            if self.is_task()
            else self.duration * (self.engagement / 100.0)
        )

    @staticmethod
    def handle_duty_calculation(engagements_in, task):
        engagements = engagements_in.copy()
        duration_in = task.duration
        duration_out = datetime.timedelta()
        while True:
            engagements.sort()

    def chain_duration(self):
        engagements = []
        duration = datetime.timedelta()
        for task in TaskDefinition.depended_chain_from(self):
            if task.engagement:
                engagements.append(
                    EngagementSet(
                        task.id,
                        task.engagement,
                        task.duration,
                    )
                )
            else:
                (
                    consumed_duration,
                    engagements,
                ) = task.consume_duration(engagements)
                duration += task.duration + consumed_duration
        if len(engagements):
            engagements.sort()
            duration += engagements[-1].duration
        return duration

    def duration_to(self):
        duration = datetime.timedelta(seconds=0)
        tasks = reversed(
            list(TaskDefinition.dependency_chain_from(self))
        )
        for task in tasks:
            duration += task.duration
        return duration

    def consume_duration(self, engagements):
        earliest_duration_work = EngagementSet.earliest_duration_work(
            engagements
        )
        return (
            EngagementSet.leftover_duration_engagements(
                self.duration, engagements
            )
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
            otherDuration = other.chain_duration()
            selfDuration = self.chain_duration()
            return otherDuration < selfDuration
        *_, first = other.depended_chain_from()
        seen_self = False
        for model in first.dependency_chain_from():
            if model == self:
                seen_self = True
            elif model == other:
                return not seen_self
        raise SystemError("can't find way to connect self & other")


class PartToRun(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        indexes = [models.Index(fields=["uuid"])]

    def left_definitions(self):
        definitions = set()
        run_parts = RunPart.objects.filter(run=self)
        for run_part in run_parts:
            definitions.update(get_task_definitions(run_part.part_to))
        started = TaskStatus.objects.filter(run=self.id)
        started_definitions = set(self.unwaiting_definitions())
        return filter(
            lambda definition: definition not in started_definitions,
            definitions,
        )

    def startable_duties(self):
        leftover_duties = list(
            filter(
                lambda definition: not definition.is_task(),
                self.left_definitions(),
            )
        )
        leftover_duties.sort(
            key=lambda definition: definition.chain_duration(),
            reverse=True,
        )
        return leftover_duties

    def running_definitions(self):
        started = TaskStatus.objects.filter(
            run=self,
            started__isnull=False,
            ended__isnull=True,
        )
        return map(
            lambda task: task.definition,
            started,
        )

    def running_tasks(self):
        return filter(
            lambda definition: definition.is_task(),
            self.running_definitions(),
        )

    def running_duties(self):
        return filter(
            lambda definition: not definition.is_task(),
            self.running_definitions(),
        )

    def unwaiting_definitions(self):
        started = TaskStatus.objects.filter(
            run=self.id, started__isnull=False
        )
        return map(
            lambda task: task.definition,
            started,
        )

    def until_next_duty(self):
        duties = self.startable_duties()
        if len(duties) == 0:
            return None
        duty = duties[0]
        left_tasks = list(
            filter(
                lambda definition: definition.is_task(),
                self.left_definitions(),
            )
        ) + list(
            filter(
                lambda definition: definition.is_task(),
                self.running_definitions(),
            )
        )
        left_tasks.sort()
        task_sum = datetime.timedelta()
        for task in left_tasks:
            if task.depends_on(duty):
                continue
            task_sum += task.duration
        task_sum += duty.weight()
        until = task_sum - duty.duration
        return (
            until
            if until > datetime.timedelta()
            else datetime.timedelta()
        )

    def first_undones(self):
        lefts = self.left_definitions()
        unwaiting_definitions = set(self.unwaiting_definitions())
        earliests = {}
        for left in lefts:
            for dependency in left.dependency_chain_from():
                if dependency in unwaiting_definitions:
                    continue
                earliests[dependency.part_to] = dependency
        return earliests

    def __next__(self):
        next_duty_time = self.until_next_duty()
        duties = self.startable_duties()
        if (
            next_duty_time is not None
            and next_duty_time <= datetime.timedelta()
        ):
            return TaskStatus.objects.create(
                run=self, definition=duties[0]
            )
        left = list(
            filter(
                lambda definition: definition.is_task(),
                self.left_definitions(),
            )
        )
        if len(left) == 0:
            raise StopIteration
        left.sort()
        if left[0] in map(lambda task: task.depended, duties):
            return TaskStatus.objects.create(
                run=self, definition=duties[0]
            )
        return TaskStatus.objects.create(run=self, definition=left[0])


class TaskStatus(models.Model):
    run = models.ForeignKey("PartToRun", on_delete=models.CASCADE)
    definition = models.ForeignKey(
        "TaskDefinition",
        on_delete=models.CASCADE,
    )
    started = models.DateTimeField(default=datetime.datetime.now)
    ended = models.DateTimeField(null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        indexes = [models.Index(fields=["uuid"])]

    def __call__(self):
        self.ended = datetime.datetime.now()
        self.save()


class RunPart(models.Model):
    part_to = models.ForeignKey("PartTo", on_delete=models.CASCADE)
    run = models.ForeignKey("PartToRun", on_delete=models.CASCADE)


def start_run(part_tos):
    run = PartToRun.objects.create()
    for part_to in part_tos:
        RunPart.objects.create(part_to=part_to, run=run)
    return run
