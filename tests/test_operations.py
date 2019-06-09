from operations import TableManager


def test_create():
    TableManager().create(db='app', table='toys', fields={'name': 'number'})


def test_drop():
    manager = TableManager()
    manager.create(db='app', table='toys', fields={'name': 'number'})
    manager.drop(db='app', table='toys')


test_drop()
