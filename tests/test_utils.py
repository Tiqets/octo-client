from octo_client.utils import hide_sensitive_data


def test_hide_sensitive_data():
    data = {
        "nonSensitiveData": "foo",
        "otherNonSensitiveData": {
            "isItSensitive": "I don't think so ;)",
        },
        "userAddress": "1234 Main St",
        "userCity": "Anytown",
        "userZip": "12345",
        "userCountry": "USA",
        "userState": "CA",
        "contact": {
            "firstName": "John",
            "lastName": "Doe",
            "userEmail": "foo@boo.com",
            "userPhone": "1234567890",
        },
    }

    result = hide_sensitive_data(data)

    assert result == {
        "nonSensitiveData": "foo",
        "otherNonSensitiveData": {
            "isItSensitive": "I don't think so ;)",
        },
        "userAddress": "[Filtered private data]",
        "userCity": "[Filtered private data]",
        "userZip": "[Filtered private data]",
        "userCountry": "[Filtered private data]",
        "userState": "[Filtered private data]",
        "contact": {
            "firstName": "[Filtered private data]",
            "lastName": "[Filtered private data]",
            "userEmail": "[Filtered private data]",
            "userPhone": "[Filtered private data]",
        },
    }
