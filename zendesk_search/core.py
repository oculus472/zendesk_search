import json
from pathlib import Path
from typing import Iterable, Mapping, Type

from tabulate import tabulate

from .logger import get_logger
from .models import Organization, Ticket, User, ZendeskModel

logger = get_logger()

collection_name_to_model_map: Mapping[str, Type[ZendeskModel]] = {
    "users": User,
    "tickets": Ticket,
    "organizations": Organization,
}
all_collection_names = tuple(collection_name_to_model_map)


def get_collection_data(collection_name: str) -> Iterable[dict]:
    filepath = (
        Path(__file__).resolve().parent.parent / "data" / f"{collection_name}.json"
    )
    with open(filepath, "r") as content:
        return json.load(content)


def get_field_choices_for_collection(collection_name: str, sort=True) -> Iterable[str]:
    """Get searchable fields for the supplied collection.

    Args:
        collection_name (str): Name of the collection.

    Returns:
        list[str]: List of searchable fields.
    """
    return collection_name_to_model_map[collection_name].get_searchable_fields(sort)


def list_search_fields() -> None:
    """Print searchable fields to the console for all Zendesk models."""
    table = {
        model.__name__: model.get_searchable_fields()
        for _, model in collection_name_to_model_map.items()
    }
    print(tabulate(table, headers="keys", tablefmt="psql"))


def search_zendesk(*args, collection="", field="", value=""):
    """Search for the specified value."""
    # get the collection
    # results = collection.filter(fields, value)
    # pretty print all results, highlight found terms
