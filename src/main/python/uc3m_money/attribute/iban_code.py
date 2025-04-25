"""docstring"""
from uc3m_money.attribute.attribute import Attribute
from uc3m_money.account_management_exception import AccountManagementException


class IBAN(Attribute):
    """verificar iban"""
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid IBAN format"
        self._validation_pattern = r"^ES[0-9]{22}$"
        self.value = attr_value  # Esto activará la validación

    def _validate(self, value: str) -> str:
        """Method for validating an IBAN including control digit check"""
        # Primero validar el formato básico con el patrón regex
        iban = super()._validate(value)
        original_code = iban[2:4]
        # replacing the control
        iban = iban[:2] + "00" + iban[4:]
        iban = iban[4:] + iban[:4]

        # Convertir el IBAN en una cadena numérica, reemplazando letras por números
        iban = (iban.replace('A', '10').replace('B', '11').
                replace('C', '12').replace('D', '13').replace('E', '14').
                replace('F', '15'))
        iban = (iban.replace('G', '16').replace('H', '17').
                replace('I', '18').replace('J', '19').replace('K', '20').
                replace('L', '21'))
        iban = (iban.replace('M', '22').replace('N', '23').
                replace('O', '24').replace('P', '25').replace('Q', '26').
                replace('R', '27'))
        iban = (iban.replace('S', '28').replace('T', '29').replace('U', '30').
                replace('V', '31').replace('W', '32').replace('X', '33'))
        iban = iban.replace('Y', '34').replace('Z', '35')

        # Mover los cuatro primeros caracteres al final

        # Convertir la cadena en un número entero
        int_i = int(iban)

        # Calcular el módulo 97
        mod = int_i % 97

        # Calcular el dígito de control (97 menos el módulo)
        dc = 98 - mod

        if int(original_code) != dc:
            # print(dc)
            raise AccountManagementException("Invalid IBAN control digit")

        return value