from zendesk_search.enums import ExtendedEnum


def test_values_method_returns_all_enum_values():
    class TestEnum(ExtendedEnum):
        Error = "raised error"
        Running = "still running"
        Success = "completed successfully"

    assert TestEnum.values() == [
        "raised error",
        "still running",
        "completed successfully",
    ]
