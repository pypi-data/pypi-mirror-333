import unittest

from main.superfluid import is_permissions_clean, validate_chain_id, get_network
from main.superfluid import InvalidChainId
from main.superfluid import types


class TestPermissionChecker(unittest.TestCase):

    def test_valid_permissions(self):
        self.assertEqual(is_permissions_clean(
            1), True)
        self.assertEqual(is_permissions_clean(
            2), True)
        self.assertEqual(is_permissions_clean(
            3), True)
        self.assertEqual(is_permissions_clean(
            4), True)
        self.assertEqual(is_permissions_clean(
            5), True)
        self.assertEqual(is_permissions_clean(
            6), True)
        self.assertEqual(is_permissions_clean(
            7), True)

    def test_invalid_permissions(self):
        self.assertEqual(is_permissions_clean(
            8), False)
        self.assertEqual(is_permissions_clean(
            9), False)
        self.assertEqual(is_permissions_clean(
            10), False)
        self.assertEqual(is_permissions_clean(
            11), False)
        self.assertEqual(is_permissions_clean(
            12), False)
        self.assertEqual(is_permissions_clean(
            13), False)
        self.assertEqual(is_permissions_clean(
            14), False)


class TestValidateChainId(unittest.TestCase):

    def test_valid_chain_id(self):
        self.assertEqual(validate_chain_id(
            5), True)
        self.assertEqual(validate_chain_id(
            80001), True)
        self.assertEqual(validate_chain_id(
            420), True)
        self.assertEqual(validate_chain_id(
            421613), True)
        self.assertEqual(validate_chain_id(
            43113), True)
        self.assertEqual(validate_chain_id(
            11155111), True)
        self.assertEqual(validate_chain_id(
            100), True)

    def test_invalid_chain_id(self):
        with self.assertRaises(InvalidChainId):
            validate_chain_id(88)
        with self.assertRaises(InvalidChainId):
            validate_chain_id(599)
        with self.assertRaises(InvalidChainId):
            validate_chain_id(76)


class TestGetNetwork(unittest.TestCase):

    def test_valid_network(self):
        polygon_mumbai_network = get_network(80001)
        self.assertEqual(
            polygon_mumbai_network.RESOLVER, "0x8C54C83FbDe3C59e59dd6E324531FB93d4F504d3")
        self.assertEqual(
            polygon_mumbai_network.HOST, "0xEB796bdb90fFA0f28255275e16936D25d3418603")
        self.assertEqual(
            polygon_mumbai_network.GOVERNANCE, "0x2637eA93EE5cd887ff9AC98185eA67Bd70C5f62e")
        self.assertEqual(
            polygon_mumbai_network.CFA_V1, "0x49e565Ed1bdc17F3d220f72DF0857C26FA83F873")
        self.assertEqual(
            polygon_mumbai_network.CFA_V1_FORWARDER, "0xcfA132E353cB4E398080B9700609bb008eceB125")
        self.assertEqual(
            polygon_mumbai_network.IDA_V1, "0x804348D4960a61f2d5F9ce9103027A3E849E09b8")
        self.assertEqual(
            polygon_mumbai_network.SUPER_TOKEN_FACTORY, "0xB798553db6EB3D3C56912378409370145E97324B")
        self.assertEqual(
            polygon_mumbai_network.SUPERFLUID_LOADER, "0x0d56ED56b63382B0FC964490feB9AE438B6B4b79")
        self.assertEqual(
            polygon_mumbai_network.TOGA, "0x38DD80876DBA048d0050D28828522c313967D073")
        self.assertEqual(
            polygon_mumbai_network.SUPER_SPREADER, "0x74CDF863b00789c29734F8dFd9F83423Bc55E4cE")
        self.assertEqual(
            polygon_mumbai_network.FLOW_SCHEDULER, "0x59A3Ba9d34c387FB70b4f4e4Fbc9eD7519194139")
        self.assertEqual(
            polygon_mumbai_network.VESTING_SCHEDULER, "0x3962EE56c9f7176215D149938BA685F91aBB633B")

        optimism_goerli_network = get_network(420)
        self.assertEqual(
            optimism_goerli_network.RESOLVER, "0x21d4E9fbB9DB742E6ef4f29d189a7C18B0b59136")
        self.assertEqual(
            optimism_goerli_network.HOST, "0xE40983C2476032A0915600b9472B3141aA5B5Ba9")
        self.assertEqual(
            optimism_goerli_network.GOVERNANCE, "0x777Be25F9fdcA87e8a0E06Ad4be93d65429FCb9f")
        self.assertEqual(
            optimism_goerli_network.CFA_V1, "0xff48668fa670A85e55A7a822b352d5ccF3E7b18C")
        self.assertEqual(
            optimism_goerli_network.CFA_V1_FORWARDER, "0xcfA132E353cB4E398080B9700609bb008eceB125")
        self.assertEqual(
            optimism_goerli_network.IDA_V1, "0x96215257F2FcbB00135578f766c0449d239bd92F")
        self.assertEqual(
            optimism_goerli_network.SUPER_TOKEN_FACTORY, "0xfafe31cf998Df4e5D8310B03EBa8fb5bF327Eaf5")
        self.assertEqual(
            optimism_goerli_network.SUPERFLUID_LOADER, "0x5Bb5908dcCC9Bb0fC39a78CfDf9e47B4C08E9521")
        self.assertEqual(
            optimism_goerli_network.TOGA, None)
        self.assertEqual(
            optimism_goerli_network.SUPER_SPREADER, None)
        self.assertEqual(
            optimism_goerli_network.FLOW_SCHEDULER, None)
        self.assertEqual(
            optimism_goerli_network.VESTING_SCHEDULER, None)

    def test_invalid_network(self):
        with self.assertRaises(InvalidChainId):
            get_network(59)
        with self.assertRaises(InvalidChainId):
            get_network(500)
        with self.assertRaises(InvalidChainId):
            get_network(60)
