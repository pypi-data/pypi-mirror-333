import base64
import struct
from typing import Union

import binascii

bytes_types = (bytes, bytearray)  # Types acceptable as binary data
versionBytes = {
    'account': binascii.a2b_hex('30'),  # G 48 6 << 3
}


def calculate_checksum(payload: bytes) -> bytes:
    """
    Function calculates CRC16-XModem payload checksum
    :param payload: Bytes
    :return: Checksum
    """
    checksum = binascii.crc_hqx(payload, 0)
    # Ensure that the checksum is in LSB order.
    checksum = struct.pack('<H', checksum)
    return checksum


def bytes_from_decode_data(s: Union[str, bytes]) -> bytes:
    """
    Function tries to encode string in bytes (using ASCII encoding)
    :param s: String
    :return: Bytes representation of input string
    """
    if isinstance(s, str):
        try:
            return s.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('string argument should contain only ASCII characters')
    if isinstance(s, bytes_types):
        return s
    try:
        return memoryview(s).tobytes()
    except TypeError:
        raise TypeError(
            "argument should be a bytes-like object or ASCII " "string, not %r" % s.__class__.__name__
        ) from None


def decode_check(version_byte_name: str, encoded: str) -> bytes:
    """
    Function takes address as input, performs encoding and checkes checksum
    :param version_byte_name: Type encoding
    :param encoded: Address
    :return: Decoded bytes
    """
    encoded = bytes_from_decode_data(encoded)

    try:
        decoded = base64.b32decode(encoded)
    except binascii.Error:
        raise ValueError('Incorrect padding.')

    if encoded != base64.b32encode(decoded):  # Is that even possible?
        raise ValueError('Invalid encoded bytes.')

    version_byte = decoded[0:1]
    payload = decoded[0:-2]
    data = decoded[1:-2]
    checksum = decoded[-2:]

    expected_version = versionBytes[version_byte_name]
    if version_byte != expected_version:
        raise ValueError('Invalid version byte. Expected {}, got {}'.format(str(expected_version), str(version_byte)))

    expected_checksum = calculate_checksum(payload)
    if expected_checksum != checksum:
        raise ValueError('Invalid checksum')

    return data
