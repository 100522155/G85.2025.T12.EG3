"""Account manager module """
import json
from datetime import datetime, timezone
from wsgiref.validate import validator

from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import (TRANSFERS_STORE_FILE,DEPOSITS_STORE_FILE,
                                        TRANSACTIONS_STORE_FILE,BALANCES_STORE_FILE)
from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit
from uc3m_money.attribute import IBAN, CONCEPT, DATE, FORMAT, TRANSFER, DEPOSIT  # Nuevas clases

class AccountManager:
    """Class for providing the methods for managing the orders"""

    def __init__(self):
        pass

    def transfer_request(self, from_iban: str, to_iban: str, concept: str,
                         transfer_type: str, date: str,amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""
        IBAN(from_iban)
        IBAN(to_iban)
        CONCEPT(concept)
        FORMAT(transfer_type)
        DATE(date)
        TRANSFER(amount)

        my_request = TransferRequest(from_iban,to_iban,concept,transfer_type,date,amount)

        transfer_list = self.load_json_store(TRANSFERS_STORE_FILE)
        for transfer_item in transfer_list:
            if (transfer_item["from_iban"] == my_request.from_iban and
                    transfer_item["to_iban"] == my_request.to_iban and
                    transfer_item["transfer_date"] == my_request.transfer_date and
                    transfer_item["transfer_amount"] == my_request.transfer_amount and
                    transfer_item["transfer_concept"] == my_request.transfer_concept and
                    transfer_item["transfer_type"] == my_request.transfer_type):
                raise AccountManagementException("Duplicated transfer in transfer list")

        transfer_list.append(my_request.to_json())
        self._write_json_file(TRANSFERS_STORE_FILE, transfer_list)
        return my_request.transfer_code

    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        deposit_file = self.load_json_store(input_file, raise_if_missing= True )
        deposit_iban, deposit_amount = DEPOSIT(deposit_file)
        # comprobar valores del fichero

        deposit_obj = AccountDeposit(deposit_iban,deposit_amount) # quitadas especif innecesarias

        deposit_list = self.load_json_store(DEPOSITS_STORE_FILE)
        deposit_list.append(deposit_obj.to_json())
        self._write_json_file(DEPOSITS_STORE_FILE, deposit_list)

        return deposit_obj.deposit_signature

    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        IBAN(iban)
        transactions_list = self.load_json_store(TRANSACTIONS_STORE_FILE, raise_if_missing=True)
        iban_found = False
        total_balance = 0
        for transaction in transactions_list:
            #print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == iban:
                total_balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")

        last_balance = {"IBAN": iban,
                        "time": datetime.timestamp(datetime.now(timezone.utc)),
                        "BALANCE": total_balance}

        balance_list = self.load_json_store(BALANCES_STORE_FILE)
        balance_list.append(last_balance)
        self._write_json_file(BALANCES_STORE_FILE,balance_list)
        return True

    @staticmethod
    def load_json_store(file_store, raise_if_missing: bool = False  ) -> list :
        """Lee un archivo JSON y devuelve su contenido como lista.
        Si el archivo no existe, devuelve una lista vacía."""
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                return json.load(file)
        except FileNotFoundError:
            if raise_if_missing:
                raise AccountManagementException("Wrong file or file path")
            return []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

    @staticmethod
    def _write_json_file(file_path: str, data: list) -> None:
        """Escribe datos en un archivo JSON. Maneja errores de escritura."""
        try:
            with open(file_path, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)
        except (OSError, json.JSONDecodeError) as ex:
            raise AccountManagementException("Wrong file or file path or JSON decode error") from ex
