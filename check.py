import sys
import re
import json
import base64
import binascii
import argparse

from simple_logger import *
from pathlib import Path
from requests import Session

TOKEN = 'CfDJ8J3HFu-R0HlNvutoAYRa68EjeSliPuQR8Ogt7niNVzgha2wJQ1jDNyCmxzGv95aKF911acVDx12U1BFi0z-JcR2taHJKjY6X0qWq2H5MD65oEZJYGUkzop-l7rOa8eJJKs1V9BjJZDjLPmdOsXmquBU'
COOKIE = '.AspNetCore.Antiforgery.pcAz0O62JyE=CfDJ8J3HFu-R0HlNvutoAYRa68FIgcbDEr06bq4cJyWCC5Pl6SyEHKMWynbvPsY7pf8KYwtuZLNZMHoMv8uhJxOUyWYpCA-yrH3NW8uH0pMACoc_u8afV2xtezmcOmG53Qe9uq8U7Hv-84UWvRRraNvbsQI'


def fetch_challenge_data(challenge: str) -> str:
    info('Fetching license request data')
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
        error(res.text)

    return res.text


def parse_challenge_data(data: str) -> dict:
    info('Parsing device info')

    errors = re.compile(r'remove-sign.+>\s(.+)[<^.]')

    for err in errors.findall(data):
        error(err.replace('&quot;', '"'), False)

    td = r'>(.+)<\/td>.*\n.+<td>'
    tags = re.findall(td + r'(.+)[<^]', data)
    divs = re.findall(td + r'\n.+<div>(.+)[<^]', data)
    client_type = [x for x in tags if 'Type' in x][0][1]

    dic = dict(
        (x, y.replace('&#x0;', ''))
        for x, y in tags + divs
    )
    dic.update({'Type': client_type})
    return dic


def get_device_info(challenge: str, cwd: Path) -> None:

    data = fetch_challenge_data(challenge)
    tags = parse_challenge_data(data)

    def get(tag: str) -> str:
        match = tags.get(tag)

        if match is None:
            warn(f'No match found for: {tag}')

        return match

    system_id = get('System ID')

    if system_id is None:
        error(f'[ERROR]: System ID is not found. '
              'Looks like your challenge data is invalid')

    status = get('Status')
    sec_level = get('Security Level')
    model_name = get('model_name')
    device_name = get('device_name')
    sys_chip = get('System on Chip')

    data = {
        'status': status.upper(),
        'ForTestingOnly': get('For Testing Only'),
        'systemId': system_id,
        'securityLevel': f'LEVEL_{sec_level}',
        'manufacturer': get('Manufacturer'),
        'model': get('Model'),
        'modelYear': get('Model Year'),
        'modelName': model_name,
        'systemOnChip': sys_chip,
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
    if status == 'REVOKED':
        warn('This device was already REVOKED :(')
    else:
        info('This device is currently ACTIVE :)')

    name = model_name.replace(" ", "-")
    if sys_chip and 'generic' in sys_chip:
        name = device_name

    file_name = cwd / f'{name}-{system_id}-L{sec_level}-[{status}].json'
    data = json.dumps(data, indent=4, ensure_ascii=False)
    file_name.write_text(data)
    print('\n', data)

    info(f'Device info has been saved to: "{file_name}"')
    sys.exit()


def is_base64(txt) -> bool:
    try:
        base64.b64decode(txt, validate=True)
        return True
    except binascii.Error:
        return False


def main(arg):
    chal_path = Path(arg.challenge)

    # base64 string
    if is_base64(arg.challenge):
        get_device_info(arg.challenge, Path().cwd())
    elif not chal_path.is_file():
        error('Invalid challenge base64 input')

    if not chal_path.exists():
        error(f'{chal_path} does not exist')

    # device_client_id_blob
    if 'blob' in arg.challenge or chal_path.suffix == '.bin':
        from cdm import extract_challenge

        info(f'Extracting challenge data from: "{chal_path}"')
        challenge = extract_challenge(chal_path, arg.quite)
        info('Writing challenge base64 to "challenge.txt" file')
        Path('challenge.txt').write_text(challenge)

    # any txt file name with .txt extension
    elif chal_path.suffix == '.txt':
        info(f'Loading challenge from "{chal_path}"')
        challenge = chal_path.read_text()
    else:
        error('Invalid challenge input file')

    get_device_info(challenge, chal_path.parent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Simple util to parse CDM device info from license request/challenge.")
    parser.add_argument(dest='challenge', nargs='?', default=None, help='Challenge or license request')
    parser.add_argument('-q', '--quite', default=False, action='store_true', help='Don\'t print the results')
    sys.exit(main(parser.parse_args()))
