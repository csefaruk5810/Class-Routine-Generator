from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import ActivatableModel, TimeStampedModel


class UserRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    DEPARTMENT_ADMIN = "DEPARTMENT_ADMIN", "Department Admin"
    TEACHER = "TEACHER", "Teacher"
    STUDENT = "STUDENT", "Student"


class User(AbstractUser, TimeStampedModel, ActivatableModel):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, choices=UserRole.choices, default=UserRole.DEPARTMENT_ADMIN)
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

