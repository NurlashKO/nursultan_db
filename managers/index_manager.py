import os
from json import load
from typing import Dict

from cli.b_tree import BTree
from cli.db_index import DatabaseIndex

class Singleton(type):
    _instances = {}

    def call(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).call(*args, **kwargs)
        return cls._instances[cls]

class IndexManager(metaclass=Singleton):
    def __init__(self, db: str = 'app'):
        self.indexes = {}
        directory = os.fsencode(f'{db}/.')

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                with open(file=f'./{db}/{filename}', mode='r+') as table:
                    data = load(fp=table)
                    db_table = filename.replace('.json', '')
                    indexes: list = data.get('indexes')
                    records: list = data.get('records')
                    for index in indexes:
                        for record in records:
                            if not self.index_key(table=filename) in self.indexes:
                                self.indexes = BTree(2)
                            self.indexes[self.index_key(db=db, table=db_table)].insert(
                                DatabaseIndex(record[index], record))

    def index_key(self, db: str = 'app', table: str = None):
        return f'{db}/{table}'

    def get(self, db: str = 'app', table: str = None, condition: Dict = None):
        result = []
        for record in self.indexes[self.index_key(db=db, table=table)]:
            if eval(f"record.get(condition.get('field')) {condition.get('operator')} condition.get('value')"):
                result.append(record)
        return result
