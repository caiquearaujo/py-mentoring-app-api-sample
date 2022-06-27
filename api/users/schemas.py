import dataclasses
import datetime
from email.policy import default
from typing import TYPE_CHECKING
from xmlrpc.client import DateTime
from marshmallow import Schema, fields, validate

from .models import User, UserStatus

if TYPE_CHECKING:
    from .models import User


@dataclasses.dataclass
class UserData:
    id: int = None
    first_name: str = None
    last_name: str = None
    email: str = None
    location: str = None
    employer: str = None
    title: str = None
    status: str = UserStatus.CREATED.value
    password: str = None
    date_joined: DateTime = datetime.datetime.utcnow()
    last_login: DateTime = None

    @classmethod
    def from_instance(self, user: "User") -> "UserData":
        return self(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            location=user.location,
            employer=user.employer,
            title=user.title,
            status=user.status,
            date_joined=user.date_joined,
            last_login=user.last_login,
        )


class UserSchema(Schema):
    id = fields.Integer(dump_only=True, default=None)
    first_name = fields.Str(validate=validate.Length(max=150), required=True)
    last_name = fields.Str(validate=validate.Length(max=150), required=True)
    email = fields.Email(validate=validate.Length(max=150), required=True)
    location = fields.Str(validate=validate.Length(max=150), default=None)
    employer = fields.Str(validate=validate.Length(max=150), default=None)
    title = fields.Str(validate=validate.Length(max=150), default=None)
    status = fields.Str(
        validate=validate.OneOf([member.value for member in UserStatus]),
        default=UserStatus.CREATED.value,
    )

    date_joined = fields.DateTime(dump_only=True, default=datetime.datetime.utcnow())
    last_login = fields.DateTime(dump_only=True, default=None)


class ProfileUpdateSchema(Schema):
    first_name = fields.Str(validate=validate.Length(max=150), required=True)
    last_name = fields.Str(validate=validate.Length(max=150), required=True)
    location = fields.Str(validate=validate.Length(max=150), default=None)
    employer = fields.Str(validate=validate.Length(max=150), default=None)
    title = fields.Str(validate=validate.Length(max=150), default=None)


class OldAndNewDataSchema(Schema):
    old = fields.Str(required=True)
    new = fields.Str(required=True)


class AccountUpdateSchema(Schema):
    email = fields.Nested(OldAndNewDataSchema)
    password = fields.Nested(OldAndNewDataSchema)


class LoginSchema(Schema):
    email = fields.Email(validate=validate.Length(max=150), required=True)
    password = fields.Str(required=True, load_only=True, default=None)


class ProfileCreateSchema(ProfileUpdateSchema, LoginSchema):
    pass
