from dataclasses import dataclass

from zendesk_search.models import ZendeskModel


def test_zendesk_model_get_searchable_fields_returns_model_fields():
    @dataclass(frozen=True)
    class TestModel(ZendeskModel):
        subclass_field: bool

    assert TestModel.get_searchable_fields() == [
        "_id",
        "url",
        "external_id",
        "created_at",
        "tags",
        "subclass_field",
    ]
