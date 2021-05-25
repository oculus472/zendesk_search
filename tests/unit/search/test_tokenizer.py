import pytest

from zendesk_search.search.tokenizer import tokenize


@pytest.mark.parametrize(
    "arg,expected",
    [
        ("test", ["test"]),
        ("This is a sentence", ["this", "is", "a", "sentence"]),
        (
            "Another one, this time it'll have.... punctuation!",
            ["another", "one", "this", "time", "itll", "have", "punctuation"],
        ),
    ],
)
def test_tokenize_returns_tokenized_list(arg, expected):
    actual = tokenize(arg)

    assert expected == actual
