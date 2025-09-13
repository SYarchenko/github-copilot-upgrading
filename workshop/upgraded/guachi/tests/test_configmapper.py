import os
import pytest

from guachi import ConfigMapper
from guachi.database import dbdict

DEFAULT_CONFIG = {
    'frequency': 60,
    'master': 'False',
    'host': 'localhost',
    'ssh_user': 'root',
    'ssh_port': 22,
    'hosts_path': '/opt/pacha',
    'hg_autocorrect': 'True',
    'log_enable': 'False',
    'log_path': 'False',
    'log_level': 'DEBUG',
    'log_format': '%(asctime)s %(levelname)s %(name)s %(message)s',
    'log_datefmt': '%H:%M:%S'
}

@pytest.fixture(autouse=True)
def cleanup_db():
    try:
        os.remove('/tmp/guachi.db')
        os.remove('/tmp/foo_guachi.db')
    except Exception:
        pass
    yield
    try:
        os.remove('/tmp/guachi.db')
        os.remove('/tmp/foo_guachi.db')
    except Exception:
        pass

def test_init():
    foo = ConfigMapper('/tmp')
    expected = '/tmp/guachi.db'
    actual = foo.path
    assert actual == expected

def test__call__():
    foo = ConfigMapper('/tmp')
    actual = foo()
    expected = {}
    assert actual == expected

def test_set_ini_options():
    foo = ConfigMapper('/tmp')
    my_config = {'config.db.port': 'db_port'}
    foo.set_ini_options(my_config)
    db = dbdict(path='/tmp/guachi.db', table='_guachi_options')
    expected = my_config
    actual = db.get_all()
    assert actual == expected

def test_set_default_options():
    foo = ConfigMapper('/tmp')
    my_config = {'db_port': 1234}
    foo.set_default_options(my_config)
    db = dbdict(path='/tmp/guachi.db', table='_guachi_defaults')
    expected = my_config
    actual = db.get_all()
    assert actual == expected

def test_get_ini_options():
    foo = ConfigMapper('/tmp')
    my_config = {'config.db.port': 'db_port'}
    foo.set_ini_options(my_config)
    defaults = foo.get_ini_options()
    actual = defaults['config.db.port']
    expected = 'db_port'
    assert actual == expected

def test_get_default_options():
    foo = ConfigMapper('/tmp')
    my_config = {'db_port': 1234}
    foo.set_default_options(my_config)
    defaults = foo.get_default_options()
    actual = defaults['db_port']
    expected = 1234
    assert actual == expected

def test_path_verify_file():
    foo = ConfigMapper('/tmp/foo_guachi.db')
    actual = foo._path_verify('/tmp/foo_guachi.db')
    expected = '/tmp/foo_guachi.db'
    assert actual == expected

def test_path_verify_dir():
    foo = ConfigMapper('/tmp')
    actual = foo._path_verify('/tmp')
    expected = '/tmp/guachi.db'
    assert actual == expected

def test_update_config_dict_empty():
    foo = ConfigMapper('/tmp')
    foo.update_config({})
    db = dbdict('/tmp/guachi.db')
    actual = db.get_all()
    expected = {}
    assert actual == expected

def test_update_config_dict():
    foo = ConfigMapper('/tmp')
    foo.update_config(DEFAULT_CONFIG)
    db = dbdict('/tmp/guachi.db')
    actual = db.get_all()
    expected = DEFAULT_CONFIG
    assert actual == expected

def test_set_config_dict_empty():
    foo = ConfigMapper('/tmp')
    foo.set_config({})
    db = dbdict('/tmp/guachi.db')
    actual = db.get_all()
    expected = {}
    assert actual == expected

def test_set_config_dict():
    foo = ConfigMapper('/tmp')
    foo.set_config(DEFAULT_CONFIG)
    db = dbdict('/tmp/guachi.db')
    actual = db.get_all()
    expected = DEFAULT_CONFIG
    assert actual == expected

def test_get_dict_config():
    foo = ConfigMapper('/tmp')
    foo.set_config(DEFAULT_CONFIG)
    actual = foo.get_dict_config()
    expected = DEFAULT_CONFIG
    assert actual == expected

def test_integrity_check():
    foo = ConfigMapper('/tmp')
    foo.set_config(DEFAULT_CONFIG)
    actual = foo.integrity_check()
    assert actual

def test_stored():
    foo = ConfigMapper('/tmp')
    bar = foo.stored_config()
    assert bar == {}

def test_stored_get_data():
    foo = ConfigMapper('/tmp')
    bar = foo.stored_config()
    bar['a'] = 1
    assert bar == {'a': 1}


