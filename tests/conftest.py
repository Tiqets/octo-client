import json
import os

import pytest
import responses

from octo_client import OctoClient


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def load_json_response(filename: str):
    """
    Loading JSON file located in the responses folder.
    """
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "responses", filename)
    with open(file_path) as json_file:
        return json.load(json_file)


@pytest.fixture
def client(mocked_responses):
    suppliers_response = load_json_response("suppliers.json")
    mocked_responses.add(responses.GET, "http://fake-api.local/suppliers", json=suppliers_response)
    return OctoClient("http://fake-api.local", "secret-token")
