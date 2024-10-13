from django.db import models

class UuidedModel:
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        unique_together = [("uuid")]
        indexes = [models.Index(fields=["uuid"])]
