__version__ = '1.0.7'

import sys
import re
import json
import base64
import binascii
import argparse

from pathlib import Path
from requests import Session
from config import (
    colored_print,
    SITE,
    TOKEN,
    COOKIE,
    info,
    error,
    printl,
    warn,
    FILE_NAME_FORMAT,
    FILE_NAME_SEPARATOR,
)
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)


def fetch_challenge_data(challenge: str) -> str:
    info('Fetching license request data')
    res = Session().post(
        url=SITE,
        data={
            'LicenseRequestEncoding': 'Base64',
            'LicenseRequest': challenge,
            '__RequestVerificationToken': TOKEN
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://tools.axinom.com/',
            'Accept': '*/*',
            'Cookie': COOKIE
        },
        verify=False
    )
    if not res.ok:
        error(res.text)

    return res.text


def parse_challenge_data(data: str) -> dict:
    info('Parsing device info')

    errors = re.compile(r'remove-sign.+>\s(.+)[<^.]')

    for err in errors.findall(data):
        error('[AXINOM]: ' + err.replace('&quot;', '"'), False)

    td = r'>(.+)<\/td>.*\n.+<td>'
    tags = re.findall(td + r'(.+)[<^]', data)
    divs = re.findall(td + r'\n.+<div>(.+)[<^]', data)

    if not tags and not divs:
        error('No any result found. Possible problem are: '
              'Invalid challenge, Invalid RegEx, Site has been updated or currently not available')

    # Since it has mutlitple Type result, just get the second one
    client_type = [x for x in tags if 'Type' in x][0][1]

    dic = dict(
        (x, y.replace('&#x0;', ''))
        for x, y in tags + divs
    )
    dic.update({'Type': client_type})
    return dic


def get_device_info(challenge: str, cwd: Path, save: bool) -> None:

    main_info = fetch_challenge_data(challenge)
    tags = parse_challenge_data(main_info)

    def get(tag: str) -> str:
        match = tags.get(tag, "")

        if match == "":
            warn(f'No match found for: {tag}')

        return match

    system_id = get('System ID')

    if system_id is None:
        error(f'System ID is not found. '
              'Looks like your challenge data is invalid')

    sec_level = get('Security Level')

    main_info = {
        'status': get('Status').upper(),
        'forTestingOnly': get('For Testing Only'),
        'systemId': system_id,
        'securityLevel': f'LEVEL_{sec_level}',
        'manufacturer': get('Manufacturer'),
        'model': get('Model'),
        'modelYear': get('Model Year'),
        'modelName': get('model_name'),
        'systemOnChip': get('System on Chip'),
        'type': get('Type')
    }
    additional_info = {
        'applicationName': get('application_name'),
        'architectureName': get('architecture_name'),
        'buildInfo': get('build_info'),
        'companyName': get('company_name'),
        'deviceId': get('device_id'),
        'deviceName': get('device_name'),
        'productName': get('product_name'),
        'osVersion': get('os_version'),
        'widevineCdmVersion': get('widevine_cdm_version')
    }

    printl()
    info("AXINOM'S DEVICE INFO RESPONSE:")
    printl()
    colored_print(main_info)
    print()
    colored_print(additional_info)

    printl(end='\n')

    if not save:
        sys.exit()

    file_name = format_file_name(main_info)

    main_info.update({'additionalInfo': additional_info})
    main_info = json.dumps(main_info, indent=4, ensure_ascii=False)
    output = cwd / f'{file_name}.json'
    output.write_text(main_info)

    info(f'Output File Name: "{file_name}"')
    info(f'Device info has been saved to: "{output}"')
    sys.exit()


def format_file_name(data: dict) -> str:
    keys = []
    for name in FILE_NAME_FORMAT.split(' '):
        # removed first the square brackets
        key = re.sub(r'[\[\]]', '', name)
        key = data.get(key)

        if key is None:
            continue

        # just use square brackets if it is set in the template
        if re.match(r'(\[.+\])', name):
            key = f'[{key}]'

        # replace LEVEL_1/3
        key = str(key).replace('LEVEL_', 'L').replace(' ', '-')
        keys.append(key)

    return FILE_NAME_SEPARATOR.join(keys)


def is_base64(txt: str) -> bool:
    try:
        base64.b64decode(txt, validate=True)
        return True
    except binascii.Error:
        return False


def main(arg):
    txt_file = 'challenge.txt'

    if arg.challenge is None:
        error('Challenge/Client Id Blob input is empty.', False)
        if str(input(' ' * 5 + f'Do you want to load the default challenge from "{txt_file}" instead? '
                     '(Press y/Y if yes or any key to exit): ')).lower() != 'y':
            sys.exit()

        default_chal = Path(txt_file)

        if not default_chal.exists():
            error(f'"{txt_file}" does not exist')

        arg.challenge = default_chal.read_text()

    # check if the first arg is a valid base64 else assume that it is a file instead
    if is_base64(arg.challenge):
        # info('Using input challenge base64')
        get_device_info(arg.challenge, Path().cwd(), arg.save)

    # file argument
    chal_path = Path(arg.challenge)

    if not chal_path.exists():
        error(f'"{chal_path}" does not exist')

    # device_client_id_blob
    if 'blob' in arg.challenge or chal_path.suffix == '.bin':
        from cdm import parse_client_id_blob

        info(f'Parsing client id blob from: "{chal_path}"')
        challenge = parse_client_id_blob(chal_path, arg.quite)

        if arg.save:
            info('Writing challenge base64 to "challenge.txt" file')
            Path(txt_file).write_text(challenge)

    # any txt file name with .txt extension
    elif chal_path.suffix == '.txt':
        info(f'Loading challenge from "{chal_path}"')
        challenge = chal_path.read_text()
    else:
        error('Invalid challenge input file')

    get_device_info(challenge, chal_path.parent, arg.save)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=f'CDM Device Checker | Version {__version__}',
        description='Simple util to parse CDM device info from license request/challenge\n.'
    )
    parser.add_argument(dest='challenge', nargs='?', default=None, help='Challenge or license request')
    parser.add_argument('-q', '--quite', default=False, action='store_true', help='Don\'t print the info of client_id_blob')
    parser.add_argument('-s', '--save', default=False, action='store_true', help='Save device info to json file')
    args = parser.parse_args()
    sys.exit(main(args))
