from typing import Optional

from web3 import Web3
from web3.types import TxParams
from web3.middleware import geth_poa_middleware
from web3.contract.contract import ContractFunction
from eth_typing import HexAddress, HexStr

from .host import Host
from .constants import CFA_V1_ABI, CFA_V1_FORWARDER_ABI
from .types import GetFlowParams, GetAccountFlowInfoParams, GetFlowOperatorDataParams, GetFlowOperatorDataParamsByID, CreateFlowParams, UpdateFlowParams, DeleteFlowParams, CreateFlowByOperatorParams, UpdateFlowByOperatorParams, Web3FlowInfo, UpdateFlowParams, Web3FlowOperatorData, FlowRateAllowanceParams, UpdateFlowOperatorPermissionsParams, FullControlParams
from .errors import SFError
from .operation import Operation
from .utils import get_network


class CFA_V1:

    def __init__(self, rpc: str, chain_id: int) -> None:
        self.rpc = rpc
        network = get_network(chain_id)
        web3 = Web3(Web3.HTTPProvider(rpc))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.host = Host(rpc, network.HOST)
        self.contract = web3.eth.contract(
            address=network.CFA_V1, abi=CFA_V1_ABI)
        self.forwarder = web3.eth.contract(
            address=network.CFA_V1_FORWARDER, abi=CFA_V1_FORWARDER_ABI)

    def get_flow(self, super_token: HexAddress, sender: HexAddress, receiver: HexAddress) -> Web3FlowInfo:
        """
            Get the details of a flow.

            @param super_token - The token to be flowed
            @param sender - the sender of the flow
            @param receiver - the receiver of the flow
            @returns - Web3FlowInfo
        """
        try:
            validated_params = GetFlowParams(super_token, sender, receiver)
            transaction_response = self.contract.functions.getFlow(
                validated_params.super_token, validated_params.sender, validated_params.receiver).call()
            info = {
                "timestamp": transaction_response[0],
                "flowRate": transaction_response[1],
                "deposit": transaction_response[2],
                "owedDeposit": transaction_response[3]
            }
            return info
        except Exception as e:
            raise SFError(
                "CFAV1_READ", "There was an error getting the flow", e)

    def get_account_flow_info(self, super_token: HexAddress, account: HexAddress) -> Web3FlowInfo:
        """
            Get the details of a account flow in a super token

            @param super_token - The token to be flowed
            @param account - the account to get its info
            @returns - Web3FlowInfo
        """
        try:
            validated_params = GetAccountFlowInfoParams(
                super_token, account)
            transaction_response = self.contract.functions.getAccountFlowInfo(
                validated_params.super_token, validated_params.account).call()
            info = {
                "timestamp": transaction_response[0],
                "flowRate": transaction_response[1],
                "deposit": transaction_response[2],
                "owedDeposit": transaction_response[3]
            }
            return info
        except Exception as e:
            raise SFError(
                "CFAV1_READ", "There was an error getting the account flow information", e)

    def get_net_flow(self, super_token: HexAddress, account: HexAddress) -> int:
        """
            Get the details of the net flow of an account in a super token.

            @param super_token - The token to be flowed
            @param account - the account to get its info
            @returns - int: net flow rate of the account
        """
        try:
            validated_params = GetAccountFlowInfoParams(
                super_token, account)
            transaction_response = self.contract.functions.getNetFlow(
                validated_params.super_token, validated_params.account).call()
            net_flow_rate = transaction_response
            return net_flow_rate
        except Exception as e:
            raise SFError(
                "CFAV1_READ", "There was an error getting net flow", e)

    def get_flow_operator_data(self, super_token: HexAddress, sender: HexAddress, flow_operator: HexAddress) -> Web3FlowOperatorData:
        """
            Get the details of a flow operator to a sender

            @param super_token - The token to be flowed
            @param sender - the sender of the flow
            @param flow_operator - the spender
            @returns - Web3FlowOperatorData
        """
        try:
            validated_params = GetFlowOperatorDataParams(
                super_token, sender, flow_operator)
            transaction_response = self.contract.functions.getFlowOperatorData(
                validated_params.super_token, validated_params.sender, validated_params.flow_operator).call()
            flow_operator_data = {
                # TODO: Review conversions
                "flowOperatorId": Web3.to_hex(transaction_response[0]),
                "permissions": transaction_response[1],
                "flowRateAllowance": transaction_response[2]
            }
            return flow_operator_data
        except Exception as e:
            raise SFError(
                "CFAV1_READ", "There was an error getting flow operator data", e)

    def get_flow_operator_data_by_id(self, super_token: HexAddress, flow_operator_id: HexStr) -> Web3FlowOperatorData:
        """
            Get the details of a flow operator to a sender by id

            @param super_token - The token to be flowed
            @param flow_operator_id - the flow operator id
            @returns - Web3FlowOperatorData
        """
        try:
            validated_params = GetFlowOperatorDataParamsByID(
                super_token, flow_operator_id)
            transaction_response = self.contract.functions.getFlowOperatorDataByID(
                validated_params.super_token, validated_params.flow_operator_id).call()
            flow_operator_data = {
                # TODO: Review conversions
                "flowOperatorId": validated_params.flow_operator_id,
                "permissions": transaction_response[0],
                "flowRateAllowance": transaction_response[1]
            }
            return flow_operator_data
        except Exception as e:
            raise SFError(
                "CFAV1_READ", "There was an error getting flow operator data", e)

    def create_flow(self, sender: HexAddress, receiver: HexAddress, super_token: HexAddress, flow_rate: int, user_data: Optional[HexStr] = None,  should_use_call_agreement: Optional[bool] = None) -> Operation:
        """
            Creates a flow

            @param sender - sender of the flow
            @param receiver - receiver of a flow
            @param super_token - The token to be flowed
            @param flow_rate - flow rate for the flow
            @param user_data(Optional) - Extra data provided
            @param should_use_call_agreement(Optional) - whether or not to use the host contract
            @returns - Operation
        """
        validated_params = CreateFlowParams(
            sender, receiver, super_token, flow_rate, user_data, should_use_call_agreement)
        calldata = self.contract.encodeABI(fn_name='createFlow', args=[
            validated_params.super_token, validated_params.receiver, validated_params.flow_rate, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, validated_params.user_data or "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.createFlow(
            validated_params.super_token, validated_params.sender, validated_params.receiver, validated_params.flow_rate, validated_params.user_data or "0x")
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, validated_params.should_use_call_agreement)

    def update_flow(self, sender: HexAddress, receiver: HexAddress, super_token: HexAddress, flow_rate: int, user_data: Optional[HexStr] = None,  should_use_call_agreement: Optional[bool] = None) -> Operation:
        """
            Updates a flow

            @param sender - sender of the flow
            @param receiver - receiver of a flow
            @param super_token - The token to be flowed
            @param flow_rate - flow rate for the flow
            @param user_data(Optional) - Extra data provided
            @param should_use_call_agreement(Optional) - whether or not to use the host contract
            @returns - Operation
        """
        validated_params = UpdateFlowParams(
            sender, receiver, super_token, flow_rate, user_data, should_use_call_agreement)
        calldata = self.contract.encodeABI(fn_name='updateFlow', args=[
            validated_params.super_token, validated_params.receiver, validated_params.flow_rate, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.updateFlow(
            validated_params.super_token, validated_params.sender, validated_params.receiver, validated_params.flow_rate, validated_params.user_data or "0x")
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, validated_params.should_use_call_agreement)

    def delete_flow(self, sender: HexAddress, receiver: HexAddress, super_token: HexAddress, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> Operation:
        """
            Deletes a flow

            @param sender - sender of the flow
            @param receiver - receiver of a flow
            @param super_token - The token to be flowed
            @param user_data(Optional) - Extra data provided
            @param should_use_call_agreement(Optional) - whether or not to use the host contract
            @returns - Operation
        """
        validated_params = DeleteFlowParams(
            sender, receiver, super_token, user_data, should_use_call_agreement)
        calldata = self.contract.encodeABI(fn_name='deleteFlow', args=[
            validated_params.super_token, validated_params.sender, validated_params.receiver, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.deleteFlow(
            validated_params.super_token, validated_params.sender, validated_params.receiver, validated_params.user_data or "0x")
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, validated_params.should_use_call_agreement)

    def increase_flow_rate_allowance(self, super_token: HexAddress, flow_operator: HexAddress, flow_rate_allowance_delta: int, user_data: Optional[HexStr] = None) -> Operation:
        """
            Increases the flow rate allowance of a flow operator

            @param super_token - The token to be flowed
            @param flow_operator - The operator of the flow
            @param flow_rate_allowance_delta - The amount to increase the flow rate allowance by
            @param user_data(Optional) - Extra data provided
            @returns - Operation
        """
        validated_params = FlowRateAllowanceParams(
            super_token, flow_operator, flow_rate_allowance_delta, user_data)
        calldata = self.contract.encodeABI(fn_name='increaseFlowRateAllowance', args=[
            validated_params.super_token, validated_params.flow_operator, validated_params.flow_rate_allowance_delta, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, validated_params.user_data or "0x")
        return call_agreement_operation

    def decrease_flow_rate_allowance(self, super_token: HexAddress, flow_operator: HexAddress, flow_rate_allowance_delta: int, user_data: Optional[HexStr] = None) -> Operation:
        """
            Decreases the flow rate allowance of a flow operator

            @param super_token - The token to be flowed
            @param flow_operator - The operator of the flow
            @param flow_rate_allowance_delta - The amount to decrease the flow rate allowance by
            @param user_data(Optional) - Extra data provided
            @returns - Operation
        """
        validated_params = FlowRateAllowanceParams(
            super_token, flow_operator, flow_rate_allowance_delta, user_data)
        calldata = self.contract.encodeABI(fn_name='decreaseFlowRateAllowance', args=[
            validated_params.super_token, validated_params.flow_operator, validated_params.flow_rate_allowance_delta, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, validated_params.user_data or "0x")
        return call_agreement_operation

    def update_flow_operator_permissions(self, super_token: HexAddress, flow_operator: HexAddress, permissions: int, flow_rate_allowance: int, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> Operation:
        """
            Update permissions for a flow operator as a sender.

            @param super_token - The token to be flowed
            @param flow_operator - The operator of the flow
            @param permissions - Number specifying the permission type
            @param flow_rate_allowance - Allowance to an operator
            @param user_data(Optional) - Extra data provided
            @returns - Operation
        """
        validated_params = UpdateFlowOperatorPermissionsParams(
            super_token, flow_operator, permissions, flow_rate_allowance, user_data, should_use_call_agreement)
        calldata = self.contract.encodeABI(fn_name='updateFlowOperatorPermissions', args=[
            validated_params.super_token, validated_params.flow_operator, validated_params.permissions, validated_params.flow_rate_allowance, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, validated_params.user_data or "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.updateFlowOperatorPermissions(
            validated_params.super_token, validated_params.flow_operator, validated_params.permissions, validated_params.flow_rate_allowance)
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, validated_params.should_use_call_agreement)

    def authorize_flow_operator_with_full_control(self, super_token: HexAddress, flow_operator: HexAddress, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> Operation:
        """
            Give flow operator full control - max flow rate and create/update/delete permissions.

            @param super_token - The token to be flowed
            @param flow_operator - The operator of the flow
            @param user_data(Optional) - Extra data provided
            @param should_use_call_agreement(Optional) - whether or not to use the host contract
            @returns - Operation
        """
        validated_params = FullControlParams(
            super_token, flow_operator, user_data, should_use_call_agreement)
        calldata = self.contract.encodeABI(fn_name='authorizeFlowOperatorWithFullControl', args=[
            validated_params.super_token, validated_params.flow_operator, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, validated_params.user_data or "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.grantPermissions(
            validated_params.super_token, validated_params.flow_operator)
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, validated_params.should_use_call_agreement)

    def revoke_flow_operator_with_full_control(self, super_token: HexAddress, flow_operator: HexAddress, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> Operation:
        """
            Revoke flow operator control - set flow rate to 0 with no permissions.

            @param super_token - The token to be flowed
            @param flow_operator - The operator of the flow
            @param user_data(Optional) - Extra data provided
            @param should_use_call_agreement(Optional) - whether or not to use the host contract
            @returns - Operation
        """
        validated_params = FullControlParams(
            super_token, flow_operator, user_data, should_use_call_agreement)
        calldata = self.contract.encodeABI(fn_name='revokeFlowOperatorWithFullControl', args=[
            validated_params.super_token, validated_params.flow_operator, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, validated_params.user_data or "0x")
        forwarder_call: ContractFunction = self.forwarder.functions.revokePermissions(
            validated_params.super_token, validated_params.flow_operator)
        return self._get_call_agreement_operation(call_agreement_operation, forwarder_call, validated_params.should_use_call_agreement)

    def create_flow_by_operator(self, sender: HexAddress, receiver: HexAddress, super_token: HexAddress, flow_rate: int, user_data: Optional[HexStr] = None,  should_use_call_agreement: Optional[bool] = None) -> Operation:
        """
            Create a flow as an operator

            @param sender - sender of the flow
            @param receiver - receiver of a flow
            @param super_token - The token to be flowed
            @param flow_rate - flow rate for the flow
            @param user_data(Optional) - Extra data provided
            @param should_use_call_agreement(Optional) - whether or not to use the host contract
            @returns - Operation
        """
        validated_params = CreateFlowByOperatorParams(
            sender, receiver, super_token, flow_rate, user_data, should_use_call_agreement)
        calldata = self.contract.encodeABI(fn_name='createFlowByOperator', args=[
            validated_params.super_token, validated_params.sender, validated_params.receiver, validated_params.flow_rate, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, validated_params.user_data or "0x")
        create_flow_operation = self.create_flow(
            sender, receiver, super_token, flow_rate, user_data, should_use_call_agreement)
        return self._get_call_agreement_operation(call_agreement_operation, create_flow_operation.forwarder_call, validated_params.should_use_call_agreement)

    def update_flow_by_operator(self, sender: HexAddress, receiver: HexAddress, super_token: HexAddress, flow_rate: int, user_data: Optional[HexStr] = None,  should_use_call_agreement: Optional[bool] = None) -> Operation:
        """
            Update a flow as an operator

            @param sender - sender of the flow
            @param receiver - receiver of a flow
            @param super_token - The token to be flowed
            @param flow_rate - flow rate for the flow
            @param user_data(Optional) - Extra data provided
            @param should_use_call_agreement(Optional) - whether or not to use the host contract
            @returns - Operation
        """
        validated_params = UpdateFlowByOperatorParams(
            sender, receiver, super_token, flow_rate, user_data, should_use_call_agreement)
        calldata = self.contract.encodeABI(fn_name='updateFlowByOperator', args=[
            validated_params.super_token, validated_params.sender, validated_params.receiver, validated_params.flow_rate, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, "0x")
        update_flow_operation = self.update_flow(
            sender, receiver, super_token, flow_rate, user_data, should_use_call_agreement)
        return self._get_call_agreement_operation(call_agreement_operation, update_flow_operation.forwarder_call, validated_params.should_use_call_agreement)

    def delete_flow_by_operator(self, sender: HexAddress, receiver: HexAddress, super_token: HexAddress, user_data: Optional[HexStr] = None, should_use_call_agreement: Optional[bool] = None) -> Operation:
        """
            Delete a flow as an operator

            @param sender - sender of the flow
            @param receiver - receiver of a flow
            @param super_token - The token to be flowed
            @param user_data(Optional) - Extra data provided
            @param should_use_call_agreement(Optional) - whether or not to use the host contract
            @returns - Operation
        """
        validated_params = DeleteFlowParams(
            sender, receiver, super_token, user_data, should_use_call_agreement)
        calldata = self.contract.encodeABI(fn_name='deleteFlowByOperator', args=[
            validated_params.super_token, validated_params.sender, validated_params.receiver, "0x"])
        call_agreement_operation = self.host.call_agreement(
            self.contract.address, calldata, "0x")
        delete_flow_operation = self.delete_flow(
            sender, receiver, super_token, user_data, should_use_call_agreement)
        return self._get_call_agreement_operation(call_agreement_operation, delete_flow_operation.forwarder_call, validated_params.should_use_call_agreement)

    def _get_call_agreement_operation(self, call_agreement_operation: Operation, forwarder_call: Optional[ContractFunction] = None, should_use_call_agreement: Optional[bool] = None) -> Operation:
        if should_use_call_agreement == True:
            return call_agreement_operation
        else:
            return Operation(self.rpc, call_agreement_operation.agreement_call, call_agreement_operation.type, forwarder_call)
