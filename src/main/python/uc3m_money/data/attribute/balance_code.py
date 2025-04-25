from uc3m_money.data.attribute.attribute import Attribute
from uc3m_money.account_management_exception import AccountManagementException

class BALANCE(Attribute):
    def _validate(self, iban: str, transactions_list ):
        iban_found = False
        total_balance = 0
        for transaction in transactions_list:
            # print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == iban:
                total_balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")