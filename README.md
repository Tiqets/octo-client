# OCTO API client

Python HTTP client for OCTO (Open Connection for Tourism) APIs.

More info at [octospec.com](https://octospec.com/)

API Specification: https://docs.octo.travel/docs/octo/r6gduoa5ah5ne-octo-api

## Installation

    pip install octo-api-client

## Requirements

* Python v3.7+

## Development

### Getting started

    $ pip install poetry
    $ poetry install

### Running tests and linters

To run linters:

    $ poetry run ruff octo_client
    $ poetry run mypy octo_client

To run tests:

    $ poetry run pytest


## Usage

```
from octo_client import OctoClient

client = OctoClient('https://octo-api.mysupplier.com', 'MY-SECRET_TOKEN')
client.get_suppliers()
```
