from multiprocessing.sharedctypes import Value
from django.db import models
from django.contrib.auth import models as auth_models


class UserManager(auth_models.BaseUserManager):
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email=str,
        password: str = None,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> "User":
        if not email:
            raise ValueError("User must have an email address")

        if not first_name:
            raise ValueError("User must have a first name")

        if not last_name:
            raise ValueError("User must have a last name")

        user: User = self.model(email=self.normalize_email(email))

        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.save()
        return user

    def create_superuser(
        self,
        first_name: str,
        last_name: str,
        email=str,
        password: str = None,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> "User":
        return self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=is_staff,
            is_superuser=True,
        )


class User(auth_models.AbstractUser):
    username = None

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    location = models.CharField(_("location"), max_length=150, black=True)
    employer = models.CharField(_("employer"), max_length=150, blank=True)
    title = models.CharField(_("title"), max_length=150, blank=True)
    expertise = models.CharField(_("expertise"), max_length=150, blank=True)
    type = models.CharField(_("type"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    email = models.EmailField(_("email address"), blank=False, unique=True)

    password = models.CharField(max_length=255)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = ["first_name", "last_name"]
