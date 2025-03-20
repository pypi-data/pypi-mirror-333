import pytest
from protoai.config.base import load_secret


def test_load_secret_success():
    secret = load_secret()
    print(secret)
    assert len(secret) > 0


def test_load_secret_raise_file_not_found():
    with pytest.raises(FileNotFoundError) as exc_info:
        secret = load_secret('no exists file')


def test_load_secret_raise_key_error():
    with pytest.raises(KeyError) as exc_info:
        secret = load_secret('README.md')
