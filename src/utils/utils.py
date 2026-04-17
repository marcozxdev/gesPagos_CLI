

import bcrypt


from datetime import datetime


def parse_number(value: str) -> int:
    value = value.replace(".", "").replace(",", "")
    return int(value)



def get_current_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# formatear monedas siguendo la regla de miles 
def format_currency(currency):
    return f"{currency:,}".replace(",", ".")



# encryptador de contraseña
def encrypte_password(pasword):
    pasword_bytes = pasword.encode("utf-8")

    salt = bcrypt.gensalt()
    hashed_pasword = bcrypt.hashpw(pasword_bytes, salt)

    return hashed_pasword




# valida la contraseña
def valide_pasword(input, dbhp):
    pasword_bytes = input.encode("utf-8")

    if bcrypt.checkpw(pasword_bytes, dbhp):
        return True
    else:
        False




# print(format_currency(100000))