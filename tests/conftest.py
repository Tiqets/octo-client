import pytest
import responses

from octo_client import OctoClient


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def client(mocked_responses):
    mocked_responses.add(responses.GET, 'http://fake-api.local/suppliers', json=[
        {
            'id': '0001',
            'name': 'Acme Tour Co.',
            'endpoint': 'https://api.my-booking-platform.com/v1',
            'contact': {
                'website': 'https://acme-tours.co.fake',
                'email': 'info@acme-tours.co.fake',
                'telephone': '+1 888-555-1212',
                'address': '123 Main St, Anytown USA'
            }
        }
    ])
    return OctoClient('http://fake-api.local', 'bar')
