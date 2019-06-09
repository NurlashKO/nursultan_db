import re


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
