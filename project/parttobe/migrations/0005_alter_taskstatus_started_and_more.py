# Generated by Django 5.0.3 on 2024-10-24 23:21

import datetime
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "parttobe",
            "0004_parttorun_runpart_taskstatus_partto_uuid_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskstatus",
            name="started",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterUniqueTogether(
            name="partto",
            unique_together={("uuid",)},
        ),
        migrations.AlterUniqueTogether(
            name="parttorun",
            unique_together={("uuid",)},
        ),
        migrations.AlterUniqueTogether(
            name="taskdefinition",
            unique_together={("uuid",)},
        ),
        migrations.AlterUniqueTogether(
            name="taskstatus",
            unique_together={("uuid",)},
        ),
        migrations.CreateModel(
            name="RunState",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "operation",
                    models.IntegerField(
                        choices=[
                            ("Staged", 1),
                            ("Started", 2),
                            ("Completed", 3),
                            ("Voided", 4),
                        ]
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="parttobe.runstate",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="parttobe.taskdefinition",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["uuid"],
                        name="parttobe_ru_uuid_21b900_idx",
                    )
                ],
                "unique_together": {("uuid",)},
            },
        ),
    ]
