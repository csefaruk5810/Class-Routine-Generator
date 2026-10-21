from django.db import models

from apps.common.models import ActivatableModel, TimeStampedModel


class RoomType(models.TextChoices):
    CLASSROOM = "CLASSROOM", "Classroom"
    LAB = "LAB", "Lab"
    PROJECT_ROOM = "PROJECT_ROOM", "Project Room"
    OTHER = "OTHER", "Other"


class Room(TimeStampedModel, ActivatableModel):
    department = models.ForeignKey("academics.Department", on_delete=models.CASCADE, related_name="rooms")
    code = models.CharField(max_length=64)
    room_type = models.CharField(max_length=32, choices=RoomType.choices, default=RoomType.CLASSROOM)
    capacity = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = [("department", "code")]
        ordering = ["code"]


class SchedulingConfiguration(TimeStampedModel, ActivatableModel):
    department = models.ForeignKey("academics.Department", on_delete=models.CASCADE, related_name="configurations")
    academic_session = models.ForeignKey(
        "academics.AcademicSession",
        on_delete=models.CASCADE,
        related_name="configurations",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=128)
    source_filename = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = [("department", "name")]


class DayDefinition(TimeStampedModel):
    configuration = models.ForeignKey(SchedulingConfiguration, on_delete=models.CASCADE, related_name="days")
    name = models.CharField(max_length=32)
    order_index = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = [("configuration", "name")]
        ordering = ["order_index", "id"]


class TimeSlotType(models.TextChoices):
    THEORY = "THEORY", "Theory"
    LAB = "LAB", "Lab"
    FLEX = "FLEX", "Flex"


class TimeSlot(TimeStampedModel):
    configuration = models.ForeignKey(SchedulingConfiguration, on_delete=models.CASCADE, related_name="time_slots")
    day = models.ForeignKey(DayDefinition, on_delete=models.CASCADE, related_name="time_slots")
    slot_type = models.CharField(max_length=16, choices=TimeSlotType.choices, default=TimeSlotType.FLEX)
    start_time = models.TimeField()
    end_time = models.TimeField()
    label = models.CharField(max_length=64)
    duration_minutes = models.PositiveIntegerField()

    class Meta:
        unique_together = [("configuration", "day", "start_time", "end_time", "slot_type")]
        ordering = ["day__order_index", "start_time", "end_time"]


class TeacherAvailabilityRule(TimeStampedModel):
    teacher = models.ForeignKey("academics.Teacher", on_delete=models.CASCADE, related_name="availability_rules")
    day_name = models.CharField(max_length=32)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_available = models.BooleanField(default=False)


class ConstraintWeight(TimeStampedModel):
    department = models.ForeignKey("academics.Department", on_delete=models.CASCADE, related_name="constraint_weights")
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    weight = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = [("department", "name")]

