from typing import Mapping, Type

from tabulate import tabulate

from .data import Backend, get_backend
from .models import Organization, Ticket, User, ZendeskModel

_resource_to_model_map: Mapping[str, Type[ZendeskModel]] = {
    "users": User,
    "tickets": Ticket,
    "organizations": Organization,
}
all_resources = tuple(_resource_to_model_map)


def get_field_choices_for_resource(resource: str, sort=True) -> list[str]:
    """Get searchable fields for the supplied resource.

    Args:
        resource (str): Name of the resource.

    Returns:
        list[str]: List of searchable fields.
    """
    return _resource_to_model_map[resource].get_searchable_fields(sort)


def list_search_fields() -> None:
    """Print searchable fields to the console for all Zendesk models."""
    table = {
        model.__name__: model.get_searchable_fields()
        for _, model in _resource_to_model_map.items()
    }
    print(tabulate(table, headers="keys", tablefmt="psql"))


def search_zendesk(backend: Backend = None):
    """Search for the specified value."""
    if not backend:
        backend = get_backend()
