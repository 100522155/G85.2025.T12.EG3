"""Docstring"""
import re
from datetime import datetime, timezone
from uc3m_money.exception.account_management_exception import AccountManagementException


class Attribute:
    """fijar atributos"""
    def __init__(self):
        self._attr_value = ""
        self._error_message = ""
        self._validation_pattern = r""

    def _validate(self, value: str):
        """Validates the value against the validation pattern"""
        myregex = re.compile(self._validation_pattern)
        res = myregex.fullmatch(value)
        if not res:
            raise AccountManagementException(self._error_message)
        return value

    @property
    def value(self):
        """Getter for the attribute value"""
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        """Setter with validation"""
        self._attr_value = self._validate(attr_value)


class CONCEPT(Attribute):
    """"""
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid concept format"
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z])+(\s[a-zA-Z]+)+$"
        self.value = attr_value

class IBAN(Attribute):
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid IBAN format"
        self._validation_pattern = r"^ES[0-9]{22}$"
        self.value = attr_value  # Esto activará la validación

    def _validate(self, iban: str) -> str:
        """Method for validating an IBAN including control digit check"""
        # Primero validar el formato básico con el patrón regex
        super()._validate(iban)
        # Validación del dígito de control
        original_code = iban[2:4]
        # Reemplazar el código de control por 00 para el cálculo
        iban = iban[:2] + "00" + iban[4:]
        # Mover los primeros 4 caracteres al final
        iban = iban[4:] + iban[:4]
        # Crear tabla de traducción de letras a números
        translation_table = str.maketrans({
            'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15',
            'G': '16', 'H': '17', 'I': '18', 'J': '19', 'K': '20', 'L': '21',
            'M': '22', 'N': '23', 'O': '24', 'P': '25', 'Q': '26', 'R': '27',
            'S': '28', 'T': '29', 'U': '30', 'V': '31', 'W': '32', 'X': '33',
            'Y': '34', 'Z': '35'
        })
        # Aplicar traducción
        iban_numeric = iban.translate(translation_table)
        # Calcular dígito de control (98 - (mod 97))
        calculated_code = 98 - (int(iban_numeric) % 97)
        # Comprobar que coincide con el código original
        if int(original_code) != calculated_code:
            raise AccountManagementException("Invalid IBAN control digit")

        return iban

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


class DATE(Attribute):
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid date format"
        self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self.value = attr_value  # Esto activará la validación


    def _validate(self, transfer_date):
        super()._validate(transfer_date)

        try:
            my_date = datetime.strptime(transfer_date, "%d/%m/%Y").date()
            if not (2025 <= my_date.year <= 2050):
                raise AccountManagementException("Invalid date format")
            if my_date < datetime.now(timezone.utc).date():
                raise AccountManagementException("Transfer date must be today or later.")
        except ValueError:
            raise AccountManagementException("Invalid date format")

class FORMAT(Attribute):
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid transfer type"
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self.value = attr_value  # Esto activará la validación

class TRANSFER(Attribute):
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid transfer amount"
        self._validation_pattern = r"^(10|1[1-9]|[2-9]\d|[1-9]\d{2,3}|10000)(\.\d{1,2})?$"
        self.value = attr_value  # Esto activará la validación

    def _validate(self, value):
        # Convertir a string si es un float/int
        if isinstance(value, (float, int)):
            value = str(value)
        return super()._validate(value)  # Ahora value es string y el regex funciona

class DEPOSIT(Attribute):
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Error - Invalid deposit amount"
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}"
        self.value = attr_value  # Esto activará la validación
    def _validate(self,deposit_amount):

        super()._validate(deposit_amount)
        deposit_amount_valid = float(deposit_amount[4:])
        if deposit_amount_valid == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")