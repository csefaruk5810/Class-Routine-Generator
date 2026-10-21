from django.db import models

from apps.common.models import TimeStampedModel


class ImportStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    VALIDATED = "VALIDATED", "Validated"
    IMPORTED = "IMPORTED", "Imported"
    FAILED = "FAILED", "Failed"


class ImportJob(TimeStampedModel):
    department = models.ForeignKey("academics.Department", on_delete=models.CASCADE, related_name="import_jobs")
    configuration = models.ForeignKey(
        "resources.SchedulingConfiguration",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="import_jobs",
    )
    filename = models.CharField(max_length=255)
    payload_hash = models.CharField(max_length=128, blank=True)
    status = models.CharField(max_length=16, choices=ImportStatus.choices, default=ImportStatus.PENDING)
    raw_payload = models.JSONField(default=dict, blank=True)
    preview_data = models.JSONField(default=dict, blank=True)
    errors = models.JSONField(default=list, blank=True)
    warnings = models.JSONField(default=list, blank=True)

