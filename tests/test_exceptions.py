import pytest
import responses

from icf_client import exceptions


def test_incorrect_api_key(client, mocked_responses):
    mocked_responses.add(responses.GET, 'http://fake-api.local/suppliers', status=403)
    with pytest.raises(exceptions.Unauthorized):
        client.get_suppliers()


def test_bad_request(client, mocked_responses):
    mocked_responses.add(responses.GET, 'http://fake-api.local/suppliers', status=403)
    with pytest.raises(exceptions.Unauthorized):
        client.get_suppliers()


@pytest.mark.parametrize('status_code', (404, 500))
def test_api_exception(status_code, client, mocked_responses):
    mocked_responses.add(responses.GET, 'http://fake-api.local/suppliers', status=status_code)
    with pytest.raises(exceptions.ApiError):
        client.get_suppliers()
