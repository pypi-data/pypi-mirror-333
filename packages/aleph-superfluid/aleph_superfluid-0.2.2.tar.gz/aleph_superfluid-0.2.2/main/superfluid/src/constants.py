import json
import os

from .abis import cfa_v1, cfa_v1_forwarder, host
from .metadata import networks


CFA_V1_ABI = json.loads(cfa_v1)

CFA_V1_FORWARDER_ABI = json.loads(cfa_v1_forwarder)

HOST_ABI = json.loads(host)

NETWORKS = json.loads(networks)

"""
------- ACL AUTHORIZATION BIT OPERATIONS -------
"""
AUTHORIZE_FLOW_OPERATOR_CREATE = 1 << 0
AUTHORIZE_FLOW_OPERATOR_UPDATE = 1 << 1
AUTHORIZE_FLOW_OPERATOR_DELETE = 1 << 2
