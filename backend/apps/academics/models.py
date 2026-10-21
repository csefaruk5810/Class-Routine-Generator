from django.db import models

from apps.common.models import ActivatableModel, TimeStampedModel


class Department(TimeStampedModel, ActivatableModel):
    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:
        return self.code


class AcademicSession(TimeStampedModel, ActivatableModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="sessions")
    name = models.CharField(max_length=64)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [("department", "name")]
        ordering = ["-start_year", "name"]


class Semester(TimeStampedModel, ActivatableModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="semesters")
    name = models.CharField(max_length=64)
    year_label = models.CharField(max_length=32)
    term_label = models.CharField(max_length=32)
    ordinal = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [("department", "name")]
        ordering = ["ordinal", "name"]


class Section(TimeStampedModel, ActivatableModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="sections")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=16)
    capacity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [("semester", "name")]
        ordering = ["semester__ordinal", "name"]


class Teacher(TimeStampedModel, ActivatableModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="teachers")
    employee_id = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=128, blank=True)
    seniority_level = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = [("department", "employee_id")]
        ordering = ["name"]


class CourseType(models.TextChoices):
    THEORY = "THEORY", "Theory"
    LAB = "LAB", "Lab"
    PROJECT = "PROJECT", "Project"


class Course(TimeStampedModel, ActivatableModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=255)
    course_type = models.CharField(max_length=16, choices=CourseType.choices)
    credit = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    default_duration_minutes = models.PositiveIntegerField(default=50)

    class Meta:
        unique_together = [("department", "code")]
        ordering = ["code"]


class CourseOffering(TimeStampedModel, ActivatableModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="offerings")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="course_offerings")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="course_offerings")
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name="course_offerings")
    weekly_frequency = models.PositiveSmallIntegerField(default=1)
    duration_minutes = models.PositiveIntegerField()
    required_room_type = models.CharField(max_length=32, blank=True)
    allow_split_across_days = models.BooleanField(default=True)
    composite_group_code = models.CharField(max_length=64, blank=True)

    class Meta:
        unique_together = [("course", "section", "session")]


class CourseOfferingTeacher(TimeStampedModel):
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name="teacher_assignments")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="course_offerings")
    is_primary = models.BooleanField(default=True)

    class Meta:
        unique_together = [("course_offering", "teacher")]

