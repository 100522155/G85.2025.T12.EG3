"""Account manager module """
import os
import json
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import (DEPOSITS_STORE_FILE, BALANCES_STORE_FILE)
from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.data.attribute.iban_balance import IbanBalance
from uc3m_money.storage.transfers_json_store import TransfersJsonStore

class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    #pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str,to_iban: str,concept: str,
                         transfer_type: str,date: str,amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""
        my_request = TransferRequest(from_iban=from_iban,to_iban=to_iban,
                                     transfer_concept=concept,transfer_type=transfer_type,
                                     transfer_date=date,transfer_amount=amount)

        transfer_store = TransfersJsonStore()
        transfer_store.add_item(my_request)
        return my_request.transfer_code

    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        deposit_file = self.read_input_file(input_file, raise_if_missing=True)
        try:
            deposit_iban = deposit_file["IBAN"]
            deposit_amount = deposit_file["AMOUNT"]
        except KeyError as e:
            raise AccountManagementException("Error - Invalid Key in JSON") from e

        deposit_obj = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=deposit_amount)

        deposits_json_store = DepositsJsonStore()
        deposits_json_store.add_item(deposit_obj)
        return deposit_obj.deposit_signature

        return deposit_obj.deposit_signature

    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        total_balance = IbanBalance(iban)
        balance_list = self.read_input_file(BALANCES_STORE_FILE)
        balance_list.append(total_balance.to_json())
        self.write_input_file(BALANCES_STORE_FILE, balance_list)
        return True

    @staticmethod
    def read_input_file(input_file, raise_if_missing: bool = False) -> list:
        """Lee un archivo JSON y devuelve su contenido como lista.
        Si el archivo no existe, devuelve una lista vacía."""
        try:
            input_file = os.path.abspath(input_file)
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                return json.load(file)
        except FileNotFoundError:
            if raise_if_missing:
                raise AccountManagementException('Wrong file or file path')
            return []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

    @staticmethod
    def write_input_file(input_file: str, data: list) -> None:
        """Escribe datos en un archivo JSON. Maneja errores de escritura."""
        try:
            input_file = os.path.abspath(input_file)
            with open(input_file, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)
        except (OSError, json.JSONDecodeError) as ex:
            raise AccountManagementException("Wrong file or file path or JSON decode error") from ex
