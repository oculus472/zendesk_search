import textwrap
import time

import pytest


@pytest.mark.skip(reason="Flakey in CI/CD")
def test_search_zendesk_action_with_results(cli_app, keys):
    cli_app.expect(
        textwrap.dedent(
            """\
             ? What do you want to do?  (Use arrow keys)
              ❯ Search Zendesk
                List search fields
                Quit"""
        )
    )

    cli_app.write(keys["enter"])
    time.sleep(1.5)

    cli_app.expect(
        textwrap.dedent(
            """\
            ? What do you want to do?  Search Zendesk
            ? What collection do you want to search?  (Use arrow keys)
             ❯ organizations
               tickets
               users"""
        )
    )

    cli_app.write(keys["enter"])
    time.sleep(1.5)

    cli_app.expect(
        textwrap.dedent(
            """\
            ? What collection do you want to search?  organizations
            ? What field do you want to search?  (Use arrow keys)
             ❯ _id
               created_at
               details
               domain_names
               external_id
               name
               shared_tickets
               tags
               url"""
        )
    )

    cli_app.write(keys["enter"])
    time.sleep(1.5)

    cli_app.expect(
        textwrap.dedent(
            """\
            ? What field do you want to search?  _id
            ? What do you want to search for?"""
        )
    )

    cli_app.write("101")
    cli_app.write(keys["enter"])
    time.sleep(2)

    cli_app.expect(
        textwrap.dedent(
            """\
            ? What do you want to search for?  101
            {
                "_id": 101,
                "url": "http://initech.zendesk.com/api/v2/organizations/101.json",
                "external_id": "9270ed79-35eb-4a38-a46f-35725197ea8d",
                "name": "Enthaze",
                "domain_names": [
                    "kage.com",
                    "ecratic.com",
                    "endipin.com",
                    "zentix.com"
                ],
                "created_at": "2016-05-21T11:10:28 -10:00",
                "details": "MegaCorp",
                "shared_tickets": false,
                "tags": [
                    "Fulton",
                    "West",
                    "Rodriguez",
                    "Farley"
                ]
            }
            ? What do you want to do?  (Use arrow keys)
             ❯ Search Zendesk
               List search fields
               Quit"""
        )
    )
