
from .attribute import Attribute

class TRANSFER(Attribute):
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid transfer amount"
        self._validation_pattern = r"^(?!10000\.0[1-9]|10000\.[1-9]\d)(10|1[1-9]|[2-9]\d|[1-9]\d{2,3}|10000(\.00)?)(\.\d{1,2})?$"
        self.value = attr_value  # Esto activará la validación

    def _validate(self, value):
        # Convertir a string si es un float/int
        if isinstance(value, (float, int)):
            value = str(value)
        return super()._validate(value)  #  value es string y el regex funciona
