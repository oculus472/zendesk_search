import json
import pathlib
from operator import itemgetter
from pathlib import Path
from time import perf_counter
from typing import Iterable

from ..logger import get_logger
from ..utils import Bunch
from .indexer import get_indexer
from .relationships import collection_relationships

logger = get_logger()

_data_path = Path(__file__).resolve().parent.parent.parent / "data"

all_collections = [
    path.stem for path in pathlib.Path(_data_path).iterdir() if path.is_file()
]

db = Bunch()


class Collection:
    """A collection represents a set of documents.

    Equivilent to a table in traditional databases.
    """

    def __init__(self, name):
        self._name = name
        self._data = self._get_data(self._name)
        self._searchable_fields = list(self._data[0])
        self._searchable_fields.sort()
        self._indexer = get_indexer()

    @property
    def searchable_fields(self):
        """The fields that can be searched on documents in the collection

        Returns:
            (list[str]): list of searchable fields.
        """
        return self._searchable_fields

    def find(self, **kwargs) -> Iterable[dict]:
        """Find documents matching the supplied query.

        The `select_related` kwarg can be supplied to include any
        documents from related collections in the results.

        Example:
        collection.find(name="DocumentName")

        Returns:
            Iterable[dict]: list of documents matching query.
        """
        documents = []
        select_related = kwargs.pop("select_related", False)
        for index, _ in self._indexer.find(**kwargs):
            document = self._data[index]
            if select_related:
                document = {**document, **self._join_collections(document)}
            documents.append(document)
        return documents

    def _join_collections(self, document):
        """Fetch related documents from other collections

        Args:
            document (dict): the document to join.

        Returns:
            dict: a dicitionary containing documents from
            foreign collections.
        """
        result = {}
        for relation in collection_relationships.get(self._name, []):
            related_collection = getattr(db, relation["collection"])
            fk, pk = itemgetter("foreign_key", "primary_key")(relation)
            try:
                related_documents = related_collection.find(**{fk: document[pk]})
            # Happens when a document is missing a field.
            # Probably wouldn't be a thing with real data.
            except KeyError:
                pass
            result[relation["propogate_field"]] = related_documents
        return result

    def build_index(self):
        """Build the collection index."""
        self._indexer.build_index(self._data)

    def _get_data(self, collection_name: str) -> Iterable[dict]:
        """Get the raw data for this collection

        Args:
            collection_name (str): name of the collection,
            this corresponds to a json file in the data directory.

        Returns:
            Iterable[dict]: list of documents.
        """
        filepath = _data_path / f"{collection_name}.json"
        with open(filepath, "r") as content:
            return json.load(content)


def _build_collection(name) -> Collection:
    """Build and index the supplied collection.

    Args:
        name (str): name of the collection.

    Returns:
        Collection: The indexed collection.
    """
    collection = Collection(name)
    start_time = perf_counter()
    collection.build_index()
    end_time = perf_counter()
    logger.info(f"Indexing duration: {end_time - start_time}")
    return collection


def build_collections() -> None:
    """Build and index all collections."""
    for collection_name in all_collections:
        setattr(db, collection_name, _build_collection(collection_name))
