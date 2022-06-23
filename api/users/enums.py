from enum import Enum


class UserStatus(Enum):
    CREATED = "created"
    PENDING = "pending"
    APPROVED = "approved"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
