import re

def validar_email(email):
    """
    Verifica si el email tiene un formato válido usando una expresión regular.
    """
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    return re.match(regex, email) is not None
