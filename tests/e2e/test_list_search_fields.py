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
        Search Users with
        _id
        url
        external_id
        created_at
        tags
        name
        alias
        active
        verified
        shared
        locale
        ---------------
        Search Tickets with
        _id
        url
        external_id
        created_at
        tags
        type
        subject
        description
        priority
        status
        submitter_id
        organization_id
        has_incidents
        due_at
        via
        ---------------
        Search Organizations with
        _id
        url
        external_id
        created_at
        tags
        name
        domain_names
        details
        shared_tickets
        ---------------
        """
        )
    )
