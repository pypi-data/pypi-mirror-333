from typing import Optional, TypedDict, Dict
from enum import Enum

from eth_typing import HexAddress, HexStr

from .utils import normalize_address, is_permissions_clean
from .errors import SFError


class GetFlowParams:

    def __init__(self, super_token: HexAddress, sender: HexAddress, receiver: HexAddress) -> None:
        """
            @param super_token - The token to be flowed
            @param sender - the sender of the flow
            @param receiver - the receiver of the flow
        """
        self.super_token = normalize_address(super_token)
        self.sender = normalize_address(sender)
        self.receiver = normalize_address(receiver)


class Web3FlowInfo(TypedDict):
    timestamp: int
    flowRate: int
    deposit: int
    owedDeposit: int


class GetAccountFlowInfoParams:

    def __init__(self, super_token: HexAddress, account: HexAddress) -> None:
        """
            @param super_token - The token to be flowed
            @param account - the account to get its info
        """
        self.super_token = normalize_address(super_token)
        self.account = normalize_address(account)


class GetFlowOperatorDataParams:

    def __init__(self, super_token: HexAddress, sender: HexAddress, flow_operator: HexAddress) -> None:
        """
            @param super_token - The token to be flowed
            @param sender - the sender of the flow
            @param flow_operator - the spender
        """
        self.super_token = normalize_address(super_token)
        self.sender = normalize_address(sender)
        self.flow_operator = normalize_address(flow_operator)


class Web3FlowOperatorData(TypedDict):
    flowOperatorId: HexStr
    permissions: int
    flowRateAllowance: int


class GetFlowOperatorDataParamsByID:

    def __init__(self, super_token: HexAddress, flow_operator_id: HexStr) -> None:
        """
            @param super_token - The token to be flowed
            @param flow_operator_id - the flow operator id
        """
        self.super_token = normalize_address(super_token)
        self.flow_operator_id = flow_operator_id


class ShouldUseCallAgreement:

    def __init__(self, should_use_call_agreement: Optional[bool] = None) -> None:
        """
            @param should_use_call_agreement - whether or not to use the host contract
        """
        self.should_use_call_agreement = should_use_call_agreement


class UserData:

    def __init__(self, user_data: Optional[HexStr] = None) -> None:
        """
            @param user_data - Extra data provided
        """
        self.user_data = user_data


class ModifyFlowParams(ShouldUseCallAgreement, UserData):

    def __init__(self, receiver: HexAddress, super_token: HexAddress, flow_rate: Optional[int] = None, sender: Optional[HexAddress] = None, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> None:
        """
            @param receiver - receiver of a flow
            @param super_token - The token to be flowed
            @param flow_rate(Optional) - flow rate for the flow
            @param sender(Optional) - sender of the flow
        """
        super().__init__(should_use_call_agreement)
        UserData.__init__(self, user_data)
        self.receiver = normalize_address(receiver)
        self.super_token = normalize_address(super_token)
        self.flow_rate = flow_rate
        self.sender = normalize_address(sender)


class CreateFlowParams(ModifyFlowParams):

    def __init__(self, sender: HexAddress, receiver: HexAddress, super_token: HexAddress, flow_rate: int, user_data: Optional[HexStr] = None,  should_use_call_agreement: Optional[bool] = None) -> None:

        super().__init__(receiver,
                         super_token, sender=sender, flow_rate=flow_rate, user_data=user_data, should_use_call_agreement=should_use_call_agreement)


class UpdateFlowParams(CreateFlowParams):
    pass


class DeleteFlowParams(ModifyFlowParams):

    def __init__(self, sender: HexAddress, receiver: HexAddress, super_token: HexAddress, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> None:
        super().__init__(receiver,
                         super_token, sender=sender, user_data=user_data, should_use_call_agreement=should_use_call_agreement)


class CreateFlowByOperatorParams(CreateFlowParams):
    pass


class UpdateFlowByOperatorParams(CreateFlowByOperatorParams):
    pass


class SuperTokenFlowRateAllowanceParams(UserData):

    def __init__(self, flow_operator: HexAddress, flow_rate_allowance_delta: int, user_data: Optional[HexStr] = None) -> None:
        """
            @param flow_operator - The operator of the flow
            @param flow_rate_allowance_delta - The amount to increase the flow rate allowance by
        """
        super().__init__(user_data)
        self.flow_operator = normalize_address(flow_operator)
        self.flow_rate_allowance_delta = flow_rate_allowance_delta


class FlowRateAllowanceParams(SuperTokenFlowRateAllowanceParams):

    def __init__(self, super_token: HexAddress, flow_operator: HexAddress, flow_rate_allowance_delta: int, user_data: Optional[HexStr] = None) -> None:
        """ 
            @param flow_operator - The operator of the flow
            @param flow_rate_allowance_delta - The amount to increase the flow rate allowance by
            @param super_token - super token
        """
        super().__init__(flow_operator, flow_rate_allowance_delta, user_data)
        self.super_token = normalize_address(super_token)


class SuperTokenUpdateFlowOperatorPermissionsParams(ShouldUseCallAgreement, UserData):

    def __init__(self, flow_operator: HexAddress, permissions: int, flow_rate_allowance: int, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> None:
        """
            @param flow_operator - The operator of the flow
            @param permissions - Number specifying the permission type
            @param flow_rate_allowance - Allowance to an operator
        """
        super().__init__(should_use_call_agreement)
        UserData.__init__(self, user_data)
        self.flow_operator = normalize_address(flow_operator)
        if is_permissions_clean(permissions):
            self.permissions = permissions
        else:
            raise SFError("UNCLEAN_PERMISSIONS",
                          "The desired permissions are unclean")
        if flow_rate_allowance < 0:
            raise SFError("NEGATIVE_FLOW_ALLOWANCE",
                          "No negative flow allowance allowed")
        else:
            self.flow_rate_allowance = flow_rate_allowance


class UpdateFlowOperatorPermissionsParams(SuperTokenUpdateFlowOperatorPermissionsParams):

    def __init__(self, super_token: HexAddress, flow_operator: HexAddress, permissions: int, flow_rate_allowance: int, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> None:
        """
            @param super_token - The token to be flowed
            @param flow_operator - The operator of the flow
            @param permissions - Number specifying the permission type
            @param flow_rate_allowance - Allowance to an operator
        """
        super().__init__(flow_operator, permissions,
                         flow_rate_allowance, user_data, should_use_call_agreement)
        self.super_token = normalize_address(super_token)


class SuperTokenFullControlParams(ShouldUseCallAgreement, UserData):

    def __init__(self, flow_operator: HexAddress, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> None:
        """
            @param flow_operator - The operator of the flow
        """
        super().__init__(should_use_call_agreement)
        UserData.__init__(self, user_data)
        self.flow_operator = normalize_address(flow_operator)


class FullControlParams(SuperTokenFullControlParams):

    def __init__(self, super_token: HexAddress, flow_operator: HexAddress, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> None:
        """
            @param super_token - The token to be flowed
            @param flow_operator - The operator of the flow
        """
        super().__init__(flow_operator, user_data, should_use_call_agreement)
        self.super_token = super_token


class BatchOperationType(Enum):

    UNSUPPORTED = "UNSUPPORTED"  # 0
    ERC20_APPROVE = "ERC20_APPROVE"  # 1
    ERC20_TRANSFER_FROM = "ERC20_TRANSFER_FROM"  # 2
    ERC777_SEND = "ERC777_SEND"  # 3
    ERC20_INCREASE_ALLOWANCE = "ERC20_INCREASE_ALLOWANCE"  # 4
    ERC20_DECREASE_ALLOWANCE = "ERC20_DECREASE_ALLOWANCE"  # 5
    SUPERTOKEN_UPGRADE = "SUPERTOKEN_UPGRADE"  # 101
    SUPERTOKEN_DOWNGRADE = "SUPERTOKEN_DOWNGRADE"  # 102
    SUPERFLUID_CALL_AGREEMENT = "SUPERFLUID_CALL_AGREEMENT"  # 201
    CALL_APP_ACTION = "CALL_APP_ACTION"  # 202


class NETWORK:

    def __init__(self, network: Dict) -> None:
        self.CHAIN_ID = network["chainId"]
        self.RESOLVER = network["contractsV1"].get("resolver")
        self.HOST = network["contractsV1"].get("host")
        self.GOVERNANCE = network["contractsV1"].get("governance")
        self.CFA_V1 = network["contractsV1"].get("cfaV1")
        self.CFA_V1_FORWARDER = network["contractsV1"].get("cfaV1Forwarder")
        self.IDA_V1 = network["contractsV1"].get("idaV1")
        self.SUPER_TOKEN_FACTORY = network["contractsV1"].get(
            "superTokenFactory")
        self.SUPERFLUID_LOADER = network["contractsV1"].get("superfluidLoader")
        self.TOGA = network["contractsV1"].get("toga")
        self.BATCH_LIQUIDATOR = network["contractsV1"].get("batchLiquidator")
        self.FLOW_SCHEDULER = network["contractsV1"].get("flowScheduler")
        self.VESTING_SCHEDULER = network["contractsV1"].get("vestingScheduler")
        self.SUPER_SPREADER = network["contractsV1"].get("superSpreader")
