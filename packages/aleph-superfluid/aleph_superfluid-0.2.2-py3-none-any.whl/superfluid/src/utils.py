from eth_typing import HexAddress
from web3 import Web3

from .errors import InvalidAddressError, InvalidChainId
from .constants import NETWORKS, AUTHORIZE_FLOW_OPERATOR_CREATE, AUTHORIZE_FLOW_OPERATOR_DELETE, AUTHORIZE_FLOW_OPERATOR_UPDATE
# from .types import NETWORK


def to_bytes32(string: str) -> bytes:
    encoded_string = string.encode('utf-8')
    if len(encoded_string) > 32:
        raise ValueError("Input string is too long for bytes32")
    padding_length = 32 - len(encoded_string)
    padded_string = encoded_string + b'\x00' * padding_length
    return padded_string


def to_bytes(string: str) -> bytes:
    encoded_string = string.encode('utf-8')
    return encoded_string


def normalize_address(address: HexAddress) -> HexAddress:
    if len(address) == 42 or 40:
        return Web3.to_checksum_address(address)
    else:
        raise InvalidAddressError(f"{address} is invalid")


def is_permissions_clean(permissions: int) -> bool:
    return ((permissions & ~(AUTHORIZE_FLOW_OPERATOR_CREATE | AUTHORIZE_FLOW_OPERATOR_UPDATE | AUTHORIZE_FLOW_OPERATOR_DELETE)) == 0)


def validate_chain_id(chain_id: int) -> bool:
    for network in NETWORKS:
        if chain_id == network.get("chainId"):
            return True
    raise InvalidChainId("Chain not supported")


def get_network(chain_id: int):
    from .types import NETWORK
    for network in NETWORKS:
        if chain_id == network.get("chainId"):
            return NETWORK(network)
    raise InvalidChainId("Chain not supported")
