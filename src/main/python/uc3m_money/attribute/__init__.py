import re
from uc3m_money.account_management_exception import AccountManagementException


class Attribute():
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


class Concept(Attribute):
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid concept format"
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+$"
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
    class TRANSFER_DATE(Attribute):
        def __init__(self, attr_value):
            super().__init__()
            self._error_message = "Invalid date format"
            self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
            self.value = attr_value  # Esto activará la validación

