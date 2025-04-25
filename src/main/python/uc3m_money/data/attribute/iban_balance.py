"""docstring"""
import json
import os
from datetime import datetime,timezone
from uc3m_money.data.attribute.iban_code import IBAN
from uc3m_money.exception.account_management_exception import AccountManagementException
from uc3m_money.config.account_management_config import TRANSACTIONS_STORE_FILE

class IbanBalance:
    """docstring"""
    def __init__(self,iban):
        self._iban = IBAN(iban).value
        self.__last_balance_time = datetime.timestamp(datetime.now(timezone.utc))
        self.__balance = self.calculate_iban_balance()


    def calculate_iban_balance(self):
        """docstring"""
        transactions_list = self.read_input_file(TRANSACTIONS_STORE_FILE, raise_if_missing=True)
        iban_found = False
        total_balance = 0
        for transaction in transactions_list:
            # print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == self._iban:
                total_balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")
        return total_balance

    @staticmethod
    def read_input_file(input_file, raise_if_missing: bool = False) -> list:
        """Lee un archivo JSON y devuelve su contenido como lista.
        Si el archivo no existe, devuelve una lista vacía."""
        try:
            input_file = os.path.abspath(input_file)
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                return json.load(file)
        except FileNotFoundError as exc:
            if raise_if_missing:
                raise AccountManagementException('Wrong file or file path')
            return []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def to_json(self):

        return {"IBAN": self._iban,
                "time": self.__last_balance_time,
                "BALANCE": self.__balance}
