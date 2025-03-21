import dataclasses
from _blake2 import blake2b
from typing import Optional, Union

import base58


@dataclasses.dataclass
class SS58Address:
    format: int
    length: int


def decode_ss58_address_format(address: bytes, valid_ss58_format: Optional[int]) -> SS58Address:
    if address[0] & 0b0100_0000:
        format_length = 2
        ss58_format = ((address[0] & 0b0011_1111) << 2) | (address[1] >> 6) | ((address[1] & 0b0011_1111) << 8)
    else:
        format_length = 1
        ss58_format = address[0]

    if ss58_format in [46, 47]:
        raise ValueError(f'{ss58_format} is a reserved SS58 format')

    if valid_ss58_format is not None and ss58_format != valid_ss58_format:
        raise ValueError('Invalid SS58 format')

    return SS58Address(format=ss58_format, length=format_length)


def get_checksum_length(decoded_base58_len: int, ss58_address: SS58Address) -> int:
    if decoded_base58_len in (3, 4, 6, 10):
        return 1
    elif decoded_base58_len in (5, 7, 11, 34 + ss58_address.length, 35 + ss58_address.length):
        return 2
    elif decoded_base58_len in (8, 12):
        return 3
    elif decoded_base58_len in (9, 13):
        return 4
    elif decoded_base58_len == 14:
        return 5
    elif decoded_base58_len == 15:
        return 6
    elif decoded_base58_len == 16:
        return 7
    elif decoded_base58_len == 17:
        return 8
    else:
        raise ValueError('Invalid address length')


def ss58_decode(address: Union[str, bytes], valid_ss58_format: Optional[int] = None) -> str:
    decoded_base58 = base58.b58decode(address)

    ss58_address = decode_ss58_address_format(decoded_base58, valid_ss58_format)

    checksum_length = get_checksum_length(len(decoded_base58), ss58_address)

    checksum = blake2b(b'SS58PRE' + decoded_base58[:-checksum_length]).digest()

    if checksum[0:checksum_length] != decoded_base58[-checksum_length:]:
        raise ValueError('Invalid checksum')

    return decoded_base58[ss58_address.length : len(decoded_base58) - checksum_length].hex()
