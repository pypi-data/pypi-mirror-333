from typing import Dict, Any, List, cast, Type, Iterable

from bson import ObjectId
from pymongo import MongoClient
from pymongo.synchronous.collection import Collection

from adrcommon.constants import REF_ID
from adrcommon.query import Operator, Query, QueryItem, QueryGroup, LIMIT
from .datastore import IDataStore, IDataStoreFactory, Record, T

MONGO = 'mongo'
MONGO_ID = '_id'

def translate_query_group(group: QueryGroup, existing_filter: Dict[str, Any] = None) -> Dict[str, Any]:
    existing_filter = existing_filter or {}
    mongo_filter = []
    items = group.items()

    for idx, item in enumerate(items):
        next_idx = idx + 1
        next_item = items[next_idx] if next_idx < len(items) else None
        
        if QueryItem.is_query_item(item):
            item = QueryItem.parse(item)
            
            # Single condition
            field = item.key() if item.key() != REF_ID else MONGO_ID
            operator = item.oper()
            value = item.value()
            
            if field == MONGO_ID:
                if isinstance(value, Iterable) and not isinstance(value, str):
                    value = [ObjectId(value) for value in value]
                else:
                    value = ObjectId(value)

            # Map operators to MongoDB format
            if operator == Operator.EQUALS:
                mongo_filter.append({field: {'$eq': value}})
            elif operator == Operator.NOT_EQUALS:
                mongo_filter.append({field: {'$ne': value}})
            elif operator == Operator.GREATER_THAN:
                mongo_filter.append({field: {'$gt': value}})
            elif operator == Operator.GREATER_THAN_EQUALS:
                mongo_filter.append({field: {'$gte': value}})
            elif operator == Operator.LESS_THAN:
                mongo_filter.append({field: {'$lt': value}})
            elif operator == Operator.LESS_THAN_EQUALS:
                mongo_filter.append({field: {'$lte': value}})
            elif operator == Operator.CONTAINS:
                mongo_filter.append({field: {'$regex': value}})
            elif operator == Operator.IN:
                mongo_filter.append({field: {'$in': value}})
            elif operator == Operator.NOT_IN:
                mongo_filter.append({field: {'$nin': value}})
            else:
                raise ValueError(f'Operator "{operator}" is not supported')
        elif item in (Operator.AND, Operator.OR):
            if isinstance(next_item, List):
                sub_filter = translate_query_group(QueryGroup(next_item))
                mongo_filter.append({f'{item.lower()}': sub_filter})
            

    # Combine filters with $and if multiple conditions exist
    if len(mongo_filter) > 0:
        if '$and' in existing_filter:
            existing_filter['$and'].extend(mongo_filter)
        else:
            existing_filter['$and'] = mongo_filter

    return existing_filter


def to_document(model: T) -> dict:
    """
    Convert model to document
    :param model:
    :return: dict
    """
    model_with_id = cast(Record, model)
    data = model_with_id.model_dump()
    data.pop(REF_ID)
    if model_with_id.ref_id:
        data["_id"] = model_with_id.ref_id
    return data


def to_model(schema: T, data: dict) -> T:
    """
    Convert document to model with custom output type
    """
    data_copy = data.copy()
    if "_id" in data_copy:
        data_copy[REF_ID] = data_copy.pop("_id")
    return schema.model_validate(data_copy)


class MongoDbStore(IDataStore):
    def __init__(self, schema: Type[T], collection: Collection):
        self._schema = schema
        self._collection = collection

    def retrieve(self, query: Query):
        filter_query = translate_query_group(query.group(), {})
        return [to_model(self._schema, row) for row in self._collection.find(filter_query, limit=query.config(LIMIT))]

    def create(self, data: T):
        in_data = to_document(data)
        self._collection.insert_one(in_data)

    def update(self, data: Dict[str, Any], query: Query):
        filter_query = translate_query_group(query.group(), {})
        self._collection.update_many(filter_query, {'$set': data})

    def delete(self, query: Query):
        filter_query = translate_query_group(query.group(), {})
        self._collection.delete_many(filter_query)


class MongoDbStoreFactory(IDataStoreFactory):
    def __init__(self, connection_uri: str, database_name: str, username: str = None, password: str = None):
        connection_uri = connection_uri.format(username=username, password=password)
        self._client = MongoClient(connection_uri)[database_name]
    
    def get(self, collection: Type[T]) -> MongoDbStore:
        return MongoDbStore(collection, self._client[collection.__name__.lower()])
