import pytest

from zendesk_search.cli.utils import display_document
from zendesk_search.search import db
from zendesk_search.search.collections import _build_collection, build_collections


@pytest.mark.parametrize("collection", ("users", "tickets", "organizations"))
def test_build_collections_builds_expected_collection(collection):
    build_collections()
    assert getattr(db, collection)


def test_searchable_fields_returns_document_keys():
    collection = _build_collection("users")

    assert collection.searchable_fields == [
        "_id",
        "active",
        "alias",
        "created_at",
        "email",
        "external_id",
        "last_login_at",
        "locale",
        "name",
        "organization_id",
        "phone",
        "role",
        "shared",
        "signature",
        "suspended",
        "tags",
        "timezone",
        "url",
        "verified",
    ]


def test_find_returns_document():
    build_collections()
    documents = db.organizations.find(name="Enthaze")

    assert documents == [
        {
            "_id": 101,
            "url": "http://initech.zendesk.com/api/v2/organizations/101.json",
            "external_id": "9270ed79-35eb-4a38-a46f-35725197ea8d",
            "name": "Enthaze",
            "domain_names": ["kage.com", "ecratic.com", "endipin.com", "zentix.com"],
            "created_at": "2016-05-21T11:10:28 -10:00",
            "details": "MegaCorp",
            "shared_tickets": False,
            "tags": ["Fulton", "West", "Rodriguez", "Farley"],
        }
    ]
