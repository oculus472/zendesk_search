from enum import Enum
from typing import Callable, Mapping, NoReturn

from PyInquirer.prompt import prompt

from ..core import (
    all_resources,
    get_field_choices_for_resource,
    list_search_fields,
    search_zendesk,
)
from ..logger import get_logger
from .enums import ActionChoice
from .exceptions import QuittingException

logger = get_logger()


def _calculate_field_choices(answers: dict) -> list[str]:
    return get_field_choices_for_resource(answers["resource"])


def search_zendesk_action() -> None:
    opts = prompt(
        [
            {
                "type": "list",
                "name": "resource",
                "message": "What resource do you want to search?",
                "choices": all_resources,
            },
            {
                "type": "list",
                "name": "field",
                "message": "What field do you want to search?",
                "choices": _calculate_field_choices,
            },
            {
                "type": "input",
                "name": "search_term",
                "message": "What do you want to search for?",
            },
        ]
    )
    logger.debug(f"User selected the following search options: {opts}")
    search_zendesk(**opts)


def list_search_fields_action() -> None:
    list_search_fields()


def quit_action() -> NoReturn:
    # By raising an exception to signal quitting the application we avoid
    # the use of a global 'is_running' type variable.
    logger.debug("Raising quitting exception")
    raise QuittingException


_action_handler_map: Mapping[str, Callable] = {
    ActionChoice.SEARCH_ZENDESK.value: search_zendesk_action,
    ActionChoice.LIST_SEARCH_FIELDS.value: list_search_fields_action,
    ActionChoice.QUIT.value: quit_action,
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
                "choices": ActionChoice.values(),
            }
        ]
    ).get("action")
    logger.debug(f"User selected action: {action}")
    return action


def handle_action(action: str) -> None:
    handler = _action_handler_map.get(action)
    if not handler:
        logger.warn(f"No handler found for action {action}")
        return
    logger.debug(f"Executing handler: {handler.__name__}")
    handler()


def prompt_loop() -> None:
    while True:
        try:
            handle_action(prompt_for_action())
        # SIGINT signal already handled gracefully by PyInquirer.
        except QuittingException:
            break
