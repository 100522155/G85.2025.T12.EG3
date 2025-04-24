from unittest import TestCase

from uc3m_money import AccountManager

from uc3m_money.storage.transfer_json_store import TransferJsonStore

class TestSinglenton(TestCase):

    def test_account_manager_singleton(self):
        am1 = AccountManager()
        am2 = AccountManager()
        am3 = AccountManager()
        self.assertEqual(am1, am2)
        self.assertEqual(am2, am3)
        self.assertEqual(am1, am3)

    def test_transfer_json_store(self):
        transfer1 = TransferJsonStore()
        transfer2 = TransferJsonStore()
        transfer3 = TransferJsonStore()
        self.assertEqual(transfer1, transfer2)
        self.assertEqual(transfer2, transfer3)
        self.assertEqual(transfer1, transfer3)
        #########

    def test_deposits_json_store(self):
        deposit1 = DepositJsonStore()
        deposit2 = DepositJsonStore()
        deposit3 = DepositJsonStore()
        self.assertEqual(deposit1, deposit2)
        self.assertEqual(deposit1, deposit3)
        self.assertEqual(deposit3, deposit2)


