"""docstring"""
import re
from uc3m_money.account_management_exception import AccountManagementException


class Attribute:
    """fijar atributos"""
    def __init__(self):
        self._attr_value = ""
        self._error_message = ""
        self._validation_pattern = r""

    def _validate(self, value: str):
        """Validates the value against the validation pattern"""
        myregex = re.compile(self._validation_pattern)
        regex_natches = myregex.fullmatch(value)
        if not regex_natches:
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

