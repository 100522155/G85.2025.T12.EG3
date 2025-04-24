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
