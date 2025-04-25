from .attribute import Attribute

class FORMAT(Attribute):
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid transfer type"
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self.value = attr_value  # Esto activará la validación

    def _validate(self, value):
        value_upper = value.upper()
        return super()._validate(value_upper)  # Guarda en mayúsculas