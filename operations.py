from json import dump, load
from os import makedirs, remove
from os.path import exists
from types import MappingProxyType
from typing import Tuple, Dict, Generator, Any

OPERATION_LESS = "<"
OPERATION_EQUAL = "="
OPERATION_GREATER = ">"

OPERATIONS = {
    OPERATION_LESS: '<',
    OPERATION_EQUAL: '==',
    OPERATION_GREATER: '>',
}

class TableManager:

    def create(self, db: str = 'app', table: str = None, **fields):
        if not exists(db):
            makedirs(db)
        fields['records'] = ()
        with open(file=f'{db}/{table}.json', mode='w+') as file:
            dump(obj=fields, fp=file, indent=4)

    def drop(self, db: str = 'app', table: str = None):
        filepath: str = f'{db}/{table}.json'
        if exists(path=filepath):
            remove(filepath)

    def select(
            self, db: str = 'app', table: str = None,
            requested_fields: Tuple = (), conditions: Tuple = (), limit: int = None
    ) -> Generator[Dict, Any, None]:
        filepath: str = f'{db}/{table}.json'
        if not exists(path=filepath):
            raise ValueError(f'No {table} doesn\'t exist')
        with open(file=filepath, mode='r') as file:
            data = load(fp=file)
            fields: Dict = data.get('fields')
            records: list = data.get('records')
            for requested_field in requested_fields:
                if requested_field not in fields.keys():
                    raise ValueError(f'table doesn\'t have this field: {requested_field}')
            for record in records:
                for condition in conditions:
                    if condition.get('field') == None:
                        continue
                    if condition.get('field') not in fields.keys():
                        raise ValueError(f'table doesn\'t have this field: {condition.get("field")}')
                    if fields.get(condition.get('field')) != 'number':
                        raise ValueError('table supports only number filtering')
                    if eval(f"not record.get(condition.get('field')) {condition.get('operator')} condition.get('value')"):
                        records.remove(record)
            requested_records =  ({
                requested_field: record.get(requested_field) for requested_field in requested_fields
            } for record in records)
            return requested_records if limit is None else list(requested_records)[:limit]
