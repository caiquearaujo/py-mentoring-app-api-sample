import dataclasses
import datetime
from typing import TYPE_CHECKING

import core.jwt as jwt
from .models import User
from . import schemas

if TYPE_CHECKING:
    from .models import User


def create_new_account(user: "schemas.UserData") -> "schemas.UserData":
    instance = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        location=user.location,
        employer=user.employer,
        title=user.title,
    )

    if user.password is not None:
        instance.set_password(user.password)

    instance.save()
    return schemas.UserData.from_instance(instance)


def update_account(user: "User", **update) -> "schemas.UserData":
    user.first_name = update.get("first_name", user.first_name)
    user.last_name = update.get("last_name", user.last_name)
    user.email = update.get("email", user.email)
    user.location = update.get("location", user.location)
    user.employer = update.get("employer", user.employer)
    user.title = update.get("title", user.title)
    user.status = update.get("status", user.status)

    if update.get("password"):
        user.set_password(user.password)

    user.save()
    return schemas.UserData.from_instance(user)


def find_by_email(email: str) -> "User":
    return User.objects.filter(email=email).first()


def create_token(id: int) -> str:
    return jwt.encode(id)
