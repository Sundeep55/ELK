import pytest
import requests

@pytest.fixture(scope='session')
def connector():
    session = requests.Session()
    yield session
    session.close()
