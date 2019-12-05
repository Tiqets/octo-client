import responses

from icf_client import models as m


def test_suppliers_list(client, mocked_responses):
    mocked_responses.add(responses.GET, 'http://fake-api.local/suppliers', json=[
        {
            "id": "0001",
            "name": "Acme Tour Co.",
            "endpoint": "https://api.my-booking-platform.com/v1",
            "contact": {
                "website": "https://acme-tours.co.fake",
                "email": "info@acme-tours.co.fake",
                "telephone": "+1 888-555-1212",
                "address": "123 Main St, Anytown USA"
            }
        }
    ])
    suppliers = client.get_suppliers()
    assert suppliers == [
        m.Supplier(
            id='0001',
            name='Acme Tour Co.',
            endpoint='https://api.my-booking-platform.com/v1',
            contact=m.SupplierContact(
                address='123 Main St, Anytown USA',
                email='info@acme-tours.co.fake',
                telephone='+1 888-555-1212',
                description=None,
                website='https://acme-tours.co.fake'
            )
        )
    ]
    assert len(mocked_responses.calls) == 1, 'Too many requests'
    assert mocked_responses.calls[0].request.url == 'http://fake-api.local/suppliers'
    assert mocked_responses.calls[0].request.headers['Authorization'] == 'Bearer bar'
