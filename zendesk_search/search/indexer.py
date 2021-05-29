from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from typing import Any

from ..logger import get_logger
from .tokenizer import tokenize

logger = get_logger()


class Indexer(ABC):
    @abstractmethod
    def build_index(self, data, fields_to_index) -> None:
        pass

    @abstractmethod
    def find(self, query):
        pass

    @abstractmethod
    def filter(self, query):
        pass


class InvertedIndex(Indexer):
    def __init__(self):
        self._index_data = defaultdict(list)

    def _tokenize_field(self, value: Any) -> Iterable[Any]:
        if isinstance(value, str):
            return tokenize(value)
        if isinstance(value, Iterable):
            tokens: list[Any] = []
            for nested_value in value:
                tokens.extend(self._tokenize_field(nested_value))
            return tokens
        # bools, ints, etc.
        return [value]

    def _get_key(self, value, field):
        return f"{field}.{value}"

    def build_index(self, data: Iterable[dict], fields_to_index: Iterable[str]) -> None:
        document_index = 0
        for document in data:
            for field in fields_to_index:
                try:
                    value = document[field]
                except KeyError:
                    logger.warning(
                        f"Document at index {document_index} missing field {field}"
                    )
                else:
                    tokens = self._tokenize_field(value)
                    for token in tokens:
                        key = self._get_key(token, field)
                        self._index_data[key].append(document_index)
            document_index += 1

    def find(self, query):
        pass

    def filter(self, query):
        pass


def get_indexer() -> Indexer:
    return InvertedIndex()
