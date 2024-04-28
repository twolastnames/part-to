from django.db import models
import functools
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


class PartToTaskDefinition(models.Model):
    part_to = models.ForeignKey("PartTo", on_delete=models.CASCADE)
    depend = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)


class IngredientDefinition(models.Model):
    name = models.CharField(max_length=0x80)
    task = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)


class ToolDefinition(models.Model):
    name = models.CharField(max_length=0x40)
    task = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)


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
    def chain_duration(start):
        duration = datetime.timedelta(seconds=0)
        for model in TaskDefinition.depended_chain_from(start):
            duration += model.duration
        return duration

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
        *_, first = self.depended_chain_from(other)
        seen_self = False
        for model in self.dependency_chain_from(first):
            if model == self:
                seen_self = True
            elif model == other:
                return not seen_self
        raise Exception("self and other do not connect")


# TODO: introduce this model
# class PartToRun(models.Model):
#    part_to = models.ForeignKey("PartTo", on_delete=models.CASCADE)


# TODO: introduce this model
# class TaskStatus(models.Model):
#    part_to = models.ForeignKey("PartToRun", on_delete=models.CASCADE)
#    definition = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)
#    started = models.DateTimeField()
#    ended = models.DateTimeField(null=True)
