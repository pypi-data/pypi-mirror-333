from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Type, TypeVar

from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField

from adrcommon.constants import REF_ID
from adrcommon.query import Query


class Record(BaseModel):
    def __hash__(self):  # make hashable BaseModel subclass
        return hash((type(self),) + tuple(self.__dict__.values()))

    def __getitem__(self, item):
        return getattr(self, item)
    
    ref_id: ObjectIdField = Field(default_factory=lambda: ObjectIdField(), description="Reference identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp")


T = TypeVar('T', bound=Record)


class IDataStore(ABC):
    @abstractmethod
    def retrieve(self, query: Query) -> List[Dict[str, Any]]: raise NotImplementedError()
    @abstractmethod
    def create(self, data: Dict[str, Any]): raise NotImplementedError()
    @abstractmethod
    def update(self, data: Dict[str, Any], query: Query): raise NotImplementedError()
    @abstractmethod
    def delete(self, query: Query): raise NotImplementedError()


class IDataStoreFactory(ABC):
    @abstractmethod
    def get(self, collection: Type[T]) -> IDataStore: raise NotImplementedError()


class Result:
    def __init__(self, rows: List[Dict[str, Any]]):
        self._rows = rows

    @property
    def count(self):
        return len(self._rows)

    def __iter__(self):
        def schema_iter():
            for row in self._rows:
                yield row
        
        return schema_iter()


class DataStore:
    def __init__(self, factory: IDataStoreFactory, schema: Type[T] = None):
        self._factory = factory
        self._schema = schema

    def retrieve(self, query: Query) -> Result:
        rows = self._factory.get(self._schema).retrieve(query)
        return Result(rows)

    def create(self, data: T) -> ObjectIdField:
        self._factory.get(self._schema).create(data)
        return data.ref_id

    def update(self, data: Dict[str, Any], query: Query) -> None:
        if REF_ID in data.keys(): del data[REF_ID]
        self._factory.get(self._schema).update(data, query)

    def delete(self, query: Query) -> None:
        self._factory.get(self._schema).delete(query)
