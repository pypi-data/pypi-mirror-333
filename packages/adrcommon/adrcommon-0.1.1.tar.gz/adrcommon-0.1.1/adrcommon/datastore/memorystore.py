from typing import List, Dict, Any, Type

from .datastore import IDataStore, T
from adrcommon.query import Query, QueryGroup, QueryItem, Operator


def apply_query_item(item: QueryItem, row: Dict[str, Any]) -> bool:
    value = row.get(item.key())
    query_value = item.value()

    if item.oper() == Operator.EQUALS:
        return value == query_value
    elif item.oper() == Operator.NOT_EQUALS:
        return value != query_value
    elif item.oper() == Operator.LESS_THAN:
        return value < query_value if value is not None else False
    elif item.oper() == Operator.LESS_THAN_EQUALS:
        return value <= query_value if value is not None else False
    elif item.oper() == Operator.GREATER_THAN:
        return value > query_value if value is not None else False
    elif item.oper() == Operator.GREATER_THAN_EQUALS:
        return value >= query_value if value is not None else False
    elif item.oper() == Operator.BEGINS_WITH:
        return value.startswith(query_value) if value is not None else False
    elif item.oper() == Operator.ENDS_WITH:
        return value.endswith(query_value) if value is not None else False
    elif item.oper() == Operator.CONTAINS:
        return query_value in value if value is not None else False
    elif item.oper() == Operator.NOT_CONTAINS:
        return query_value not in value if value is not None else True
    elif item.oper() == Operator.IN:
        return value in query_value if value is not None else False
    return False


def apply_query_group(group: QueryGroup, row: Dict[str, Any]) -> bool:
    items = group.items()

    result = True
    current_op = Operator.AND

    for item in items:
        if QueryItem.is_query_item(item):
            item = QueryItem.parse(item)
            
            item_result = apply_query_item(item, row)
            result = result and item_result if current_op == Operator.AND else result or item_result
        elif isinstance(item, list):
            group_result = apply_query_group(QueryGroup(item), row)
            result = result and group_result if current_op == Operator.AND else result or group_result
        elif item in (Operator.AND, Operator.OR):
            current_op = item

    return result


class MemoryStore(IDataStore):
    def __init__(self, schema: Type[T]):
        self._schema = schema
        self._rows: List[Dict[str, Any]] = []

    def retrieve(self, query: Query) -> List[Dict[str, Any]]:
        return [row for row in self._rows if apply_query_group(query.group(), row)]

    def create(self, data: Dict[str, Any]):
        self._rows.append(data)

    def update(self, data: Dict[str, Any], query: Query):
        for row in self._rows:
            if apply_query_group(query.group(), row):
                row.update(data)

    def delete(self, query: Query):
        self._rows = [row for row in self._rows if not apply_query_group(query.group(), row)]
