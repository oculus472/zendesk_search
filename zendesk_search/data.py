import json
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from typing import Type


class DataProvider(ABC):
    @abstractmethod
    def get_all(self):
        pass


class ZendeskDataProvider(DataProvider):
    def __init__(self, resource):
        self.filepath = (
            Path(__file__).resolve().parent.parent / "data" / f"{resource}.json"
        )

    def get_all(self) -> list[dict]:
        with open(self.filepath) as f:
            return json.load(f)


class Backend(ABC):
    def __init__(self):
        self.users = self.provider("users")
        self.tickets = self.provider("tickets")
        self.organizations = self.provider("organizations")

    @abstractproperty
    def provider(self) -> Type[DataProvider]:
        pass


class ZendeskBackend(Backend):
    provider = ZendeskDataProvider


def get_backend(config=None) -> Backend:
    return ZendeskBackend()
