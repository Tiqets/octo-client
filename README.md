# OCTO API client

Python HTTP client for OCTO (Open Connection for Tourism) APIs.

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
