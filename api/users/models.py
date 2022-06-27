from typing import List

from django.contrib.auth.hashers import make_password
from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from metadata.models import Metadata

from .enums import UserRole


class UserManager(auth_models.UserManager):
    use_in_migrations = False

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given data.
        """
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("location", None)
        extra_fields.setdefault("employer", None)
        extra_fields.setdefault("title", None)
        extra_fields.setdefault("status", UserStatus.CREATED)
        extra_fields.setdefault("role", UserRole.ANONYMOUS.value)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if not email:
            raise ValueError("User must have an email address")

        if not extra_fields.get("first_name"):
            raise ValueError("User must have a first name")

        if not extra_fields.get("last_name"):
            raise ValueError("User must have a last name")

        if extra_fields.get("role") not in [member.value for member in UserRole]:
            raise ValueError("Role must be a valid data")

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("location", None)
        extra_fields.setdefault("employer", None)
        extra_fields.setdefault("title", None)
        extra_fields.setdefault("status", UserStatus.CREATED.value)
        extra_fields.setdefault("role", UserRole.ANONYMOUS.value)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not email:
            raise ValueError("User must have an email address")

        if not extra_fields.get("first_name"):
            raise ValueError("User must have a first name")

        if not extra_fields.get("last_name"):
            raise ValueError("User must have a last name")

        if extra_fields.get("role") not in [member.value for member in UserRole]:
            raise ValueError("Role must be a valid data")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class UserStatus(models.IntegerChoices):
    CREATED = 1, _("Created")
    PENDING = 2, _("Pending")
    APPROVED = 3, _("Approved")


class User(auth_models.AbstractUser):
    username = None

    first_name = models.CharField(
        _("first name"),
        blank=False,
        max_length=150,
    )

    last_name = models.CharField(
        _("last name"),
        blank=False,
        max_length=150,
    )

    location = models.CharField(
        _("location"),
        max_length=150,
        blank=False,
        null=True,
    )

    employer = models.CharField(
        _("employer"),
        max_length=150,
        blank=False,
        null=True,
    )

    title = models.CharField(
        _("title"),
        max_length=150,
        blank=False,
        null=True,
    )
    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True,
    )

    password = models.CharField(
        max_length=255,
    )

    status = models.CharField(
        max_length=10,
        choices=UserStatus.choices,
        default=UserStatus.CREATED.value,
        db_index=True,
    )

    role = models.CharField(
        max_length=10,
        choices=UserRole.choices(),
        default=UserRole.ANONYMOUS.value,
        db_index=True,
    )

    metadata = models.ManyToManyField(
        Metadata,
        verbose_name=_("Metadata"),
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )

    available_time = models.JSONField(
        blank=True,
        null=True,
    )

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"
        constraints = [
            models.CheckConstraint(
                check=models.Q(status__in=UserStatus.values),
                name="valid_user_status",
            )
        ]
