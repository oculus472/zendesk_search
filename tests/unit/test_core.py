from zendesk_search.core import get_field_choices_for_collection


def test_get_field_choices_for_collection_returns_fields():
    assert get_field_choices_for_collection("users", False) == [
        "_id",
        "url",
        "external_id",
        "created_at",
        "tags",
        "name",
        "alias",
        "active",
        "verified",
        "shared",
        "locale",
    ]
