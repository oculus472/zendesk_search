from time import perf_counter
from typing import Dict, Iterable, Optional

from zendesk_search.logger import get_logger

from ..core import collection_name_to_model_map, get_collection_data
from .indexer import Indexer, get_indexer

logger = get_logger()


class Collection:
    def __init__(
        self, data, index_fields: Iterable[str], indexer: Optional[Indexer] = None
    ):
        self._data = data
        self._index_fields = index_fields
        if not indexer:
            indexer = get_indexer()
        self._indexer = indexer

    def find(self, query):
        self._indexer.find(query)

    def build_index(self, fields: Optional[Iterable[str]] = None):
        if not fields:
            fields = self._index_fields
        self._indexer.build_index(self._data, fields)


_collections: Dict[str, Optional[Collection]] = {
    "users": None,
    "tickets": None,
    "organizations": None,
}


def get_collection(collection_name: str) -> Optional[Collection]:
    return _collections.get(collection_name)


def _build_collection(
    data, index_fields: Iterable[str], indexer: Optional[Indexer] = None
) -> Collection:
    collection = Collection(data, index_fields, indexer)
    start_time = perf_counter()
    collection.build_index()
    end_time = perf_counter()
    logger.info(f"Indexing duration: {end_time - start_time}")
    return collection


def build_collections() -> None:
    for collection_name, model in collection_name_to_model_map.items():
        data = get_collection_data(collection_name)
        index_fields = model.get_searchable_fields()
        logger.debug(
            f"Building {collection_name} collection, indexed fields: {index_fields}"
        )
        _collections[collection_name] = _build_collection(data, index_fields)
