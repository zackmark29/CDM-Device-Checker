from pathlib import Path
from base64 import b64encode
from config import colored_print, error, info, printl
from google.protobuf import text_format
from google.protobuf.message import DecodeError
from wv_proto.wv_proto2_pb2 import ClientIdentification, SignedLicenseRequest


def parse_client_id_blob(client_id_blob: Path, quite: bool) -> str:
    client_id = ClientIdentification()

    try:
        client_id.ParseFromString(client_id_blob.read_bytes())
    except DecodeError as e:
        error(f'Unable to decode/parse "{client_id_blob}"', False)
        error(e)

    lic_request = SignedLicenseRequest()
    lic_request.Msg.ClientId.CopyFrom(client_id)
    license_challenge = lic_request.SerializeToString()
    challenge_b64 = b64encode(license_challenge).decode()

    printl()
    info('DEVICE CLIENT ID BLOB INFO:')
    printl()

    if not quite:
        print()
        for msg in text_format.MessageToString(lic_request).splitlines():
            info(msg)
        printl()
        return challenge_b64

    cid = lic_request.Msg.ClientId
    client_info = {}
    for i in cid.ClientInfo:
        i.Name = i.Name.replace('_', ' ').title().replace(' ', '')
        if i.Name == 'DeviceId':
            i.Value = b64encode(i.Value.encode()).decode()
        client_info[i.Name] = i.Value

    cc = cid._ClientCapabilities
    client_info.update({
        'SystemId': cid.Token._DeviceCertificate.SystemId,
        'ClientCapabilities': {
            'SessionToken': cc.SessionToken,
            'MaxHdcpVersion': cc.MaxHdcpVersion,
            'OemCryptoApiVersion': cc.OemCryptoApiVersion
        }
    })
    colored_print(client_info)
    return challenge_b64
