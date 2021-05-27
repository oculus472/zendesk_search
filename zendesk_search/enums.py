from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def values(cls):
        return [e.value for e in cls]
