# Changelog

## 1.1.7

- Handle list data when hidding client sensitive data

## 1.1.6

- Fix client displaying sensitive data in logs

## 1.1.5

- Update client methods to accept a `headers` parameter to forward HTTP request headers.

## 1.1.4

- Add flag to log requests

## 1.1.3

- Update the `get_calendar` method to remove the parameter `availability_ids`.

## 1.1.2

- Update the client to add a function to build the endpoint's URL for requests to a given supplier.

## 1.1.1

- Convert unknown values for `UnitType` `Enum` to `UnitType.OTHER`.
- Convert unknown values for `DeliveryFormat` `Enum` to `DeliveryFormat.OTHER`.
- Deprecate `DeliveryFormat.PKPASS_URL` and replace it by `DeliveryFormat.OTHER`.
- Support alternative values for the `RequiredContactField` Enum.

## 1.1.0

- Updating the client to the current OCTO version (v1.0)

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
