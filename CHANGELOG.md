# Changelog

## 1.0.4

- Fix for logging when receiving a non-JSON response

## 1.0.3

- Automatic release of package on merge to master.

## 1.0.2

- Change of argument type in raise_for_status method from bytes to string.
- _raise_for_status will now receive response.text instead of response.content

## 1.0.1

- more fixes to for logging issue when logs exceeded log_size_limit.

## 1.0.0

- fix for logging issue when logs exceeded log_size_limit.

## 0.1.9

- moved log size limit to an optional variable set when initializing client.

## 0.1.8

- Remove responses that exceed DD limit.

## 0.1.7

- Replacing dacite with tonalite

## 0.1.6

- Fix handle attribute error when supplier return internal error with status code 200.

## 0.1.5

- Marking the Product.capabilities field as optional.


## 0.1.4

- Fix for sending requests without the JSON body.

## 0.1.3

- Adding `extra_fields` to each model to keep additional fields used by different capabilities.
