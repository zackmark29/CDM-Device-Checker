from os import device_encoding
import sys
import re
import json
import argparse
from pathlib import Path
from requests import Session

TOKEN = 'CfDJ8J3HFu-R0HlNvutoAYRa68EjeSliPuQR8Ogt7niNVzgha2wJQ1jDNyCmxzGv95aKF911acVDx12U1BFi0z-JcR2taHJKjY6X0qWq2H5MD65oEZJYGUkzop-l7rOa8eJJKs1V9BjJZDjLPmdOsXmquBU'
COOKIE = '.AspNetCore.Antiforgery.pcAz0O62JyE=CfDJ8J3HFu-R0HlNvutoAYRa68FIgcbDEr06bq4cJyWCC5Pl6SyEHKMWynbvPsY7pf8KYwtuZLNZMHoMv8uhJxOUyWYpCA-yrH3NW8uH0pMACoc_u8afV2xtezmcOmG53Qe9uq8U7Hv-84UWvRRraNvbsQI'


def fetch_challenge_data(challenge: str) -> str:
    res = Session().post(
        url='https://tools.axinom.com/decoders/LicenseRequest',
        data={
            'LicenseRequestEncoding': 'Base64',
            'LicenseRequest': challenge,
            '__RequestVerificationToken': TOKEN
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://tools.axinom.com/',
            'Accept': '*.*',
            'Cookie': COOKIE
        }
    )
    if not res.ok:
        exit(res.text)

    return res.text


def parse_challenge_data(data: str) -> dict:
    print('[INFO]: ', 'Getting license request info')

    errors = re.compile(r'remove-sign.+>\s(.+)[<^.]')

    for error in errors.findall(data):
        print('[ERROR]:', error.replace('&quot;', '"'))

    print('\n[INFO]: ', 'Parsing device info')

    td = r'>(.+)<\/td>.*\n.+<td>'
    tags = re.findall(td + r'(.+)[<^]', data)
    divs = re.findall(td + r'\n.+<div>(.+)[<^]', data)

    return dict(
        (x, y.replace('&#x0;', ''))
        for x, y in tags + divs
    )


def get_device_info(challenge: str, quite: bool) -> None:

    data = fetch_challenge_data(challenge)
    tags = parse_challenge_data(data)

    def get(tag: str) -> str:
        match = tags.get(tag, "")

        if match == "":
            print(f'[WARN]:  No match found for: {tag}')

        return match

    device_name = get('device_name')
    system_id = get('System ID')

    if system_id == "":
        sys.exit(f'[ERROR]: System ID is not found. '
                 'Looks like your challenge data is invalid')

    data = {
        'status': get('Status').upper(),
        'ForTestingOnly': get('For Testing Only'),
        'systemId': system_id,
        'securityLevel': {
            '1': 'LEVEL_1',
            '3': 'LEVEL_3'
        }.get(get('Security Level')),
        'manufacturer': get('Manufacturer'),
        'model': get('Model'),
        'modelYear': get('Model Year'),
        'modelName': get('model_name'),
        'systemOnChip': get('System on Chip'),
        'type': get('Type'),
        'AdditionalInfo': {
            'applicationName': get('application_name'),
            'architectureName': get('architecture_name'),
            'buildInfo': get('build_info'),
            'companyName': get('company_name'),
            'deviceId': get('device_id'),
            'deviceName': device_name,
            'productName': get('product_name'),
            'widevineCdmVersion': get('widevine_cdm_version')
        }
    }

    file_name = Path(f'{device_name}-{system_id}-DeviceInfo.json')
    data = json.dumps(data, indent=4, ensure_ascii=False)
    file_name.write_text(data)

    if not quite:
        print(data)

    print('\n[INFO]: ', f'Saving device info to: {file_name}')


def main(arg):
    if arg.test:
        challenge = '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'
        print('[INFO]: ', 'Using the test challenge')
    elif 'client_id_blob' in arg.challenge:
        from cdm import extract_challenge
        print('[INFO]: ', 'Extracting challenge info from client_id_blob')
        challenge = extract_challenge(arg.challenge, arg.quite)
    else:
        print('[INFO]: ', 'Using challenge from argument')
        challenge = arg.challenge

    get_device_info(challenge, arg.quite)


if __name__ == '__main__':
    # Just added arguments for future updates
    parser = argparse.ArgumentParser("Simple util to get CDM device info from license request/challenge.")
    parser.add_argument(dest='challenge', nargs='?', default=None, help='Challenge or license request')
    parser.add_argument('-t', '--test', default=False, action='store_true', help='Use the test challenge')
    parser.add_argument('-q', '--quite', default=False, action='store_true', help='Don\'t print the results')
    main(parser.parse_args())
