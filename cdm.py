import base64

from pathlib import Path
from simple_logger import info, error
from google.protobuf import text_format
from google.protobuf.message import DecodeError
from proto.wv_proto2_pb2 import ClientIdentification, SignedLicenseRequest


def extract_challenge(client_id_blob: Path, quite: bool) -> str:

    client_id = ClientIdentification()

    try:
        client_id.ParseFromString(client_id_blob.read_bytes())
    except DecodeError:
        error(f'Unable to decode/parse "{client_id_blob}"')

    lic_request = SignedLicenseRequest()
    lic_request.Msg.ClientId.CopyFrom(client_id)

    license_challenge = lic_request.SerializeToString()

    if not quite:
        print()
        for msg in text_format.MessageToString(lic_request).splitlines():
            info(msg)

    print()
    challenge_b64 = base64.b64encode(license_challenge).decode()
    return challenge_b64
