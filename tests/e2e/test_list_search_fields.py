import textwrap
import time

import pexpect


def test_list_search_fields_command(cli_app, keys):
    cli_app.expect(
        textwrap.dedent(
            """\
             ? What do you want to do?  (Use arrow keys)
              ❯ Search zendesk
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
            +-------------+-----------------+----------------+
            | User        | Ticket          | Organization   |
            |-------------+-----------------+----------------|
            | _id         | _id             | _id            |
            | active      | created_at      | created_at     |
            | alias       | description     | details        |
            | created_at  | due_at          | domain_names   |
            | external_id | external_id     | external_id    |
            | locale      | has_incidents   | name           |
            | name        | organization_id | shared_tickets |
            | shared      | priority        | tags           |
            | tags        | status          | url            |
            | url         | subject         |                |
            | verified    | submitter_id    |                |
            |             | tags            |                |
            |             | type            |                |
            |             | url             |                |
            |             | via             |                |
            +-------------+-----------------+----------------+
        """
        )
    )
