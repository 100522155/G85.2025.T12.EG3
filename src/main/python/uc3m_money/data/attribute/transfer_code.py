
from uc3m_money.data.attribute.attribute import Attribute
from uc3m_money.account_management_exception import AccountManagementException

class TRANSFER(Attribute):
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid transfer amount"
        self._validation_pattern = r"^(?!10000\.0[1-9]|10000\.[1-9]\d)(10|1[1-9]|[2-9]\d|[1-9]\d{2,3}|10000(\.00)?)(\.\d{1,2})?$"
        self.value = attr_value  # Esto activará la validación

    def _validate(self, value):
        # Convertir a string y normalizar formato decimal
        n_str = str(value)
        if '.' in n_str:
            decimales = len(n_str.split('.')[1])
            if decimales > 2:
                raise AccountManagementException("Invalid transfer amount")
        if isinstance(value, (float, int)):
            # Formatear a 2 decimales, eliminar .0 si es entero
            value = "{0:.2f}".format(float(value)).replace(".00", "")

        validated_value = super()._validate(value)
        try:
            f_amount  = float(value)
        except ValueError as exc:
            raise AccountManagementException("Invalid transfer amount") from exc

        if f_amount < 10 or f_amount > 10000:
            raise AccountManagementException("Invalid transfer amount")

        # Devolver como float para consistencia
        return float(validated_value)


