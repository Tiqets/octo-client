import pytest
import responses

from icf_client import exceptions


def test_incorrect_supplier_id(client, mocked_responses):
    with pytest.raises(exceptions.InvalidRequest):
        client.get_products(supplier_id='foo')


def test_incorrect_api_key(client, mocked_responses):
    mocked_responses.add(responses.GET, 'https://api.my-booking-platform.com/v1/products', status=403)
    with pytest.raises(exceptions.Unauthorized):
        client.get_products(supplier_id='0001')


def test_bad_request(client, mocked_responses):
    mocked_responses.add(responses.GET, 'https://api.my-booking-platform.com/v1/products', status=403)
    with pytest.raises(exceptions.Unauthorized):
        client.get_products(supplier_id='0001')


@pytest.mark.parametrize('status_code', (404, 500))
def test_api_exception(status_code, client, mocked_responses):
    mocked_responses.add(responses.GET, 'https://api.my-booking-platform.com/v1/products', status=status_code)
    with pytest.raises(exceptions.ApiError):
        client.get_products(supplier_id='0001')
