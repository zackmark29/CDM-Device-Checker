# CDM-Device-Checker
---

Easily parse the cdm device info response from: https://tools.axinom.com/decoders/LicenseRequest  
SITE STATUS: `ACTIVE`

---
## CHANGELOGS:

## [1.0.3] | 2021-12-21

- python 3.6-later compatibility
- Removed dictionary merge operator "|"
- Removed test argument. Just load the test challenge from "challenge.txt" (e.g. py check.py chalenge.txt)

---

- Added base64 validation
- Display if revoked or active
- Modified output file name with additional info (e.g. ChromeCDM-20122-L3-[ACTIVE].json)
- Can now load challenge base64 from txt file or client_id_blob with/without extension .bin
- Final output file path will be on the location of input file path
- And some minor changes

---

## [1.0.2] | 2021-12-09

- Fixed matching client type
- Print device info by default. Only use quite option for client_id_blob info
- Save challenge base64 to txt file if parsing client_id_blob (so you can verify from https://tools.axinom.com/decoders/LicenseRequest)

---

## [1.0.1] | 2021-12-04

- Added protobuf for parsing client_id_blob
- Extract challenge directly from client_id_blob file
- Fully refactored for getting/matching device info
- Added arguments (see --help)
- Display the error if found in the response

---

## USAGE

```
py.check.py "challenge base64 string"
py.check.py "device_client_id_blob"
py.check.py "challenge.txt"

add -q/--quite if you don't want to print the results
```

---

## RESULT

```json
{
    "status": "ACTIVE",
    "ForTestingOnly": "No",
    "systemId": "4464",
    "securityLevel": "LEVEL_3",
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
