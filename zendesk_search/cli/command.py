import click
import pyfiglet

from .. import __version__
from ..logger import get_logger, set_log_level
from ..search.collections import build_collections
from .prompt import prompt_loop

logger = get_logger()


def initialize():
    logger.debug("Initializing..")
    build_collections()


def display_banner():
    logger.debug("Displaying banner")
    banner = pyfiglet.figlet_format("Zendesk   Search")
    print(banner)


def _cli(show_prompt: bool, show_banner: bool, verbose: int) -> None:
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
    return _cli(*args, **kwargs)
