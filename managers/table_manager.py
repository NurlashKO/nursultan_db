from json import dump, load
from os import makedirs, remove
from os.path import exists
from types import MappingProxyType
from typing import Tuple, Dict, Generator, Any

from managers.index_manager import IndexManager, Singleton

OPERATION_LESS = "<"
OPERATION_EQUAL = "="
OPERATION_GREATER = ">"

OPERATIONS = {
    OPERATION_LESS: '<',
    OPERATION_EQUAL: '==',
    OPERATION_GREATER: '>',
}

class TableManager(metaclass=Singleton):

    def create(self, db: str = 'app', table: str = None, **fields):
        if not exists(db):
            makedirs(db)
        fields['records'] = ()
        fields['indexes'] = ()
        with open(file=f'{db}/{table}.json', mode='w+') as file:
            dump(obj=fields, fp=file, indent=4)

    def drop(self, db: str = 'app', table: str = None):
        filepath: str = f'{db}/{table}.json'
        if exists(path=filepath):
            remove(filepath)

    def select(
            self, db: str = 'app', table: str = None,
            requested_fields: Tuple = (), condition: Dict = None, limit: int = None
    ) -> Generator[Dict, Any, None]:
        filepath: str = f'{db}/{table}.json'
        if not exists(path=filepath):
            raise ValueError(f'No {table} doesn\'t exist')
        with open(file=filepath, mode='r') as file:
            data = load(fp=file)
            fields: Dict = data.get('fields')
            records: list = data.get('records')
            indexes : list = data.get('indexes')
            for requested_field in requested_fields:
                if requested_field not in fields.keys():
                    raise ValueError(f'table doesn\'t have this field: {requested_field}')

            if condition.get('field') != None:
                if condition.get('field') not in fields.keys():
                    raise ValueError(f'table doesn\'t have this field: {condition.get("field")}')
                if fields.get(condition.get('field')) != 'number':
                    raise ValueError('table supports only number filtering')
                if condition.get('field') in indexes:
                    records = IndexManager().get(db=db, table=table, condition=condition)
                else:
                    for record in records:
                        if eval(f"not record.get(condition.get('field')) {condition.get('operator')} condition.get('value')"):
                            records.remove(record)
            requested_records =  ({
                requested_field: record.get(requested_field) for requested_field in requested_fields
            } for record in records)
            return requested_records if limit is None else list(requested_records)[:limit]

    def create_index(self, db: str = 'app', table: str = None, param: str = None):
        filepath: str = f'{db}/{table}.json'
        if not exists(path=filepath):
            raise ValueError(f'No {table} doesn\'t exist')
        with open(file=filepath, mode='r') as file:
            data = load(fp=file)
        indexes : list = data.get('indexes')
        fields: list = data.get('fields')

        if not param in fields:
            raise ValueError('This field doesn\'t exist.')
        if not fields[param] == 'number':
            raise ValueError('Indexed field must be a number.')
        if param in indexes:
            raise ValueError('This field is already indexed.')
        data['indexes'].append(param)
        with open(file=filepath, mode='w') as file:
            dump(obj=data, fp=file, indent=4)
