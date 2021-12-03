import sys
import base64
from pathlib import Path
from google.protobuf.message import DecodeError
from google.protobuf import text_format
from proto.wv_proto2_pb2 import ClientIdentification, SignedLicenseRequest


def extract_challenge(client_id_blob: Path, quite: bool) -> str:

    if not isinstance(client_id_blob, Path):
        client_id_blob = Path(client_id_blob)

    if not client_id_blob.exists():
        sys.exit(f'{client_id_blob} is not exist')

    print('[INFO]:  Reading client_id_blob from:', client_id_blob)
    client_id = ClientIdentification()

    try:
        client_id.ParseFromString(client_id_blob.read_bytes())
    except DecodeError:
        raise DecodeError('[ERROR]: Client id failed to parse as ClientIdentification')

    lic_request = SignedLicenseRequest()
    lic_request.Msg.ClientId.CopyFrom(client_id)

    license_challenge = lic_request.SerializeToString()

    if not quite:
        print()
        for msg in text_format.MessageToString(lic_request).splitlines():
            print(msg)

    print()
    challenge_b64 = base64.b64encode(license_challenge).decode()
    return challenge_b64
