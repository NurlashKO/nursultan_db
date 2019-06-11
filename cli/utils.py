import re

from managers.table_manager import OPERATIONS


def read_next(command: str, pos):
    result = ""
    while pos < len(command) and command[pos] == " ":
        pos += 1
    while pos < len(command) and (command[pos].isdigit() or command[pos].isalpha()):
        result += command[pos]
        pos += 1
    while pos < len(command) and command[pos] == " ":
        pos += 1
    return result, pos


def is_valid_table_and_param_name(name: str):
    return len(name) > 0 and re.match('^[a-z0-9]+$', name) != None


def parse_table_name(query, pos):
    table_name, pos = read_next(query, pos)
    if not is_valid_table_and_param_name(table_name):
        raise ValueError("Systax error. invalid table name")
    return table_name, pos


def parse_condition(query, pos):
    condition = {
        'field': None,
        'operator': None,
        'value': None,
        'limit': None,
    }
    word, pos = read_next(query, pos)
    if not is_valid_table_and_param_name(word):
        raise ValueError('Syntax error. Invalid param name.')
    condition['field'] = word

    op = query[pos]
    pos += 1
    if not op in OPERATIONS:
        raise ValueError('Syntax error. Error parsing SELECT WHERE operation.')
    condition['operator'] = OPERATIONS[op]

    word, pos = read_next(query, pos)
    if not word.isnumeric():
        raise ValueError('Syntax error. Error parsing SELECT WHERE value.')
    condition['value'] = int(word)
    return condition, pos
