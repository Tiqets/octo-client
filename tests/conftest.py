import pytest
import responses

from icf_client import IcfClient


@pytest.fixture
def client():
    return IcfClient('http://fake-api.local', 'bar')


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps
