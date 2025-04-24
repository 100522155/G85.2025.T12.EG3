"""
def valivan(self, iban: str):

#Calcula el dígito de control de un IBAN español.

    iban_regex = re.compile(r"^ES[0-9]{22}")
    self.check_format(iban,iban_regex)

    original_code = iban[2:4]
    #replacing the control
    iban = iban[:2] + "00" + iban[4:]
    iban = iban[4:] + iban[:4]

    # Crear tabla de traducción
    translation_table = str.maketrans({
        'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15',
        'G': '16', 'H': '17', 'I': '18', 'J': '19', 'K': '20', 'L': '21',
        'M': '22', 'N': '23', 'O': '24', 'P': '25', 'Q': '26', 'R': '27',
        'S': '28', 'T': '29', 'U': '30', 'V': '31', 'W': '32', 'X': '33',
        'Y': '34', 'Z': '35'
    })

    # Aplicar traducción en una sola operación
    iban = iban.translate(translation_table)

    #Calcular el dígito de control: cadena a número entero, sacar módulo 97 y calcular dígito de control
    control_digit = 98 - int(iban) % 97

    if int(original_code) != control_digit:
        raise AccountManagementException("Invalid IBAN control digit")
    return iban
"""
"""
def validate_concept(self, concept: str):
    #regular expression for checking the minimum and maximum length as well as
    the allowed characters and spaces restrictions
    there are other ways to check this
    Concept(concept)
"""

"""
def validate_transfer_date(self, transfer_date):
    #validates the arrival date format  using regex
    DATE(transfer_date)

    try:
        my_date = datetime.strptime(transfer_date, "%d/%m/%Y").date()
    except ValueError as ex:
        raise AccountManagementException("Invalid date format") from ex

    if my_date < datetime.now(timezone.utc).date():
        raise AccountManagementException("Transfer date must be today or later.")

    if my_date.year < 2025 or my_date.year > 2050:
        raise AccountManagementException("Invalid date format")
    return transfer_date
"""

"""        try:
            float_amount  = float(amount)
        except ValueError as exc:
            raise AccountManagementException("Invalid transfer amount") from exc

        string_amount = str(float_amount)
        if '.' in string_amount:
            decimales = len(string_amount.split('.')[1])
            if decimales > 2:
                raise AccountManagementException("Invalid transfer amount")

        if float_amount < 10 or float_amount > 10000:
            raise AccountManagementException("Invalid transfer amount")
"""

"""    def check_format(self, to_verify, regex):
        result = regex.fullmatch(to_verify)
        if not result:
            raise AccountManagementException("Error - Invalid format")"""
"""
try:
    deposit_iban = deposit_file["IBAN"]
    deposit_amount = deposit_file["AMOUNT"]

    super()._validate(deposit_amount)
    IBAN(deposit_iban)

    deposit_amount_valid = float(deposit_amount[4:])
    if deposit_amount_valid == 0:
        raise AccountManagementException("Error - Deposit must be greater than 0")

    return deposit_iban, deposit_amount
except KeyError as e:
    raise AccountManagementException("Error - Invalid Key in JSON") from e
"""