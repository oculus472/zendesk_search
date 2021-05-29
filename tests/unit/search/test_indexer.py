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
                    "description": "Plumber by trade, hardworker",
                    "country": "USA",
                    "tags": ["tradesmen", "chess"],
                },
                {
                    "name": "anne",
                    "last_name": "jenkins",
                    "description": "Extremely bright hardworker",
                    "country": "USA",
                    "tags": ["engineer", "chess"],
                },
            ],
            ["name", "last_name", "country", "tags", "description"],
        )
        actual = self.indexer._index_data
        expected = {
            "name": {
                "bob": [(0, 0)],
                "anne": [(1, 0)],
            },
            "last_name": {
                "smith": [(0, 0)],
                "jenkins": [(1, 0)],
            },
            "description": {
                "plumber": [(0, 0)],
                "by": [(0, 1)],
                "trade": [(0, 2)],
                "extremely": [(1, 0)],
                "bright": [(1, 1)],
                "hardworker": [(0, 3), (1, 2)],
            },
            "country": {
                "usa": [(0, 0), (1, 0)],
            },
            "tags": {
                "tradesmen": [(0, 0)],
                "chess": [(0, 1), (1, 1)],
                "engineer": [(1, 0)],
            },
        }

        assert expected == actual
