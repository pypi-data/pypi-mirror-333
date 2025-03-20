from enum import Enum
from typing import Any


LIMIT = 'limit'
OFFSET = 'offset'

class Operator(str, Enum):
    EQUALS = 'eq'
    NOT_EQUALS = 'neq'
    LESS_THAN = 'lt'
    LESS_THAN_EQUALS = 'lte'
    GREATER_THAN = 'gt'
    GREATER_THAN_EQUALS = 'gte'
    BEGINS_WITH = 'bw'
    ENDS_WITH = 'ew'
    CONTAINS = 'cn'
    NOT_CONTAINS = 'ncn'
    IN = 'in'
    NOT_IN = 'nin'

    OR = 'OR'
    AND = 'AND'


class QueryItem(object):
    def __init__(self, oper: Operator, key: str, value: Any):
        self._oper = oper
        self._key = key
        self._value = value

    def oper(self):
        return self._oper

    def key(self):
        return self._key

    def value(self):
        return self._value
    
    @staticmethod
    def is_query_item(values):
        if isinstance(values, QueryItem): return True
        return len(values) == 3 and isinstance(values[1], Operator)

    @staticmethod
    def parse(values):
        if isinstance(values, QueryItem): return values
        return QueryItem(Operator(values[1]), values[0], values[2])


class QueryGroup(object):
    def __init__(self, items):
        self._items = items

    def items(self):
        return self._items

    def _add_item(self, oper, key=None, value=None):
        if oper and key and value is not None:
            self._items.append((key, oper, value))
            return

        if self._is_logic_item(oper) and not self._is_empty():
            self._items.append(oper)
            return

    def _is_logic_item(self, oper):
        return Operator.AND is oper or Operator.OR is oper

    def _is_empty(self):
        return not self._items

    def new_group(self, oper):
        oper = oper or Operator.AND
        
        if oper and self._is_logic_item(oper) and not self._is_empty():
            self._items.append(oper)

        child_items = []
        self._items.append(child_items)
        return QueryGroup(child_items)


    def OR(self):
        self._add_item(Operator.OR)
        return self

    def AND(self):
        self._add_item(Operator.AND)

    def IN(self, key, values):
        self._add_item(Operator.IN, key, values)
        return self
    
    def NOT_IN(self, key, values):
        self._add_item(Operator.NOT_IN, key, values)
        return self

    def equals(self, key, value):
        self._add_item(Operator.EQUALS, key, value)
        return self

    def contains(self, key, value):
        self._add_item(Operator.CONTAINS, key, value)
        return self


class Query(object):
    def __init__(self):
        self._items = []
        self._group = QueryGroup(self._items)

        self._config = {
            LIMIT: 1000
        }

    def group(self):
        return self._group

    def items(self):
        return self._items
    
    def config(self, key: str = None):
        if key is not None: return self._config.get(key, None)
        return self._config

    def AND(self):
        self.group().AND()
        return self

    def OR(self):
        self.group().OR()
        return self

    def IN(self, key, values):
        self.group().IN(key, values)
        return self
    
    def NOT_IN(self, key, values):
        self.group().NOT_IN(key, values)
        return self

    def equals(self, key, value):
        self.group().equals(key, value)
        return self

    def contains(self, key, value):
        self.group().contains(key, value)
        return self

    def limit(self, limit: int):
        self._config[LIMIT] = limit
        return self
