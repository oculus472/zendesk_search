from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from typing import Any

from ..logger import get_logger
from .tokenizer import tokenize

logger = get_logger()


class Indexer(ABC):
    """Database collection indexer base class."""

    @abstractmethod
    def build_index(self, data) -> None:
        """Builds a index based on concrete class implementation."""

    @abstractmethod
    def find(self, **kwargs) -> list[tuple[int, int]]:
        """Find the indexes of entries matching the supplied query."""


class InvertedIndex(Indexer):
    """Index documents using inverted indexing."""

    def __init__(self):
        self._index_data = defaultdict(lambda: defaultdict(list))

    def _normalize_index(self, value):
        """Normalize supplied value so it's suitable for an
        index key.

        Args:
            value (Any): value to normalize.

        Returns:
            Any: the normalized value.
        """
        if isinstance(value, (int, bool)):
            value = str(value)
        if isinstance(value, str):
            return value.lower()
        return value

    def _tokenize_field(self, value: Any) -> Iterable[Any]:
        """Tokenize a field in preparation to use as an index key.

        If a iterable type is supplied the function will be recursively called
        until it creates a list of tokens of basic types.

        Args:
            value (Any): value to tokenize.

        Returns:
            Iterable[Any]: the tokenized value.
        """
        value = self._normalize_index(value)
        if isinstance(value, str):
            return tokenize(value)
        if isinstance(value, Iterable):
            tokens: list[Any] = []
            for nested_value in value:
                tokens.extend(self._tokenize_field(nested_value))
            return tokens
        return [value]

    def build_index(self, data: Iterable[dict]) -> None:
        """Build the inverted index.

        Args:
            data (Iterable[dict]): raw list of documents.
        """
        for document_index, document in enumerate(data):
            for field, value in document.items():
                tokens = self._tokenize_field(value)
                for pos, token in enumerate(tokens):
                    self._index_data[field][token].append((document_index, pos))

    def find(self, **kwargs) -> list[tuple[int, int]]:
        """Find index/position pairs for the supplied query.

        Example:
        indexes = indexer.find(name="TestName")
        indexes # [(4, 0)]

        Returns:
            list[tuple[int, int]]: index,position pair.
        """
        result = []
        for field, value in kwargs.items():
            value = self._normalize_index(value)
            try:
                result.extend(self._index_data[field][value])
            except KeyError:
                pass
        return result


def get_indexer() -> Indexer:
    """Get a indexer instance."""
    return InvertedIndex()
