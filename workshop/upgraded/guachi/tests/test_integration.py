import os
import pytest

from guachi import ConfigMapper

@pytest.fixture
def mapped_options():
    return {
        'guachi.db.host': 'db_host',
        'guachi.db.port': 'db_port',
        'guachi.web.host': 'web_host',
        'guachi.web.port': 'web_port',
    }

@pytest.fixture
def mapped_defaults():
    return {
        'db_host': 'localhost',
        'db_port': 27017,
        'web_host': 'localhost',
        'web_port': '8080',
    }

@pytest.fixture(autouse=True)
def cleanup_guachi():
    try:
        if os.path.exists('/tmp/guachi'):
            os.remove('/tmp/guachi')
        else:
            os.mkdir('/tmp/guachi')
    except Exception:
        pass
    yield
    try:
        if os.path.exists('/tmp/guachi'):
            os.remove('/tmp/guachi')
        else:
            os.mkdir('/tmp/guachi')
    except Exception:
        pass

def test_access_mapped_configs_empty_dict(mapped_options, mapped_defaults):
    foo = ConfigMapper('/tmp/guachi')
    foo.set_ini_options(mapped_options)
    foo.set_default_options(mapped_defaults)
    foo.set_config({})

    assert foo() == {}
    assert foo.path == '/tmp/guachi/guachi.db'
    assert foo.get_ini_options() == {}
    assert foo.get_default_options() == {}
    assert foo.get_dict_config() == mapped_defaults
    assert foo.stored_config() == {}
    assert foo.integrity_check()

def test_access_mapped_configs_dict(mapped_options, mapped_defaults):
    foo = ConfigMapper('/tmp/guachi')
    foo.set_ini_options(mapped_options)
    foo.set_default_options(mapped_defaults)
    foo.set_config({'db_host': 'example.com', 'db_port': 0})

    assert foo() == {}
    assert foo.path == '/tmp/guachi/guachi.db'
    assert foo.get_ini_options() == {}
    assert foo.get_default_options() == {}
    assert foo.get_dict_config() == {
        'web_port': '8080',
        'web_host': 'localhost',
        'db_host': 'example.com',
        'db_port': 0
    }
    assert foo.stored_config() == {}
    assert foo.integrity_check()
