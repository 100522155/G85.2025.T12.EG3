"""docstring"""
from .attribute import Attribute
from uc3m_money.exception.account_management_exception import AccountManagementException


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