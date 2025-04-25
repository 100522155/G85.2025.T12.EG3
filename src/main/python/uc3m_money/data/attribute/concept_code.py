from uc3m_money.data.attribute.attribute import Attribute
class CONCEPT(Attribute):
    """"""
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid concept format"
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z])+(\s[a-zA-Z]+)+$"
        self.value = attr_value