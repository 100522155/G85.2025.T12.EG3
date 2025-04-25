"""docstring"""
from datetime import datetime, timezone
from uc3m_money.attribute.attribute import Attribute
from uc3m_money.account_management_exception import AccountManagementException


class DATE(Attribute):
    """docstring"""
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid date format"
        self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self.value = attr_value  # Esto activará la validación


    def _validate(self, value):
        value = super()._validate(value)
        try:
            my_date = datetime.strptime(value, "%d/%m/%Y").date()
            if not (2025 <= my_date.year <= 2050):
                raise AccountManagementException("Invalid date format")
            if my_date < datetime.now(timezone.utc).date():
                raise AccountManagementException("Transfer date must be today or later.")
        except ValueError:
            raise AccountManagementException("Invalid date format")
        return value