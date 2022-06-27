from enum import Enum


class UserRole(Enum):
    MEMBER = "member"
    MENTOR = "mentor"
    INTERNAL = "internal"
    ANONYMOUS = "anonymous"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
