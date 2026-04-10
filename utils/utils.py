

import bcrypt




# encryptador de contraseña
def encrypte_password(pasword):
    pasword_bytes = pasword.encode("utf-8")

    salt = bcrypt.gensalt()
    hached_pasword = bcrypt.hashpw(pasword_bytes, salt)

    return hached_pasword




# valida la contraseña
def valide_pasword(input, dbhp):
    pasword_bytes = input.encode("utf-8")

    if bcrypt.checkpw(pasword_bytes, dbhp):
        return True
    else:
        False
