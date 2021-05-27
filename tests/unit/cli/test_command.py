from pytest_mock import MockerFixture

from zendesk_search.cli.command import _cli


def test_verbose_arg_calls_set_log_level(mocker: MockerFixture):
    mocked_func = mocker.patch("zendesk_search.cli.command.set_log_level")
    _cli(show_prompt=False, show_banner=False, verbose=2)
    mocked_func.assert_called_once_with(2)


def test_show_banner_arg_calls_display_banner(mocker: MockerFixture):
    mocked_func = mocker.patch("zendesk_search.cli.command.display_banner")
    _cli(show_prompt=False, show_banner=True, verbose=2)
    mocked_func.assert_called_once()


def test_show_prompt_arg_calls_prompt_loop(mocker: MockerFixture):
    mocked_func = mocker.patch("zendesk_search.cli.command.prompt_loop")
    _cli(show_prompt=True, show_banner=False, verbose=2)
    mocked_func.assert_called_once()
