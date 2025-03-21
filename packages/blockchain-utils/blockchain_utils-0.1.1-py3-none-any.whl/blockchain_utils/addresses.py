import binascii
import math
import re
from base64 import b32decode
from hashlib import sha256, blake2b
from typing import Dict, Callable, Tuple, List

import base58
import cbor
from Cryptodome.Hash import SHA512
from bech32 import bech32_decode
from buidl.bech32 import decode_bech32 as buidl_decode_bech32
from blake256.blake256 import blake_hash
from monero import address as monero_address
from solders.pubkey import Pubkey
from web3 import Web3

from .address_validators.polkadot import ss58_decode
from .address_validators.stellar import decode_check
from .address_validators import flow


def normalize_eth_address(address: str) -> str:
    """Function normalizes (transform) Ethereum to canonical view
    :param address: Ethereum address
    :return: Normalized ethereum address
    """
    return Web3.to_checksum_address(address)


ETH: str = 'ETH'
BTC: str = 'BTC'
ATOM: str = 'ATOM'
XTZ: str = 'XTZ'
DCR: str = 'DCR'
QTUM: str = 'QTUM'
X_CHAIN_AVAX: str = 'X_CHAIN_AVAX'
FIL: str = 'FIL'
ICP: str = 'ICP'
FET: str = 'FET'
ADA: str = 'ADA'
LTC: str = 'LTC'
DOGE: str = 'DOGE'
XRP: str = 'XRP'
SOL: str = 'SOL'
XMR: str = 'XMR'
DOT: str = 'DOT'
DASH: str = 'DASH'
EOS: str = 'EOS'
IOTA: str = 'IOTA'
NEO: str = 'NEO'
XLM: str = 'XLM'
ZEC: str = 'ZEC'
HBAR: str = 'HBAR'
FLOW: str = 'FLOW'
EGLD: str = 'EGLD'
ALGO: str = 'ALGO'

NORMALIZATION_HANDLER: Dict[str, Callable[[str], str]] = {
    ETH: normalize_eth_address,
    BTC: lambda address: address,
    ATOM: lambda address: address,
    XTZ: lambda address: address,
    DCR: lambda address: address,
    QTUM: lambda address: address,
    X_CHAIN_AVAX: lambda address: address,
    FIL: lambda address: address,
    ICP: lambda address: address,
    FET: lambda address: address,
    ADA: lambda address: address,
    LTC: lambda address: address,
    DOGE: lambda address: address,
    XRP: lambda address: address,
    SOL: lambda address: address,
    XMR: lambda address: address,
    DOT: lambda address: address,
    DASH: lambda address: address,
    EOS: lambda address: address,
    IOTA: lambda address: address,
    NEO: lambda address: address,
    XLM: lambda address: address,
    ZEC: lambda address: address,
    HBAR: lambda address: address,
    FLOW: lambda address: address,
    EGLD: lambda address: address,
    ALGO: lambda address: address,
}


def is_btc_address(address: str) -> bool:
    """Function validates the following Bitcoin address formats: P2PKH, P2SH, Bech32 (P2WPKH and P2TR)
    :param address: Potential Bitcoin address
    :return: True if address is correct, otherwise False
    """
    if not address:
        return False

    try:
        if address[0] == '1':  # P2PKH Address
            decoded = base58.b58decode_check(address)
            return len(decoded) == 21 and decoded[0] == 0x00
        elif address[0] == '3':  # P2SH Address
            decoded = base58.b58decode_check(address)
            return len(decoded) == 21 and decoded[0] == 0x05
        elif address[:3] == 'bc1':  # Bech32 Addresses (P2WPKH and P2TR)
            if not re.match(r'^bc1[qp][a-z0-9]{38,58}$', address):
                return False
            network, _, hash = buidl_decode_bech32(address)
            return network == 'mainnet' and len(hash) in (20, 32)
        return False
    except (ValueError, TypeError):
        return False


def is_eth_address(address: str) -> bool:
    """Function validates whether the given address is Ethereum or nor
    :param address: Potential Ethereum address
    :return: True if the address is Ethereum otherwise False
    """
    return Web3.is_address(address)


def is_atom_address(address: str) -> bool:
    """Function validates whether the given address is Cosmostation or nor
    :param address: Potential Cosmostation address
    :return: True if the address is Cosmostation otherwise False
    """
    regex = r'^(cosmos)1([qpzry9x8gf2tvdw0s3jn54khce6mua7l]+)'
    match = re.match(regex, address)
    if not match:
        return False
    else:
        decodes: Tuple[str, List[int]] = bech32_decode(address)
        return len(decodes[1]) == 32 if decodes != (None, None) else False


def is_xtz_address(address: str) -> bool:
    """Function validates whether the given address is Tezos or nor
    :param address: Potential Tezos address
    :return: True if the address is Tezos otherwise False
    """
    try:
        decoded = base58.b58decode(address)
    except ValueError:
        return False
    return address.startswith("tz") and len(decoded) == 27


def is_dcr_address(address: str) -> bool:
    """Function validates whether the given address is Decred or nor
    :param address: Potential Decred address
    :return: True if the address is Decred otherwise False
    """
    try:
        decoded = base58.b58decode(address)
    except ValueError:
        return False
    body, checksum = decoded[:-4], decoded[-4:]
    return len(decoded) == 26 and blake_hash(blake_hash(body)).hex()[:8] == checksum.hex()


def is_qtum_address(address: str) -> bool:
    """Function validates whether the given address is QTUM or nor
    :param address: Potential QTUM address
    :return: True if the address is QTUM otherwise False
    """
    try:
        if address.startswith('Q'):
            decoded = base58.b58decode(address)
        else:
            return False
    except ValueError:
        return False
    body, checksum = decoded[:-4], decoded[-4:]
    return len(decoded) == 25 and sha256(sha256(body).digest()).hexdigest()[:8] == checksum.hex()


def is_x_chain_avax_address(address: str) -> bool:
    """Function validates whether the given address is AVAX X-CHAIN or nor
    :param address: Potential AVAX X-CHAIN address
    :return: True if the address is AVAX X-CHAIN otherwise False
    """
    regex = r'^(X-avax)1([qpzry9x8gf2tvdw0s3jn54khce6mua7l]+)'
    match = re.match(regex, address)
    if not match:
        return False
    else:
        decodes: Tuple[str, List[int]] = bech32_decode(address[2:])
        return len(decodes[1]) == 32 if decodes != (None, None) else False


def is_fil_address(address: str) -> bool:
    """Function validates whether the given address is Filecoin or nor
    :param address: Potential Filecoin address
    :return: True if the address is Filecoin otherwise False
    """

    if not 86 >= len(address) >= 3 or address[0] not in ('f', 't') or address[1] not in ('1', '3'):
        return False

    protocol = address[1]
    raw = address[2:]

    pad_length = math.ceil(len(raw) / 8) * 8 - len(raw)
    raw += '=' * pad_length

    try:
        payloadcksm = b32decode(raw, casefold=True)
    except binascii.Error:
        return False

    if len(payloadcksm) < 4:
        return False

    payload = payloadcksm[:len(payloadcksm) - 4]
    checksum = payloadcksm[len(payloadcksm) - 4:]

    if protocol == '1' and len(payload) != 20 or protocol == '3' and len(payload) != 48:
        return False

    to_check = bytearray(b'\x03' if protocol == '3' else b'\x01')
    to_check.extend(payload)

    return blake2b(to_check, digest_size=4).digest() == checksum


def is_icp_address(address: str) -> bool:
    """Function validates whether the given address is ICP or nor
    :param address: Potential ICP address
    :return: True if the address is ICP otherwise False
    """
    regex = r'^[a-f0-9]{64}$'
    match = re.match(regex, address)

    return bool(match)


def is_fet_address(address: str) -> bool:
    """Function validates whether the given address is FET or nor
    :param address: Potential FET address
    :return: True if the address is FET otherwise False
    """
    regex = r'^(fetch)1([qpzry9x8gf2tvdw0s3jn54khce6mua7l]+)'
    match = re.match(regex, address)
    if not match:
        return False
    else:
        decodes: Tuple[str, List[int]] = bech32_decode(address)
        return len(decodes[1]) == 32 if decodes != (None, None) else False


def is_ada_address(address: str) -> bool:
    """Function validates whether the given address is ADA or nor
    :param address: Potential ADA address
    :return: True if the address is ADA otherwise False
    """
    regexes: List[str] = [
        r'^(addr)1([qpzry9x8gf2tvdw0s3jn54khce6mua7l]+)',
        r'^(stake)1([qpzry9x8gf2tvdw0s3jn54khce6mua7l]+)',
    ]
    matches: List[bool] = [bool(re.match(regex, address)) for regex in regexes]
    if not any(matches):
        try:
            decoded_address = cbor.loads(base58.b58decode(address))
        except (ValueError, RuntimeError, LookupError):
            return False
        if (
            isinstance(decoded_address, int) or
            isinstance(decoded_address, cbor.cbor.Tag) or
            isinstance(decoded_address, list) and len(decoded_address) != 2
        ):
            return False

        try:
            tagged_address = decoded_address[0]
            provided_checksum = decoded_address[1]
            computed_checksum = binascii.crc32(tagged_address.value)
            return provided_checksum == computed_checksum
        except (AttributeError, IndexError, KeyError):
            return False

    else:
        decodes: Tuple[str, List[int]] = bech32_decode(address)
        return len(decodes[1]) in (92, 47, 56) if decodes != (None, None) else False


def is_ltc_address(address: str) -> bool:
    """Function validates whether the given address is LTC or nor
    :param address: Potential LTC address
    :return: True if the address is LTC otherwise False
    """
    segwit_pattern = r'^(ltc)1([qpzry9x8gf2tvdw0s3jn54khce6mua7l]+)'  # Check for ltc1 (SegWit) addresses
    legacy_pattern = r'^[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}$'  # Check for Legacy (L, M, 3) addresses

    if re.match(segwit_pattern, address):
        decodes: Tuple[str, List[int]] = bech32_decode(address)
        return len(decodes[1]) in (33, 53) if decodes != (None, None) else False
    elif re.match(legacy_pattern, address):
        try:
            result = base58.b58decode_check(address)
        except ValueError:
            return False
        else:
            return bool(result)
    else:
        return False


def is_doge_address(address: str) -> bool:
    """Function validates whether the given address is DOGE or nor
    :param address: Potential DOGE address
    :return: True if the address is DOGE otherwise False
    """
    try:
        if address.startswith(('D', 'A', '9')):
            result = base58.b58decode_check(address)
        else:
            return False
    except ValueError:
        return False
    else:
        return bool(result)


def is_xrp_address(address: str) -> bool:
    """Function validates whether the given address is XRP or nor
    :param address: Potential XRP address
    :return: True if the address is XRP otherwise False
    """
    try:
        if address.startswith('r'):
            result = base58.b58decode_check(address, alphabet=base58.RIPPLE_ALPHABET)
        else:
            return False
    except ValueError:
        return False
    else:
        return bool(result)


def is_sol_address(address: str) -> bool:
    """Function validates whether the given address is SOL or nor
    :param address: Potential SOL address
    :return: True if the address is SOL otherwise False
    """
    try:
        return Pubkey.from_string(address).is_on_curve()
    except ValueError:
        return False


def is_xmr_address(address: str) -> bool:
    """Function validates whether the given address is XMR or nor
    :param address: Potential XMR address
    :return: True if the address is XMR otherwise False
    """
    try:
        return bool(monero_address.address(addr=address))
    except ValueError:
        return False


def is_dot_address(address: str) -> bool:
    """Function validates whether the given address is DOT or nor
    :param address: Potential DOT address
    :return: True if the address is DOT otherwise False
    """
    try:
        return bool(ss58_decode(address=address, valid_ss58_format=0))
    except ValueError:
        return False


def is_dash_address(address: str) -> bool:
    """Function validates whether the given address is DASH or nor
    :param address: Potential DASH address
    :return: True if the address is DASH otherwise False
    """
    try:
        if address.startswith(('X', '7')):
            result = base58.b58decode_check(address)
        else:
            return False
    except ValueError:
        return False
    else:
        return bool(result)


def is_eos_address(address: str) -> bool:
    """Function validates whether the given address is EOS or nor
    :param address: Potential EOS address
    :return: True if the address is EOS otherwise False
    """
    if len(address) != 12:
        return False
    eos_pattern = re.compile('^[a-z]{1}[a-z1-5.]{10}[a-z1-5]{1}$')
    if eos_pattern.match(address) is None:
        return False
    return True


def is_iota_address(address: str) -> bool:
    """Function validates whether the given address is IOTA or nor
    :param address: Potential IOTA address
    :return: True if the address is IOTA otherwise False
    """
    regex = r'^(iota)1([qpzry9x8gf2tvdw0s3jn54khce6mua7l]+)'
    match = re.match(regex, address)
    if match:
        decodes: Tuple[str, List[int]] = bech32_decode(address)
        return len(decodes[1]) == 53 if decodes != (None, None) else False
    return False


def is_neo_address(address: str) -> bool:
    """Function validates whether the given address is NEO or nor
    :param address: Potential NEO address
    :return: True if the address is NEO otherwise False
    """
    try:
        if address.startswith(('A', 'N')):
            result = base58.b58decode_check(address)
        else:
            return False
    except ValueError:
        return False
    else:
        return bool(result)


def is_xlm_address(address: str) -> bool:
    """Function validates whether the given address is XLM or nor
    :param address: Potential XLM address
    :return: True if the address is XLM otherwise False
    """
    try:
        return bool(decode_check('account', address))
    except Exception:
        return False


def is_zec_address(address: str) -> bool:
    """Function validates whether the given address is ZEC or nor
    :param address: Potential ZEC address
    :return: True if the address is ZEC otherwise False
    """
    try:
        if address.startswith(('z', 't')):
            result = base58.b58decode_check(address)
        else:
            return False
    except ValueError:
        return False
    else:
        return bool(result)


def is_hbar_address(address: str) -> bool:
    """Function validates whether the given address is HBAR or nor
    :param address: Potential HBAR address
    :return: True if the address is HBAR otherwise False
    """
    regex = r'^(0|(?:[1-9]\d*))\.(0|(?:[1-9]\d*))\.(0|(?:[1-9]\d*))(?:-([a-z]{5}))?$'
    match = re.match(regex, address)
    if not match:
        return False
    else:
        return True


def is_flow_address(address: str) -> bool:
    """Function validates whether the given address is FLOW or nor
    :param address: Potential FLOW address
    :return: True if the address is FLOW otherwise False
    """
    try:
        return flow.is_valid_checksum(address=address)
    except ValueError:
        return False


def is_egld_address(address: str) -> bool:
    """Function validates whether the given address is EGLD or nor
    :param address: Potential EGLD address
    :return: True if the address is EGLD otherwise False
    """
    regex = r'^(erd)1([qpzry9x8gf2tvdw0s3jn54khce6mua7l]+)'
    match = re.match(regex, address)
    if not match:
        return False
    else:
        decodes: Tuple[str, List[int]] = bech32_decode(address)
        return len(decodes[1]) == 52 if decodes != (None, None) else False


def is_algo_address(address: str) -> bool:
    """
    Function validates whether the given address is Algorand or nor
    :param address: Potential ALGO address
    :return: True if the address is ALGO otherwise False
    """
    def _correct_padding(a):
        if len(a) % 8 == 0:
            return a
        return a + "=" * (8 - len(a) % 8)

    if not len(address.strip("=")) == 58:  # key length must be 58
        return False
    try:
        # Decode a string address into its address bytes and checksum
        # 4 - checksum len in bytes
        decoded = b32decode(_correct_padding(address))
        address_without_checksum = decoded[: -4]
        expected_checksum = decoded[-4:]

        chksum = SHA512.new(truncate="256")
        chksum.update(address_without_checksum)
        chksum = chksum.digest()
        chksum = chksum[-4:]  # Compute the checksum of size checkSumLenBytes for the address

        if chksum == expected_checksum:
            decoded_address = address_without_checksum
        else:
            return False

        if isinstance(decoded_address, str):
            return False

        return True
    except Exception as e:
        return False


def detect_blockchain(address: str) -> str | None:
    """Function determines which blockchain the address belongs to.
    If the blockchain is not known, then None returned
    :param address: Address
    :return: Blockchain ID or None
    """

    if is_eth_address(address):
        return ETH
    elif is_btc_address(address):
        return BTC
    elif is_atom_address(address):
        return ATOM
    elif is_xtz_address(address):
        return XTZ
    elif is_dcr_address(address):
        return DCR
    elif is_qtum_address(address):
        return QTUM
    elif is_x_chain_avax_address(address):
        return X_CHAIN_AVAX
    elif is_fil_address(address):
        return FIL
    elif is_icp_address(address):
        return ICP
    elif is_fet_address(address):
        return FET
    elif is_ada_address(address):
        return ADA
    elif is_ltc_address(address):
        return LTC
    elif is_doge_address(address):
        return DOGE
    elif is_xrp_address(address):
        return XRP
    elif is_sol_address(address):
        return SOL
    elif is_xmr_address(address):
        return XMR
    elif is_dot_address(address):
        return DOT
    elif is_dash_address(address):
        return DASH
    elif is_eos_address(address):
        return EOS
    elif is_iota_address(address):
        return IOTA
    elif is_neo_address(address):
        return NEO
    elif is_xlm_address(address):
        return XLM
    elif is_zec_address(address):
        return ZEC
    elif is_hbar_address(address):
        return HBAR
    elif is_flow_address(address):
        return FLOW
    elif is_egld_address(address):
        return EGLD
    elif is_algo_address(address):
        return ALGO

    return None


def normalize_address(address: str) -> str:
    """Function normalizes the address depending on which blockchain it belongs to.
    If the blockchain is not known, then an error UnknownBlockchain is raised
    :param address: Address
    :return: Normalized address
    """
    return NORMALIZATION_HANDLER[detect_blockchain(address)](address)
