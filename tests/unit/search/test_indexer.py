import pytest

from zendesk_search.search.indexer import InvertedIndex


class TestInvertedIndex:
    def setup_method(self):
        self.indexer = InvertedIndex()

    @pytest.mark.parametrize(
        "arg,expected",
        [
            ("Test sentence", ["test", "sentence"]),
            (11, [11]),
            (True, [True]),
            (["test", "list"], ["test", "list"]),
            (["nested", ["another", "level"]], ["nested", "another", "level"]),
        ],
    )
    def test_tokenize_field_handles_input(self, arg, expected):
        actual = self.indexer._tokenize_field(arg)

        assert expected == actual

    def test_build_index_builds_an_inverted_index(self):
        self.indexer.build_index(
            [
                {
                    "name": "bob",
                    "last_name": "smith",
                    "country": "USA",
                    "tags": ["tradesmen", "chess"],
                },
                {
                    "name": "anne",
                    "last_name": "jenkins",
                    "country": "USA",
                    "tags": ["engineer", "chess"],
                },
            ],
            ["name", "last_name", "country", "tags"],
        )
        actual = self.indexer._index_data
        expected = {
            "name.bob": [0],
            "name.anne": [1],
            "last_name.smith": [0],
            "last_name.jenkins": [1],
            "country.usa": [0, 1],
            "tags.tradesmen": [0],
            "tags.chess": [0, 1],
            "tags.engineer": [1],
        }

        assert expected == actual

    def test_get_key_returns_expected_key_format(self):
        actual = self.indexer._get_key("heidi", "name")
        expected = "name.heidi"

        assert expected == actual
