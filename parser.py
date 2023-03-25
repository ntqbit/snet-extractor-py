import struct
import json


class ParserException(Exception):
    pass


def parse_binary(data: bytes):
    cursor = 0
    sig_size = struct.unpack('>I', data[:4])[0]
    metadata = data[4:4+sig_size]
    payload = data[4+sig_size:]
    return metadata, payload


def parse_metadata(metadata: str):
    lines = metadata.splitlines()
    data = {}

    for l in lines:
        if not l:
            continue

        sep_idx = l.find(':')
        if sep_idx == -1:
            raise ParserException(
                'Could not find metadata line separator: ":"')

        data[l[:sep_idx]] = l[sep_idx + 1:]

    return data


def parse_snet_flags(data: bytes):
    metadata, payload = parse_binary(data)
    parsed_metadata = parse_metadata(metadata.decode())
    payload = json.loads(payload.decode())

    try:
        return {
            'signature': parsed_metadata['SIGNATURE'],
            'version': parsed_metadata['VERSION'],
            'payload': payload
        }
    except KeyError as e:
        raise ParserException(
            f'Could not find expected metadata field: {e.args[0]}')


def parse_jar_binary(data: bytes):
    metadata, payload = parse_binary(data)
    return payload
