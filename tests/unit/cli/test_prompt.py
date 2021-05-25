import pytest
from PyInquirer.prompt import prompt
from pytest_mock.plugin import MockerFixture

from zendesk_search.cli.exceptions import QuittingException
from zendesk_search.cli.prompt import (
    _action_handler_map,
    handle_action,
    prompt_for_action,
    prompt_loop,
    quit_action,
    search_zendesk_action,
)


def test_quit_action_raises_quitting_exception():
    with pytest.raises(QuittingException):
        quit_action()


def test_prompt_for_action_returns_the_supplied_action(mocker: MockerFixture):
    def fake_prompt(questions):
        return {"action": "Quit"}

    mocker.patch("zendesk_search.cli.prompt.prompt", wraps=fake_prompt)
    result = prompt_for_action()

    assert result == "Quit"


@pytest.mark.parametrize("action", list(_action_handler_map))
def test_handle_action_calls_associated_action_handler(action, mocker: MockerFixture):
    mocked_func = mocker.MagicMock()
    mocked_func.__name__ = "mocked_handler"
    mocker.patch("zendesk_search.cli.prompt.prompt")
    mocker.patch.dict(
        "zendesk_search.cli.prompt._action_handler_map", {action: mocked_func}
    )
    handle_action(action)

    mocked_func.assert_called_once()


def test_handle_action_does_nothing_for_invalid_action():
    assert handle_action("List search fields") is None


def test_prompt_loop_returns_if_quitting_exception_raised(mocker: MockerFixture):
    # Test that the loop is executing and raise the exception after `n` loops.
    # If loop_counter == n when prompt_loop returns we can conclude the exception was
    # the cause of the function returning/breaking out of the main loop.
    loop_count = 0

    def fake_handle_action(action=""):
        nonlocal loop_count
        loop_count += 1
        if loop_count == 6:
            raise QuittingException

    mocker.patch("zendesk_search.cli.prompt.handle_action", wraps=fake_handle_action)
    mocker.patch("zendesk_search.cli.prompt.prompt_for_action")
    prompt_loop()

    assert loop_count == 6
