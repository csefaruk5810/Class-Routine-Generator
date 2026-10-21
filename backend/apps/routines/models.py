from django.db import models

from apps.common.models import TimeStampedModel


class RoutineStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    GENERATED = "GENERATED", "Generated"
    ACTIVE = "ACTIVE", "Active"
    ARCHIVED = "ARCHIVED", "Archived"
    INVALID = "INVALID", "Invalid"


class RoutineVersion(TimeStampedModel):
    configuration = models.ForeignKey("resources.SchedulingConfiguration", on_delete=models.CASCADE, related_name="routine_versions")
    section = models.ForeignKey("academics.Section", on_delete=models.CASCADE, related_name="routine_versions")
    status = models.CharField(max_length=16, choices=RoutineStatus.choices, default=RoutineStatus.DRAFT)
    solver_status = models.CharField(max_length=64, blank=True)
    objective_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    hard_violation_count = models.PositiveIntegerField(default=0)
    soft_penalty = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]


class RoutineAssignment(TimeStampedModel):
    routine_version = models.ForeignKey(RoutineVersion, on_delete=models.CASCADE, related_name="assignments")
    course_offering = models.ForeignKey("academics.CourseOffering", on_delete=models.CASCADE, related_name="routine_assignments")
    teacher = models.ForeignKey("academics.Teacher", on_delete=models.CASCADE, related_name="routine_assignments")
    room = models.ForeignKey("resources.Room", on_delete=models.SET_NULL, related_name="routine_assignments", null=True, blank=True)
    day = models.ForeignKey("resources.DayDefinition", on_delete=models.CASCADE, related_name="routine_assignments")
    time_slot = models.ForeignKey("resources.TimeSlot", on_delete=models.CASCADE, related_name="routine_assignments")
    start_time = models.TimeField()
    end_time = models.TimeField()
    source = models.CharField(max_length=32, default="GENERATED")


class ValidationSnapshot(TimeStampedModel):
    routine_version = models.ForeignKey(RoutineVersion, on_delete=models.CASCADE, related_name="validation_snapshots")
    is_valid = models.BooleanField(default=True)
    errors = models.JSONField(default=list, blank=True)
    warnings = models.JSONField(default=list, blank=True)
    soft_penalty = models.IntegerField(default=0)

