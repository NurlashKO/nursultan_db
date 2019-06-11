from .utils import read_next, is_valid_table_and_param_name, parse_table_name, parse_condition


def parse_create_table(query, pos):
    table_name, pos = parse_table_name(query, pos)
    if query[pos] != '(':
        raise ValueError('Syntax error. Can\'t parse parameter list \'(\' character not found. ')
    pos += 1
    params = {}
    while query[pos] != ')':
        param, pos = read_next(query, pos)
        param_type, pos = read_next(query, pos)
        if query[pos] != ',' and query[pos] != ')':
            raise ValueError(
                'Syntax error. Params list should be separated with \',\' and finished with \')\' character.')
        if not is_valid_table_and_param_name(param):
            raise ValueError('Syntax error. Invalid param name.')
        if not is_valid_table_and_param_name(param_type):
            raise ValueError('Syntax error. Invalid param type name.')
        if not param_type in ('number', 'str'):
            raise ValueError("Error. Invalid param type.")
        if param in params:
            raise ValueError("Error. Two params with the same type.")
        params[param] = param_type
        if query[pos] == ',':
            pos += 1

    pos += 1
    command, pos = read_next(query, pos)
    if len(command) > 0 or query[pos] != ';':
        raise ValueError("Syntax error. Extra data at the end of CREATE TABLE command.")
    return table_name, params


def parse_select(query, pos):
    params = []
    condition = {
        'field': None,
        'operator': None,
        'value': None,
        'limit': None,
    }
    while True:
        word, pos = read_next(query, pos)
        if not is_valid_table_and_param_name(word):
            raise ValueError('Syntax error. Invalid param name.')
        params.append(word)
        if query[pos] != ',':
            word, pos = read_next(query, pos)
            if word == "from":
                break
            else:
                raise ValueError('Syntax error. Param list should be finished with keyword \'FROM\'.')
        else:
            pos += 1

    if len(params) == 0:
        raise ValueError("Error. Nothing is selected")
    table_name, pos = parse_table_name(query, pos)
    if query[pos] == ';':
        return table_name, params, condition

    word, pos = read_next(query, pos)
    if word == 'where':
        condition, pos = parse_condition(query, pos)
        word, pos = read_next(query, pos)

    if word == 'limit':
        word, pos = read_next(query, pos)
        if not word.isnumeric():
            raise ValueError('Syntax error. Error parsing SELECT LIMIT value.')
        condition['limit'] = int(word)

    if query[pos] != ';':
        raise ValueError("Syntax error. Extra data at the end of DROP TABLE command.")
    return table_name, params, condition


def parse_delete_from(query, pos):
    condition = {
        'field': None,
        'operator': None,
        'value': None,
        'limit': None,
    }
    word, pos = read_next(query, pos)
    if word != 'from':
        raise ValueError('Syntax error. Error parsing at FROM.')
    table_name, pos = parse_table_name(query, pos)
    word, pos = read_next(query, pos)

    if word == 'where':
        condition, pos = parse_condition(query, pos)
    else:
        raise ValueError('Syntax error. Error parsing WHERE.')
    if query[pos] != ';':
        raise ValueError("Syntax error. Extra data at the end of DROP TABLE command.")

    return table_name, condition


def parse_create_index(query, pos):
    table_name, pos = parse_table_name(query, pos)
    word, pos = read_next(query, pos)
    if word != 'on':
        raise ValueError('Syntax error. Error parsing string ON at CREATE INDEX.')
    param, pos = read_next(query, pos)
    if query[pos] != ';':
        raise ValueError("Syntax error. Extra data at the end of DROP TABLE command.")

    return table_name, param


def parse_drop_table(query, pos):
    command, pos = read_next(query, pos)
    if command != 'table':
        raise ValueError('Syntax error. At \'table\'')
    table_name, pos = parse_table_name(query, pos)
    if query[pos] != ';':
        raise ValueError("Syntax error. Extra data at the end of DROP TABLE command.")
    return table_name
