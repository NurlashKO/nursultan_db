import sys
from os.path import dirname

from managers.index_manager import IndexManager

sys.path.append(dirname(__file__) + '../')

from cli.parsers import parse_create_table, parse_drop_table, parse_select, parse_delete_from, parse_create_index
from cli.utils import read_next
from managers.table_manager import TableManager


# А. create table mytable (param1 number, param2 number, param3 string);
def query_create_table(query, pos):
    table_name, params = parse_create_table(query, pos)
    TableManager().create(table=table_name, fields=params)
    return table_name, params


# В. create index table_name on param1;
def query_create_index(query, pos):
    table_name, param = parse_create_index(query, pos)
    TableManager().create_index(table=table_name, param=param)
    pass


def query_create(query, pos):
    command, pos = read_next(query, pos)
    if command == "table":
        return query_create_table(query, pos)
    elif command == "index":
        return query_create_index(query, pos)
    else:
        raise ValueError("Syntax error after CREATE")


# Б. select param1, param3 from mytable where param2 > 2 limit 10;
def query_select(query, pos):
    table_name, params, condition = parse_select(query, pos)
    for value in TableManager().select(table=table_name, requested_fields=params, conditions=(condition,),
                                       limit=condition['limit']):
        print(value)


# Г. delete from maytable where param2 < 2;
def query_delete(query, pos):
    pass


def query_insert(query, pos):
    pass


# Д. drop table mytable;
def query_drop(query, pos):
    table_name = parse_drop_table(query, pos)
    TableManager().drop(table=table_name)
    return table_name


def process_query(query):
    query = query.lower()
    command, pos = read_next(query, 0)
    if command == "insert":
        return query_insert(query, pos)
    if command == "create":
        return query_create(query, pos)
    elif command == "select":
        query_select(query, pos)
    elif command == "delete":
        query_delete(query, pos)
    elif command == "drop":
        query_drop(query, pos)
    else:
        raise ValueError('Syntax error. Unrecognized query.')


if __name__ == '__main__':
    try:
        process_query(input().lower())
    except ValueError as error:
        print(error)
