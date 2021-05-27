from zendesk_search.core import get_field_choices_for_resource


def test_get_field_choices_for_resource_returns_fields():
    assert get_field_choices_for_resource("users") == [
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
