"""Account manager module """
import re
import json
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import (TRANSFERS_STORE_FILE,
                                        DEPOSITS_STORE_FILE,
                                        TRANSACTIONS_STORE_FILE,
                                        BALANCES_STORE_FILE)

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit

class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def valivan(iban: str):
        """
    Calcula el dígito de control de un IBAN español.
        """
        iban_regex = re.compile(r"^ES[0-9]{22}")
        result_iban = iban_regex.fullmatch(iban)
        if not result_iban:
            raise AccountManagementException("Invalid IBAN format")
        original_code = iban[2:4]
        #replacing the control
        iban = iban[:2] + "00" + iban[4:]
        iban = iban[4:] + iban[:4]

        # Crear tabla de traducción
        translation_table = str.maketrans({
            'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15',
            'G': '16', 'H': '17', 'I': '18', 'J': '19', 'K': '20', 'L': '21',
            'M': '22', 'N': '23', 'O': '24', 'P': '25', 'Q': '26', 'R': '27',
            'S': '28', 'T': '29', 'U': '30', 'V': '31', 'W': '32', 'X': '33',
            'Y': '34', 'Z': '35'
        })

        # Aplicar traducción en una sola operación
        iban = iban.translate(translation_table)

        #Calcular el dígito de control: cadena a número entero, sacar módulo 97 y calcular dígito de control
        control_digit = 98 - int(iban) % 97

        if int(original_code) != control_digit:
            raise AccountManagementException("Invalid IBAN control digit")
        return iban

    def validate_concept(self, concept: str):
        """regular expression for checking the minimum and maximum length as well as
        the allowed characters and spaces restrictions
        there are other ways to check this"""
        myregex = re.compile(r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$")

        result_format = myregex.fullmatch(concept)
        if not result_format:
            raise AccountManagementException ("Invalid concept format")

    def validate_transfer_date(self, transfer_date):
        """validates the arrival date format  using regex"""
        myregex = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")

        result_format = myregex.fullmatch(transfer_date)
        if not result_format:
            raise AccountManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(transfer_date, "%d/%m/%Y").date()
        except ValueError as ex:
            raise AccountManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise AccountManagementException("Transfer date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise AccountManagementException("Invalid date format")
        return transfer_date
    #pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""
        self.valivan(from_iban)
        self.valivan(to_iban)
        self.validate_concept(concept)
        myregex = re.compile(r"(ORDINARY|INMEDIATE|URGENT)")
        result_format = myregex.fullmatch(transfer_type)
        if not result_format:
            raise AccountManagementException("Invalid transfer type")
        self.validate_transfer_date(date)

        try:
            float_amount  = float(amount)
        except ValueError as exc:
            raise AccountManagementException("Invalid transfer amount") from exc

        string_amount = str(float_amount)
        if '.' in string_amount:
            decimales = len(string_amount.split('.')[1])
            if decimales > 2:
                raise AccountManagementException("Invalid transfer amount")

        if float_amount < 10 or float_amount > 10000:
            raise AccountManagementException("Invalid transfer amount")

        my_request = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=date,
                                     transfer_amount=amount)

        transfer_list = self._read_json_file(TRANSFERS_STORE_FILE)

        for transfer_item in transfer_list:
            if (transfer_item["from_iban"] == my_request.from_iban and
                    transfer_item["to_iban"] == my_request.to_iban and
                    transfer_item["transfer_date"] == my_request.transfer_date and
                    transfer_item["transfer_amount"] == my_request.transfer_amount and
                    transfer_item["transfer_concept"] == my_request.transfer_concept and
                    transfer_item["transfer_type"] == my_request.transfer_type):
                raise AccountManagementException("Duplicated transfer in transfer list")

        transfer_list.append(my_request.to_json())



        try:
            with open(TRANSFERS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(transfer_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        return my_request.transfer_code

    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        deposit_file = self.manage_read_file(input_file)

        # comprobar valores del fichero
        try:
            deposit_iban = deposit_file["IBAN"]
            deposit_amount = deposit_file["AMOUNT"]
        except KeyError as e:
            raise AccountManagementException("Error - Invalid Key in JSON") from e

        deposit_iban = self.valivan(deposit_iban)
        myregex = re.compile(r"^EUR [0-9]{4}\.[0-9]{2}")
        result = myregex.fullmatch(deposit_amount)
        if not result:
            raise AccountManagementException("Error - Invalid deposit amount")

        deposit_amount_valid = float(deposit_amount[4:])
        if deposit_amount_valid == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")

        deposit_obj = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=deposit_amount_valid)

        deposit_list = self._read_json_file(DEPOSITS_STORE_FILE)
        deposit_list.append(deposit_obj.to_json())

        self._write_json_file(DEPOSITS_STORE_FILE, deposit_list)
        return deposit_obj.deposit_signature

    def manage_read_file(self, file_path: str):
        return self._read_json_file(file_path, raise_if_missing=True)

    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        iban = self.valivan(iban)
        transactions_list = self.manage_read_file(TRANSACTIONS_STORE_FILE)
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

        balance_list = self._read_json_file(BALANCES_STORE_FILE)
        balance_list.append(last_balance)
        self._write_json_file(BALANCES_STORE_FILE,balance_list)
        return True

    def _read_json_file(file_path: str, raise_if_missing: bool = False) -> list:
        """Lee un archivo JSON y devuelve su contenido como lista.
        Si el archivo no existe, devuelve una lista vacía."""
        try:
            with open(file_path, "r", encoding="utf-8", newline="") as file:
                return json.load(file)
        except FileNotFoundError:
            if raise_if_missing:
                raise AccountManagementException("Wrong file or file path")
            return []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def _write_json_file(file_path: str, data: list) -> None:
        """Escribe datos en un archivo JSON. Maneja errores de escritura."""
        try:
            with open(file_path, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)
        except (FileNotFoundError, IOError) as ex:
            raise AccountManagementException("Wrong file or file path") from ex