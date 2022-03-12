# CDM-Device-Checker
---

Easily parse the cdm device info response from: https://tools.axinom.com/decoders/LicenseRequest  

AXINOM'S LICENSE REQUEST STATUS: `MAINTENANCE/NOT AVAILABLE`

---
## **TIPS**:
## Add context menu for easy check from challange.txt or client_id_blob

INSTRUCTIONS:

- Just double click the **`add_context_menu.bat`** to automatically add context menu into your registry
- You can also change the context title ("Check Client Id Blob") inside the bat file
- Now you can do like the ss below or you can just drag and drop the file in the bat file

`From client_id_blob`

![image](https://user-images.githubusercontent.com/62680932/147465896-bd33c653-96a4-4220-af63-6e0750c6ec66.png)


`From challange.txt`

![image](https://user-images.githubusercontent.com/62680932/147467317-3adf2f40-78dc-4a82-9146-b642395308d0.png)

---

## **CHANGELOGS**

## [1.0.7] | 2022-01-28

- Automatically run "add_context_menu.bat" as admin
- Don't write challenge.txt automatically
- Print client id blob basic info if --quite mode enabled
- Prompt to load challenge from "challenge.txt" if input is empty
- Colored is now optional (see config.py)
    - NOTE: For windows 7, if you want to print colored text, you can use **[ansicon](https://github.com/adoxa/ansicon/releases)**.
    - INSTRUCTIONS:
        - Extract the zip file
        - Take the folder (x86 if you are using 32bit / x64 if 64bit) and place somewhere and then add the binary to your **Environment Variables**
        - Simply run for the first time in your cmd: **`ansicon -i`**
        - Now it should be injected to your cmd and colored text should show normally.

---

## [1.0.6] | 2022-01-23

- Saving file is now optional (add --save arg to save the file)
- Added os_version info

---

## [1.0.5] | 2022-01-08

- Removed context_menu.reg and replaced with batch file instead to automatically assign the current check.bat full path
- Added current full path in check.bat instead of adding manually
- Renamed proto to wv_proto to avoid conflict from proto import
- colored output for device info and logger
- You can edit the output file name format (see in config.py)
- And some little changes

SAMPLE OUTPUT:

![image](https://user-images.githubusercontent.com/62680932/148638846-c10c90d0-7251-4287-9ae2-6c886575f4a6.png)

---

## [1.0.4] | 2021-12-27

- [1087720375](https://github.com/zackmark29/CDM-Device-Checker/issues/2#issue-1087720375) |
Added registry context menu for easy check from challange.txt or client_id_blob
- [1087669514](https://github.com/zackmark29/CDM-Device-Checker/issues/1#issue-1087669514) |
Fixed iterating on NoneType item

---

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

## **USAGE**

```
py.check.py "challenge base64 string"
py.check.py "device_client_id_blob"
py.check.py "challenge.txt"

add -q/--quite if you don't want to print the results
```

---

## **RESULT**

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
