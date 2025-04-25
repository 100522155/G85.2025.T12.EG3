"""docstring"""
from uc3m_money.data.attribute.attribute import Attribute
from uc3m_money.account_management_exception import AccountManagementException
class DEPOSIT(Attribute):
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Error - Invalid deposit amount"
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}$"
        self._value = self._validate(attr_value)

    def _validate(self, value):
        value = super()._validate(value)

        try:
            amount = float(value[4:])
            if amount <= 0:
                raise AccountManagementException("Error - Deposit must be greater than 0")
        except ValueError:
            raise AccountManagementException(self._error_message)

        return amount

    @property
    def value(self):
        return self._value