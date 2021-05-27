from typing import Mapping, Type

from .data import Backend, get_backend
from .models import Organization, Ticket, User, ZendeskModel

_resource_to_model_map: Mapping[str, Type[ZendeskModel]] = {
    "users": User,
    "tickets": Ticket,
    "organizations": Organization,
}
all_resources = tuple(_resource_to_model_map)


def get_field_choices_for_resource(resource: str) -> list[str]:
    return _resource_to_model_map[resource].get_searchable_fields()


def list_search_fields() -> None:
    # TODO: https://pypi.org/project/tabulate/
    for _, model in _resource_to_model_map.items():
        print(f"Search {model.__name__}s with")
        print(*model.get_searchable_fields(), sep="\n")
        print("-" * 15)


def search_zendesk(backend: Backend = None):
    if not backend:
        backend = get_backend()
