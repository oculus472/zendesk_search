from operator import itemgetter
from typing import Callable, Iterable, Mapping, NoReturn

from PyInquirer.prompt import prompt
from tabulate import tabulate

from ..logger import get_logger
from ..search import all_collections, db
from .exceptions import QuittingException
from .utils import display_document

logger = get_logger()


def _calculate_field_choices(answers: dict) -> Iterable[str]:
    """Calculate the field choices for the search action

    Args:
        answers (dict): answers to previously supplied questions.
        We have access to the selected collection here that allows
        for the calculation.

    Returns:
        Iterable[str]: list of valid search fields.
    """
    collection = getattr(db, answers["collection_name"])
    return collection.searchable_fields


def search_zendesk_action() -> None:
    """Handles the "Search Zendesk" action

    Prompts the user for input that builds up a search query
    and finally prints the results to the terminal.
    """
    opts = prompt(
        [
            {
                "type": "list",
                "name": "collection_name",
                "message": "What collection do you want to search?",
                "choices": all_collections,
            },
            {
                "type": "list",
                "name": "field",
                "message": "What field do you want to search?",
                "choices": _calculate_field_choices,
            },
            {
                "type": "input",
                "name": "value",
                "message": "What do you want to search for?",
            },
        ]
    )
    logger.debug(f"User selected the following search options: {opts}")
    try:
        collection_name, field, value = itemgetter("collection_name", "field", "value")(
            opts
        )
        collection = getattr(db, collection_name)
        documents = collection.find(**{field: value, "select_related": True})
        if not documents:
            print("No documents found")
            return
        for document in documents:
            display_document(document)
    # Happens if the user CTRL+C while prompt is executing
    except (KeyError, AttributeError):
        pass


def list_search_fields_action() -> None:
    """Displays the search fields for all collections."""
    table = {}
    for collection_name in all_collections:
        collection = getattr(db, collection_name)
        table[collection_name] = collection.searchable_fields
    print(tabulate(table, headers="keys", tablefmt="psql"))


def quit_action() -> NoReturn:
    """Signals the application should quit.

    By throwing the exception we cause the prompt loop to break.
    We use an exception instead of a global "is_running" type variable.

    Raises:
        QuittingException: Signals the application is quitting.

    Returns:
        NoReturn
    """
    logger.debug("Raising quitting exception")
    raise QuittingException


_action_handler_map: Mapping[str, Callable] = {
    "Search Zendesk": search_zendesk_action,
    "List search fields": list_search_fields_action,
    "Quit": quit_action,
}


def prompt_for_action() -> str:
    """Prompt the user for an action and return their choice."""
    logger.debug("Prompting user for action")
    action = prompt(
        [
            {
                "type": "list",
                "name": "action",
                "message": "What do you want to do?",
                "choices": list(_action_handler_map),
            }
        ]
    ).get("action")
    logger.debug(f"User selected action: {action}")
    return action


def handle_action(action: str) -> None:
    """Handle the action requested by the user.

    Args:
        action (str): the action to perform.
    """
    handler = _action_handler_map.get(action)
    if not handler:
        logger.warning(f"No handler found for action {action}")
        return
    logger.debug(f"Executing handler: {handler.__name__}")
    handler()


def prompt_loop() -> None:
    """Prompt the user for actions until a quit aciton is requested."""
    while True:
        try:
            handle_action(prompt_for_action())
        # SIGINT signal already handled gracefully by PyInquirer.
        except QuittingException:
            break
