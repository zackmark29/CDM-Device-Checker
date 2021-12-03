# CDM-Device-Checker

Easily parse the cdm device info response from: https://tools.axinom.com/decoders/LicenseRequest

## CHANGELOGS:

## [1.0.1] | 2021.11.04
- Added protobuf for parsing client_id_blob
- Extract challenge directly from client_id_blob file
- Fully refactored for getting/matching device info
- Added arguments (see --help)
- Display the error if found in the response
----

## USAGE:
```
py check.py "challenge base64" or "client_id_blob file"  

py check.py -t/--test (for testing purpose)

add -q/--quite if you don't want to print the results
```
----

## RESULT
```json
{
    "status": "Active",
    "systemId": "4464",
    "securityLevel": "3",
    "manufacturer": "Generic Field Provisioning",
    "model": "Android KLP x86",
    "modelYear": "2013",
    "modelName": "Android SDK built for x86",
    "systemOnChip": "android generic",
    "type": "software",
    "AdditionalInfo": {
        "applicationName": null,
        "architectureName": "x86",
        "buildInfo": "google/sdk_google_phone_x86/generic_x86:7.1.1/NYC/5464897:userdebug/test-keys",
        "companyName": "Google",
        "deviceId": "zdfDCPHaHrBQakqKhEcFqXiLwbblJwg",
        "deviceName": "generic_x86",
        "productName": "sdk_google_phone_x86",
        "widevineCdmVersion": "v4.1.0-android"
    }
}
```
