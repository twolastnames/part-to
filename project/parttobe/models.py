from django.db import models
from django.db import connection
from parttobe.timeline import Definition
from parttobe.timeline import Timeline
import functools
import collections
import types
import datetime
import uuid
import re
from parttobe.common import common_repr


class WrongDefinitionType(RuntimeError):
    pass


class ImproperRunStateSequence(RuntimeError):
    pass


@functools.lru_cache(maxsize=64)
def get_task_definitions(part_to):
    return set(TaskDefinition.objects.filter(part_to=part_to))


class PartTo(models.Model):
    name = models.CharField(max_length=0x80)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        unique_together = [("uuid")]
        indexes = [models.Index(fields=["uuid"])]

    @staticmethod
    def displayables():
        return (
            PartTo.objects.annotate(
                newest_ones=models.Window(
                    expression=models.Max("id"),
                    partition_by=[models.F("name")],
                )
            )
            .filter(newest_ones=models.F("id"))
            .order_by("name")
        )

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


@functools.total_ordering
class CompletionAction(
    collections.namedtuple("CompletionAction", "definition till duration")
):
    def __eq__(self, other):
        return other.till == other.till

    def __lt__(self, other):
        return self.till < other.till


class CompletionResult:
    def __init__(self, timeline):
        starts = {marker.id: marker.till for marker in timeline if not marker.is_done}
        self.result = [
            CompletionAction(
                marker.id, starts[marker.id], marker.till - starts[marker.id]
            )
            for marker in timeline
            if marker.is_done
        ]
        self.result.sort()

    def actions(self):
        return self.result

    def duration(self):
        last = datetime.timedelta(seconds=0)
        for action in self.result:
            if action.till + action.duration > last:
                last = action.till + action.duration
        return last

    def ready_tasks(self):
        depended_definitions = [action.definition.dependeds for action in self.result]
        dependeds = sum(depended_definitions, [])
        return [
            action.definition
            for action in self.result
            if action.definition.is_task() and action.definition not in dependeds
        ]


def calculate_completion(definitions, at_time=datetime.datetime.now()):
    calculated_durations = calculate_durations(definitions, at_time)
    for definition in definitions:
        definition.set_calculated_duration(calculated_durations[definition.id])
    timeline = Timeline(definitions)
    return CompletionResult(timeline)

def order_definitions(definitions):
    return [
        information.definition
        for information in calculate_completion(definitions).actions()
    ]


def next_work(run_state):
    full_state = run_state.full_state()
    if len(full_state[RunState.OPERATION_TEXTS[RunState.Operation.STAGED]]) < 1:
        return run_state
    started = full_state[RunState.OPERATION_TEXTS[RunState.Operation.STARTED]].copy()
    staged = full_state[RunState.OPERATION_TEXTS[RunState.Operation.STAGED]].copy()
    if len([task for task in started if task.is_task()]) > 0:
        return run_state
    result = calculate_completion(staged + started, full_state["timestamp"])
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

class Dependent(models.Model):
    depended = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE, related_name='dependent_taskdefinition_depended')
    dependency = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE, related_name='dependent_taskdefinition_dependency')

    class Meta:
        unique_together = [("depended", "dependency")]
        indexes = [models.Index(fields=["depended"]), models.Index(fields=["dependency"])]

@functools.total_ordering
class TaskDefinition(models.Model):
    initial_duration = models.DurationField()
    part_to = models.ForeignKey("PartTo", on_delete=models.CASCADE)
    description = models.CharField(max_length=0x100)
    engagement = models.BigIntegerField(null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        unique_together = [("uuid")]
        indexes = [models.Index(fields=["uuid"])]

    @property
    def duration(self):
        if hasattr(self, "calculated_duration"):
            return self.calculated_duration
        return self.initial_duration

    def __repr__(self):
        return common_repr(self, "id", "duration", "description", "engagement")

    def set_calculated_duration(self, calculated):
        self.calculated_duration = calculated

    @property
    def dependeds(self):
        return [dependency.depended for dependency in Dependent.objects.filter(dependency=self)]

    @property
    def dependencies(self):
        return [dependent.dependency for dependent in Dependent.objects.filter(depended=self)]

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

    def task_duration(self):
        if not self.task:
            raise WrongDefinitionType()
        if not self.task.is_task():
            raise WrongDefinitionType(
                "definition {} is not a task".format(self.task.id)
            )
        if self.operation != self.Operation.COMPLETED:
            raise WrongDefinitionType(
                "task {} is not a completed task".format(self.task.id)
            )
        active_duties = set()
        result = 0.0
        on_time = None
        for state in reversed(self.full_chain()):
            if on_time and (
                state.operation == self.Operation.STARTED
                or state.operation == self.Operation.COMPLETED
            ):
                elapsed = state.created.timestamp() - on_time.timestamp()
                engagement = sum([(duty.engagement / 100.0) for duty in active_duties])
                result = result + (elapsed * (1.0 - engagement))
            if on_time and state == self:
                return datetime.timedelta(seconds=result)
            if on_time or (
                state.task == self.task and state.operation == self.Operation.STARTED
            ):
                on_time = state.created
            if state.task.is_task():
                continue
            if state.operation == self.Operation.STARTED:
                active_duties.add(state.task)
            if state.operation == self.Operation.COMPLETED:
                active_duties.remove(state.task)
        return self.task.duration

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
        task_states = self.task_states()

        result["tasks"] = []
        result["duties"] = []
        order = order_definitions([state.task for state in task_states])
        lookup = {state.task: state.operation for state in task_states}
        for task in order:
            operation = lookup[task]
            result[RunState.OPERATION_TEXTS[operation]].append(task)
            result["tasks" if task.is_task() else "duties"].append(task)
        active_tasks = result["staged"] + result["started"]
        seen_part_tos = set()
        for task in active_tasks:
            seen_part_tos.add(task.part_to)
        result["activePartTos"] = list(seen_part_tos)
        result["timestamp"] = self.created
        completion = calculate_completion(active_tasks, self.created)
        completion_durations = {
            action.definition: action.duration for action in completion.actions()
        }
        result["upcoming"] = [
            {
                "till": action.till,
                "task": action.definition,
                "duration": action.duration,
            }
            for action in completion.actions()
        ]
        result["duration"] = completion.duration()
        timers = [
            {
                "task": state.task,
                "started": state.created,
                "duration": completion_durations[state.task],
            }
            for state in task_states
            if RunState.OPERATION_TEXTS[state.operation] == "started"
        ]
        result["timers"] = {
            "enforced": [timer for timer in timers if not timer["task"].is_task()],
            "laxed": [timer for timer in timers if timer["task"].is_task()],
            "imminent": self._imminent(completion, result["started"]),
        }
        return result

    def _imminent(self, completion, started):
        dependeds = set(
            sum([
                action.definition.dependeds
                for action in completion.actions()
                if action.definition.dependeds
            ],[])
        )
        ready_duties = [
            action
            for action in completion.actions()
            if action.definition not in dependeds
            and not action.definition.is_task()
            and action.definition not in started
        ]
        ready_duties.sort(key=lambda action: action.till)
        return [
            {
                "task": duty.definition,
                "till": duty.till,
            }
            for duty in ready_duties
        ]

    def append_states(self, operation, tasks):
        return append_states(operation, tasks, self)


def append_states(operation, tasks, run_state=None):
    if len(tasks) < 1:
        return run_state
    inserts = ["({}, %s, %s, %s, %s)".format("%s" if run_state else "NULL")] + [
        "(LAST_INSERT_ROWID(), %s, %s, %s,  %s)"
    ] * (len(tasks) - 1)
    columns = "(parent_id, uuid, created, task_id, operation)"
    table = "parttobe_runstate"

    statement = "INSERT INTO {} {} VALUES {};".format(table, columns, ",".join(inserts))

    uuids = [uuid.uuid4() for ignored in tasks]
    last_uuid = uuids[0]

    values = ([run_state.id] if run_state else []) + sum(
        [
            [
                str(uuids.pop()).replace("-", ""),
                datetime.datetime.now(),
                id,
                operation,
            ]
            for id in [task.id for task in tasks]
        ],
        [],
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(statement, values)
        finally:
            cursor.close()
            return RunState.objects.get(uuid=last_uuid)


def calculate_duty_durations(definitions, before):
    if not definitions:
        return {}
    tasks = [definition for definition in definitions if not definition.is_task()]
    statement = " UNION ALL ".join(
        [
            """
    select * from (
        WITH Durations AS (
        WITH Paired AS (
            WITH RECURSIVE Times AS (
                WITH Completeds AS (
                    SELECT 
                        id,
                        operation,
                        task_id,
                        parent_id,
                        created
                    FROM parttobe_runstate
                    WHERE operation = %s
                    AND task_id = %s
                    AND created <= %s
                    LIMIT 5
                )
                SELECT
                    id,
                    Completeds.id AS completedId,
                    operation,
                    task_id,
                    parent_id,
                    created
                FROM Completeds
                WHERE id = Completeds.id
                UNION ALL
                SELECT
                    rs.id,
                    completedId,
                    rs.operation,
                    rs.task_id,
                    rs.parent_id,
                    rs.created
                FROM parttobe_runstate rs
                JOIN Times ss ON ss.parent_id = rs.id
            )
            SELECT 
                id,
                completedId,
                task_id,
                created,
                operation
            FROM Times t1
            WHERE operation = %s OR operation = %s
        )
        SELECT p1.task_id AS task, ((    
            JULIANDAY(p1.created) - JULIANDAY(p2.created)
        ) * 24 * 60 * 60) AS duration  FROM Paired p1
        INNER JOIN Paired p2
        ON p2.completedId = p1.completedId
        AND p1.operation > p2.operation
        UNION ALL
        SELECT u1.id AS task, (u1.initial_duration / 1000000) AS duration
        FROM parttobe_taskdefinition u1
        WHERE id = %s
        LIMIT 5        
        )
        SELECT task, AVG(duration)
        FROM Durations
        GROUP BY task
        )
    """
        ]
        * len(tasks)
    )

    values = []
    for task in tasks:
        values.extend(
            [
                RunState.Operation.COMPLETED,
                task.id,
                before,
                RunState.Operation.COMPLETED,
                RunState.Operation.STARTED,
                task.id,
            ]
        )
    with connection.cursor() as cursor:
        exectued = cursor.execute(statement, values)
        query_result = exectued.fetchall()
    return {row[0]: datetime.timedelta(seconds=round(row[1])) for row in query_result}


def calculate_task_durations(definitions, before):
    tasks = [definition for definition in definitions if definition.is_task()]
    result = {}
    for task in tasks:
        completions = RunState.objects.filter(
            task=task, operation=RunState.Operation.COMPLETED, created__lt=before
        )[:5]
        observeds = [completion.task_duration().seconds for completion in completions]
        results = (
            observeds if len(observeds) > 4 else observeds + [task.duration.seconds]
        )
        result[task.id] = datetime.timedelta(seconds=sum(results) / len(results))
    return result


def calculate_durations(definitions, before):
    task_durations = calculate_task_durations(definitions, before)
    duty_durations = calculate_duty_durations(definitions, before)
    return task_durations | duty_durations
