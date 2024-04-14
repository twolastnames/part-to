from django.db import models


class PartTo(models.Model):
    name = models.CharField(max_length=0x80)


class PartToTaskDefinition(models.Model):
    part_to = models.ForeignKey("PartTo", on_delete=models.CASCADE)
    depend = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)


class IngredientDefinition(models.Model):
    name = models.CharField(max_length=0x80)
    task = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)


class ToolDefinition(models.Model):
    name = models.CharField(max_length=0x40)
    task = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)


class TaskDefinition(models.Model):
    duration = models.DurationField()
    part_to = models.ForeignKey("PartTo", on_delete=models.CASCADE)
    description = models.CharField(max_length=0x100)
    engagement = models.BigIntegerField(null=True)
    depended = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE, null=True)
