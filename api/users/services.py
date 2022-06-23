import dataclasses
import datetime
from typing import TYPE_CHECKING

import core.jwt as jwt
from .enums import UserStatus
from .models import User

if TYPE_CHECKING:
    from .models import User


@dataclasses.dataclass
class UserDataClass:
    id: int = None
    first_name: str = None
    last_name: str = None
    email: str = None
    location: str = None
    employer: str = None
    title: str = None
    status: str = UserStatus.CREATED.value
    password: str = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            location=user.location,
            employer=user.employer,
            title=user.title,
            status=user.status,
        )


def create_user(user: "UserDataClass") -> "UserDataClass":
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
    return UserDataClass.from_instance(instance)


def find_by_email(email: str) -> "User":
    user = User.objects.filter(email=email).first()
    return user


def create_token(id: int) -> str:
    return jwt.encode(id)
