import click
import pyfiglet

from .. import __version__
from ..logger import get_logger, set_log_level
from ..search import build_collections
from .prompt import prompt_loop

logger = get_logger()


def initialize():
    """Initialize the CLI application."""
    logger.debug("Initializing..")
    build_collections()


def display_banner():
    """Display the CLI app banner."""
    logger.debug("Displaying banner")
    banner = pyfiglet.figlet_format("Zendesk   Search")
    print(banner)


def _cli(show_prompt: bool, show_banner: bool, verbose: int) -> None:
    """Entrypoint stub.

    Makes unit testing easier, we don't need to mess
    with setting values for click.option.

    Args:
        show_prompt (bool): prompt the user for search input
        show_banner (bool): print the CLI banner
        verbose (int): verbosity level, example: -vvv
    """
    if verbose:
        set_log_level(verbose)
    initialize()
    if show_banner:
        display_banner()
    if show_prompt:
        prompt_loop()
    else:
        # run as cli
        pass


@click.command()
@click.version_option(__version__)
@click.option("-v", "--verbose", count=True)
@click.option("--show-prompt", default=True)
@click.option("--show-banner", default=True)
def cli(*args, **kwargs) -> None:
    """Entrypoint for the application."""
    return _cli(*args, **kwargs)
