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
        unique_together = [("uuid")]
        indexes = [models.Index(fields=["uuid"])]

    @property
    def task_definitions(self):
        return get_task_definitions(self)

    def __hash__(self):
        return self.id


DependedInformation = collections.namedtuple("DepenededInformation", "part_to depended")


class Engagement(collections.namedtuple("EngagementBase", "duty duration engagement")):
    def __eq__(self, other):
        return other.duration == other.duration

    def __lt__(self, other):
        return self.duration < other.duration

    def subtract(self, duration):
        return Engagement(self.duty, self.duration - duration, self.engagement)


class Engagements:
    def __init__(self):
        self.duties = []

    def append_duty(self, duty):
        self.duties.append(Engagement(duty, duty.duration.seconds, duty.engagement))

    def empty(self):
        """(completed_duties, work_left, time_consumed)"""
        result = (
            [Engagement.duty for engagement in self.duties],
            0,
            {
                duty.duty.part_to: datetime.timedelta(seconds=duty.duration)
                for duty in self.duties
            },
            datetime.timedelta(0),
        )
        self.duties = []
        return result

    def __len__(self):
        return len(self.duties)

    def finish_next_duty(self):
        """(completed_duties, work_left, time_consumed)"""
        time_consumed = {duty.duty.part_to: 0 for duty in self.duties}
        self.duties.sort()
        if not self.duties:
            return [], 0, {}, datetime.timedelta(seconds=0)
        time_to_consume = self.duties[0].duration
        completed_duties = [self.duties[0].duty]
        self.duties = [duty.subtract(time_to_consume) for duty in self.duties[1:]]
        time_consumed = {
            key: datetime.timedelta(seconds=value + time_to_consume)
            for key, value in time_consumed.items()
        }
        return (
            completed_duties,
            0,
            time_consumed,
            datetime.timedelta(seconds=time_to_consume),
        )

    def execute_task(self, task):
        """(completed_duties, work_left, time_consumed)"""
        if not task.is_task():
            raise SystemError("Expected a TaskDefinition without engagement")
        time_consumed = {duty.duty.part_to: 0 for duty in self.duties}
        completed_duties = []
        active = sum([duty.engagement for duty in self.duties]) / 100.0
        work = task.duration.total_seconds()
        while work > 0 and len(self.duties) > 0:
            self.duties.sort()
            earliest = self.duties[0].duration
            time_to_consume = work + work * active
            if time_to_consume >= earliest:
                completed_duties.append(self.duties.pop(0).duty)
            if work >= time_to_consume:
                subtractable = time_to_consume
                work -= time_to_consume
            else:
                subtractable = work
                work = 0
            time_consumed = {
                key: value + subtractable for key, value in time_consumed.items()
            }
            self.duties = [
                engagement.subtract(subtractable) for engagement in self.duties
            ]
        return (
            completed_duties,
            work,
            {
                id: datetime.timedelta(seconds=count)
                for id, count in time_consumed.items()
            },
            task.duration,
        )


class CompletionResult:
    class DefinitionInfo:
        def __init__(self, parent, definition, duration_to_end):
            self._definition = definition
            self.duration_to_end = duration_to_end
            self.parent = parent

        def definition(self):
            return self._definition

        def till(self):
            return self.parent._total_duration - self.duration_to_end

    def __init__(self, result, total_duration):
        self._actions = [
            CompletionResult.DefinitionInfo(self, change["definition"], change["time"])
            for change in result
        ]
        self._total_duration = total_duration

    def actions(self):
        return self._actions

    def duration(self):
        if not self.actions():
            return datetime.timedelta(seconds=0)
        last = self.actions()[-1]
        return last.till() + last.definition().duration
        # return self._total_duration

    def ready_tasks(self):
        dependeds = [action.definition().depended for action in self._actions]
        return [
            action.definition()
            for action in self._actions
            if action.definition().is_task() and action.definition() not in dependeds
        ]


def calculate_completion(definitions):
    time_consumed = {task.part_to: datetime.timedelta(0) for task in definitions}
    on_time = datetime.timedelta()
    left = [
        definition
        for definition in definitions
        if definition.depended or definition.is_task()
    ]
    engagements = Engagements()
    [
        engagements.append_duty(definition)
        for definition in definitions
        if not definition.depended and not definition.is_task()
    ]
    result = []
    for definition in definitions:
        if definition.depended or not definition.is_task():
            continue
        completed_duties, work_left, consumed, time_later = engagements.execute_task(
            definition
        )
        on_time += time_later

        if definition in left:
            left.remove(definition)
        result.append({"definition": definition, "time": on_time})
        for completed in completed_duties:
            if completed in [entry["definition"] for entry in result]:
                continue
            result.append({"definition": completed, "time": on_time})
        for id, count in consumed.items():
            time_consumed[id] += count

    def next():
        dependeds = [
            task
            for task in left
            if task.depended not in left
            and task.depended not in [duty.duty for duty in engagements.duties]
        ]
        rankings = [
            key for key, value in sorted(time_consumed.items(), key=lambda x: x[1])
        ]
        found = None
        for ranking in rankings:
            for task in dependeds:
                if task.part_to == ranking:
                    found = task
        return found

    while left or len(engagements) > 0:
        definition = next()
        if definition:
            left.remove(definition)
            if not definition.is_task():
                engagements.append_duty(definition)
                continue
            completed_duties, work_left, consumed, time_taken = (
                engagements.execute_task(definition)
            )
            on_time += time_taken
            result.append({"definition": definition, "time": on_time})
        else:
            completed_duties, work_left, consumed, time_taken = (
                engagements.finish_next_duty()
            )
            on_time += time_taken
        for id, count in consumed.items():
            time_consumed[id] += count
        result.extend(
            [
                {"definition": duty, "time": on_time}
                for duty in completed_duties
                if duty not in [action["definition"] for action in result]
            ]
        )
    completed_duties, work_left, consumed, time_taken = engagements.empty()
    on_time += time_taken
    for id, count in consumed.items():
        time_consumed[id] += count
    result.reverse()
    return CompletionResult(result, on_time)


def order_definitions(definitions):
    return [
        information.definition()
        for information in calculate_completion(definitions).actions()
    ]


def next_work(run_state):
    full_state = run_state.full_state()
    if len(full_state[RunState.OPERATION_TEXTS[RunState.Operation.STAGED]]) < 1:
        return run_state
    started = full_state[RunState.OPERATION_TEXTS[RunState.Operation.STARTED]].copy()
    started.sort()
    staged = full_state[RunState.OPERATION_TEXTS[RunState.Operation.STAGED]].copy()
    staged.sort()
    if len([task for task in started if task.is_task()]) > 0:
        return run_state
    result = calculate_completion(staged + started)
    ready_tasks = result.ready_tasks()
    to_add = []
    if (
        not [definition for definition in started if definition.is_task()]
        and ready_tasks
    ):
        to_add.append(ready_tasks[0])
    if not to_add:
        return run_state
    return run_state.append_states(RunState.Operation.STARTED, to_add)


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
            return (datetime.timedelta(), engagements)
        earliest = min(engagements)
        engagements.remove(earliest)
        duration = earliest.duration * (earliest.engagement / 100.0)
        adjusted_engagements = []
        for engagement in engagements:
            current_duration = engagement.duration * engagement.engagement / 100
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
        engagements = engagements_in.copy()
        if not len(engagements):
            return engagements
        earliest = min(engagements)
        total_engagement = functools.reduce(
            lambda previous, current: previous + current.engagement,
            engagements,
            0,
        )
        done_duration = duration / (total_engagement / 100.0)
        return (
            done_duration,
            [
                EngagementSet(
                    engagement.task_id,
                    engagement.engagement,
                    engagement.duration - done_duration,
                )
                for engagement in engagements
            ],
        )


@functools.total_ordering
class TaskDefinition(models.Model):
    initial_duration = models.DurationField()
    part_to = models.ForeignKey("PartTo", on_delete=models.CASCADE)
    description = models.CharField(max_length=0x100)
    engagement = models.BigIntegerField(null=True)
    depended = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        unique_together = [("uuid")]
        indexes = [models.Index(fields=["uuid"])]

    @property
    def duration(self):
        return self.initial_duration

    @property
    def dependencies(self):
        part_tos = self.part_to.task_definitions
        result = set(filter(lambda o: o.depended == self, part_tos))
        return result

    def depended_chain_from(self, ommitted=set()):
        on = self
        while on:
            yield on
            on = on.depended

    def dependency_chain_from(self):
        queue = [self]

        def sort_queue():
            queue.sort(key=TaskDefinition.chain_duration, reverse=True)

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
                    EngagementSet(task.id, task.engagement, task.duration)
                )
            else:
                (consumed_duration, engagements) = task.consume_duration(engagements)
                duration += task.duration + consumed_duration
        if len(engagements):
            engagements.sort()
            duration += engagements[-1].duration
        return duration

    def duration_to(self):
        duration = datetime.timedelta(seconds=0)
        tasks = reversed(list(TaskDefinition.dependency_chain_from(self)))
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
        return self.engagement is None

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


class RunState(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        auto_now_add=True, editable=False, null=False, blank=False
    )

    class Meta:
        unique_together = [("uuid")]
        indexes = [models.Index(fields=["uuid", "created", "task"])]

    class Operation(models.IntegerChoices):
        STAGED = 1
        STARTED = 2
        COMPLETED = 3
        VOIDED = 4
        CREATED = 5

    OPERATION_TEXTS = [
        None,
        "staged",
        "started",
        "completed",
        "voided",
        "created",
    ]

    operation = models.IntegerField(choices=Operation)

    task = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)

    parent = models.ForeignKey("RunState", on_delete=models.CASCADE, null=True)

    def task_states(self):
        return RunState.objects.raw(
            """
            WITH RECURSIVE States AS (
                SELECT id , operation, task_id, parent_id, created
                FROM parttobe_runstate
                WHERE id = %s
                UNION ALL
                SELECT rs.id, rs.operation, rs.task_id, rs.parent_id, rs.created
                FROM parttobe_runstate rs
                JOIN States ss ON ss.parent_id = rs.id
            )
            SELECT id, MAX(task_id), operation
            FROM States
            GROUP BY task_id
            ORDER BY task_id;
        """,
            [self.id],
        )

    def full_chain(self):
        return RunState.objects.raw(
            """
            WITH RECURSIVE States AS (
                SELECT id , operation, task_id, parent_id
                FROM parttobe_runstate
                WHERE id = %s
                UNION ALL
                SELECT rs.id, rs.operation, rs.task_id, rs.parent_id
                FROM parttobe_runstate rs
                JOIN States ss ON ss.parent_id = rs.id
            )
            SELECT *
            FROM States
        """,
            [self.id],
        )

    def full_state(self):
        result = {
            "runState": self,
        } | {
            RunState.OPERATION_TEXTS[index]: []
            for index in range(1, len(RunState.OPERATION_TEXTS))
        }
        taskStates = self.task_states()

        order = order_definitions([state.task for state in taskStates])
        lookup = {state.task: state.operation for state in taskStates}
        result["startTimes"] = [
            {"task": state.task, "started": state.created}
            for state in taskStates
            if RunState.OPERATION_TEXTS[state.operation] == "started"
        ]
        for task in order:
            operation = lookup[task]
            result[RunState.OPERATION_TEXTS[operation]].append(task)
        active_tasks = result["staged"] + result["started"]
        seen_part_tos = set()
        for task in active_tasks:
            seen_part_tos.add(task.part_to)
        result["activePartTos"] = list(seen_part_tos)
        result["tasks"] = [task for task in result["started"] if task.is_task()]
        result["duties"] = [task for task in result["started"] if not task.is_task()]
        result["timestamp"] = self.created
        completion = calculate_completion(result["staged"] + result["started"])
        result["duration"] = completion.duration()
        result["imminent"] = self._imminent(completion, result["started"])
        return result

    def _imminent(self, completion, started):
        dependeds = set(
            [
                action.definition().depended
                for action in completion.actions()
                if action.definition().depended
            ]
        )
        ready_duties = [
            action
            for action in completion.actions()
            if action.definition() not in dependeds
            and not action.definition().is_task()
            and action.definition() not in started
        ]
        ready_duties.sort(key=lambda action: action.till())
        return [
            {
                "duty": duty.definition(),
                "till": duty.till(),
            }
            for duty in ready_duties
        ]

    def append_states(self, operation, tasks):
        if len(tasks) < 1:
            return self
        result = []
        parent = self
        for task in tasks:
            parent.save()
            parent = RunState(operation=operation, task=task, parent=parent)
            result.append(parent)
        parent.save()
        return parent


def append_states(operation, tasks, run_state=None):
    if len(tasks) < 1:
        return
    if run_state:
        return run_state.append_states(operation, tasks)
    return RunState(operation=operation, task=tasks[0]).append_states(
        operation, tasks[1:]
    )


class PartToRun(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        unique_together = [("uuid")]
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
            run=self, started__isnull=False, ended__isnull=True
        )
        return map(lambda task: task.definition, started)

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
        started = TaskStatus.objects.filter(run=self.id, started__isnull=False)
        return map(lambda task: task.definition, started)

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
        return until if until > datetime.timedelta() else datetime.timedelta()

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
        if next_duty_time is not None and next_duty_time <= datetime.timedelta():
            return TaskStatus.objects.create(run=self, definition=duties[0])
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
            return TaskStatus.objects.create(run=self, definition=duties[0])
        return TaskStatus.objects.create(run=self, definition=left[0])


class TaskStatus(models.Model):
    run = models.ForeignKey("PartToRun", on_delete=models.CASCADE)
    definition = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)
    started = models.DateTimeField(default=datetime.datetime.now)
    ended = models.DateTimeField(null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        unique_together = [("uuid")]
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
