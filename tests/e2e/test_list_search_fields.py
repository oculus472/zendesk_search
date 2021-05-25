import textwrap
import time

import pytest


@pytest.mark.skip("Flakey in CI/CD")
def test_list_search_fields_command(cli_app, keys):
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
    cli_app.write(keys["enter"])
    time.sleep(0.5)

    cli_app.expect(
        textwrap.dedent(
            """\
            ? What do you want to do?  List search fields
            +-----------------+-----------------+-----------------+
            | organizations   | tickets         | users           |
            |-----------------+-----------------+-----------------|
            | _id             | _id             | _id             |
            | created_at      | assignee_id     | active          |
            | details         | created_at      | alias           |
            | domain_names    | description     | created_at      |
            | external_id     | due_at          | email           |
            | name            | external_id     | external_id     |
            | shared_tickets  | has_incidents   | last_login_at   |
            | tags            | organization_id | locale          |
            | url             | priority        | name            |
            |                 | status          | organization_id |
            |                 | subject         | phone           |
            |                 | submitter_id    | role            |
            |                 | tags            | shared          |
            |                 | type            | signature       |
            |                 | url             | suspended       |
            |                 | via             | tags            |
            |                 |                 | timezone        |
            |                 |                 | url             |
            |                 |                 | verified        |
            +-----------------+-----------------+-----------------+
        """
        )
    )
