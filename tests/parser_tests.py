from ..cmd import  process_query


def test_create_table_parser():
    assert process_query("CrEate TABLE Muslim (age int, id int, test str);") == \
        ('muslim', {'age': 'int', 'id': 'int', 'test': 'str'})
