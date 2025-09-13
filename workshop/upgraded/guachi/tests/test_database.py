import os
import sqlite3
import pytest
from guachi import database

@pytest.fixture(autouse=True)
def cleanup_db():
    yield
    try:
        os.remove('/tmp/test_guachi')
    except Exception:
        pass

def test_create_database():
    foo = database.dbdict('/tmp/test_guachi')
    assert os.path.isfile('/tmp/test_guachi')

def test_init():
    foo = database.dbdict('/tmp/test_guachi')
    assert foo.db_filename == '/tmp/test_guachi'
    assert foo.table == '_guachi_data'
    assert foo.select_value == 'SELECT value FROM _guachi_data WHERE key=?'
    assert foo.select_key == 'SELECT key FROM _guachi_data WHERE key=?'
    assert foo.update_value == 'UPDATE _guachi_data SET value=? WHERE key=?'
    assert foo.insert_key_value == 'INSERT INTO _guachi_data (key,value) VALUES (?,?)'
    assert foo.delete_key == 'DELETE FROM _guachi_data WHERE key=?'

def test_init_guachi_table():
    foo = database.dbdict('/tmp/test_guachi', table='_guachi_options')
    assert foo.table == '_guachi_options'

def test_get_item_keyerror():
    foo = database.dbdict('/tmp/test_guachi')
    with pytest.raises(KeyError):
        foo.__getitem__('meh')

def test_get_item():
    foo = database.dbdict('/tmp/test_guachi')
    foo['bar'] = 'beer'
    assert foo['bar'] == 'beer'

def test_setitem_update():
    foo = database.dbdict('/tmp/test_guachi')
    foo['a'] = 1
    foo['a'] = 2
    assert foo['a'] == 2

def test_close_db():
    foo = database.dbdict('/tmp/test_guachi')
    foo['bar'] = 'beer'
    foo._close()
    with pytest.raises(sqlite3.ProgrammingError):
        foo.__setitem__('bar', {'a':'b'})

def test_setitem_typeerror():
    foo = database.dbdict('/tmp/test_guachi')
    with pytest.raises(sqlite3.ProgrammingError):
        foo.__setitem__('bar', {'a':'b'})

def test_delitem_keyerror():
    foo = database.dbdict('/tmp/test_guachi')
    with pytest.raises(KeyError):
        foo.__delitem__('meh')

def test_delitem():
    foo = database.dbdict('/tmp/test_guachi')
    foo['bar'] = 'beer'
    assert foo['bar'] == 'beer'
    del foo['bar']
    with pytest.raises(KeyError):
        foo.__delitem__('bar')

def test_key_empty():
    foo = database.dbdict('/tmp/test_guachi')
    assert foo.keys() == []

def test_keys_get_none():
    foo = database.dbdict('/tmp/test_guachi')
    assert foo.get('does-not-exist') is None

def test_keys_get_value():
    foo = database.dbdict('/tmp/test_guachi')
    foo['bar'] = 'value'
    assert foo.get('bar') == 'value'

def test_keys_get_value_w_default():
    foo = database.dbdict('/tmp/test_guachi')
    assert foo.get('foobar', True)

def test_keys():
    foo = database.dbdict('/tmp/test_guachi')
    foo['bar'] = 'beer'
    assert foo.keys() == ['bar']

def test_integrity_check_true():
    foo = database.dbdict('/tmp/test_guachi')
    assert foo._integrity_check()

