import os, ndjson

from typing import Dict, Any, Type

from adrcommon import constants
from .datastore import IDataStore, T
from .memorystore import apply_query_group
from adrcommon.query import Query


def create_store_file(path):
    if not os.path.exists(path):
        with open(path, 'w+'): pass


class NdJsonStore(IDataStore):
    def __init__(self, schema: Type[T], path):
        self._schema = schema
        self._path = path

    def retrieve(self, query: Query):
        create_store_file(self._path)
        with open(self._path, constants.READ) as f:
            reader = ndjson.reader(f)
            result = [self._schema.model_validate(row) for row in reader if apply_query_group(query.group(), row)]
            result.sort(key=lambda x: x.timestamp)
            
            return result

    def create(self, data: Dict[str, Any]):
        create_store_file(self._path)
        with open(self._path, constants.APPEND_CREATE) as f:
            writer = ndjson.writer(f)
            writer.writerow(data)

    def update(self, data: Dict[str, Any], query: Query):
        create_store_file(self._path)
        with open(self._path, constants.READ) as f:
            rows = ndjson.load(f)

        for row in filter(lambda x: apply_query_group(query.group(), x), rows):
            row.update(data)

        with open(self._path, constants.OVERWRITE_CREATE) as f:
            data = ndjson.dumps(rows) + '\n'
            f.write(data)

    def delete(self, query: Query):
        create_store_file(self._path)
        with open(self._path, constants.READ) as f:
            rows = ndjson.load(f)

        rows = filter(lambda x: not apply_query_group(query.group(), x), rows)

        with open(self._path, constants.OVERWRITE_CREATE) as f:
            data = ndjson.dumps(rows) + '\n'
            f.write(data)
