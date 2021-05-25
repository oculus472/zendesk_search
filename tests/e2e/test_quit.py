import textwrap
import time


def test_quit_action(cli_app, keys):
    cli_app.expect(
        textwrap.dedent(
            """\
             ? What do you want to do?  (Use arrow keys)
              ❯ Search Zendesk
                List search fields
                Quit"""
        )
    )

    cli_app.write(keys["down"])
    cli_app.write(keys["down"])

    cli_app.expect(
        "❯ Quit",
        strict=False,
    )

    cli_app.write(keys["enter"])
    time.sleep(1.5)

    assert cli_app.isalive() is False
