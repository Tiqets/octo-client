# OCTo API client

Python HTTP client for OCTo (Open Connection for Tourism) APIs.

More info at [octospec.com](https://octospec.com/)

## Installation

    pip install octo-api-client

## Requirements

* Python v3.7+

## Development

### Getting started

    $ virtualenv venv _--python=python3.7
    $ . venv/bin/activate
    $ python setup.py develop

### Running tests

Install requirements:

    $ pip install -e '.[tests]'

To run all linters and tests:

    $ tox

If you want to run a specific test

    $ pytest -k test_name


## Usage

```
from octo_client import OctoClient

client = OctoClient('https://octo-api.mysupplier.com', 'MY-SECRET_TOKEN')
client.get_suppliers()
```
