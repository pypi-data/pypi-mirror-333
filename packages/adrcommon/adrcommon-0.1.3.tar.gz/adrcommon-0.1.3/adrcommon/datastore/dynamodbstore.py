from itertools import count
from typing import List, Dict, Any, Tuple, Type
import boto3
import json
from decimal import Decimal

from adrcommon.constants import REF_ID
from adrcommon.query import Query, QueryGroup, QueryItem, Operator
from .datastore import IDataStore, T


def translate_query_item(item: QueryItem, value_index: count) -> Tuple[str, Dict[str, Any]]:
    key = item.key()

    if item.oper() == Operator.EQUALS:
        value_name = f":v{next(value_index)}"
        return f"#{key} = {value_name}", {value_name: item.value()}
    elif item.oper() == Operator.NOT_EQUALS:
        value_name = f":v{next(value_index)}"
        return f"#{key} <> {value_name}", {value_name: item.value()}
    elif item.oper() == Operator.LESS_THAN:
        value_name = f":v{next(value_index)}"
        return f"#{key} < {value_name}", {value_name: item.value()}
    elif item.oper() == Operator.LESS_THAN_EQUALS:
        value_name = f":v{next(value_index)}"
        return f"#{key} <= {value_name}", {value_name: item.value()}
    elif item.oper() == Operator.GREATER_THAN:
        value_name = f":v{next(value_index)}"
        return f"#{key} > {value_name}", {value_name: item.value()}
    elif item.oper() == Operator.GREATER_THAN_EQUALS:
        value_name = f":v{next(value_index)}"
        return f"#{key} >= {value_name}", {value_name: item.value()}
    elif item.oper() == Operator.BEGINS_WITH:
        value_name = f":v{next(value_index)}"
        return f"begins_with(#{key}, {value_name})", {value_name: item.value()}
    elif item.oper() == Operator.CONTAINS:
        value_name = f":v{next(value_index)}"
        return f"contains(#{key}, {value_name})", {value_name: item.value()}
    elif item.oper() == Operator.NOT_CONTAINS:
        value_name = f":v{next(value_index)}"
        return f"NOT contains(#{key}, {value_name})", {value_name: item.value()}
    elif item.oper() == Operator.IN:
        iv = item.value() or ['YODAWG']
        values = {f":v{next(value_index)}": v for v in iv}
        return f"#{key} IN ({', '.join(values.keys())})", values
    elif item.oper() == Operator.NOT_IN:
        iv = item.value() or ['YODAWG']
        values = {f":v{next(value_index)}": v for v in iv}
        return f"#{key} NOT IN ({', '.join(values.keys())})", values
    elif item.oper() == Operator.ENDS_WITH:
        raise NotImplementedError("ENDS_WITH operator is not supported in DynamoDB")
    
    raise NotImplementedError(item.oper())


def translate_query_group(group: QueryGroup) -> Tuple[str, Dict[str, Any], Dict[str, str]]:
    """Translate a QueryGroup into a DynamoDB filter expression string and its values."""
    expressions = []
    values = {}
    names = {}
    current_op = 'AND'  # Default to AND
    value_index = count()
    
    for item in group.items():
        if isinstance(item, QueryItem):
            expr, translated_values = translate_query_item(item, value_index)
            if expr:
                expressions.append(expr)
                names[f"#{item.key()}"] = item.key()
                values.update(translated_values)
        elif isinstance(item, list):
            if isinstance(item[0], list):
                # Nested group
                nested_expr, nested_values, nested_names = translate_query_group(QueryGroup(item))
                if nested_expr:
                    expressions.append(f"({nested_expr})")
                    values.update(nested_values)
                    names.update(nested_names)
            else:
                # QueryItem in list form
                item = QueryItem.parse(item)
                expr, translated_values = translate_query_item(item, value_index)
                if expr:
                    expressions.append(expr)
                    names[f"#{item.key()}"] = item.key()
                    values.update(translated_values)
        elif isinstance(item, Operator):
            current_op = item

    return f" {current_op} ".join(expr for expr in expressions if expr), values, names

def convert_data(row: Dict[str, Any]) -> Decimal:
    return json.loads(json.dumps(row), parse_float=Decimal)


class DynamoDBStore(IDataStore):
    def __init__(self, schema: Type[T], table_name: str):
        self._dynamodb = boto3.resource('dynamodb')
        self._schema = schema
        self._table = self._dynamodb.Table(table_name)

    def retrieve(self, query: Query) -> List[Dict[str, Any]]:
        filter_expression, values, names = translate_query_group(query.group())
        if not filter_expression:
            response = self._table.scan()
        else:
            response = self._table.scan(
                FilterExpression=filter_expression,
                ExpressionAttributeValues=values,
                ExpressionAttributeNames=names
            )
        return response.get('Items', [])

    def create(self, data: Dict[str, Any]):
        data = convert_data(data)
        self._table.put_item(Item=data)

    def update(self, data: Dict[str, Any], query: Query):
        filter_expression, values, names = translate_query_group(query.group())
        if not filter_expression:
            return
        
        data = convert_data(data)

        # First get matching items
        response = self._table.scan(
            FilterExpression=filter_expression,
            ExpressionAttributeValues=values,
            ExpressionAttributeNames=names
        )
        for item in response.get('Items', []):
            # Update each matching item
            updated_item = {**item, **data}
            self._table.put_item(Item=updated_item)

    def delete(self, query: Query):
        filter_expression, values, names = translate_query_group(query.group())
        if not filter_expression:
            return

        # First get matching items
        response = self._table.scan(
            FilterExpression=filter_expression,
            ExpressionAttributeValues=values,
            ExpressionAttributeNames=names
        )
        for item in response.get('Items', []):
            # Delete each matching item
            self._table.delete_item(Key={REF_ID: item[REF_ID]})
