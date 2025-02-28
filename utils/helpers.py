import random
import string

def generar_codigo_verificacion(longitud=6):
    """
    Genera un código de verificación aleatorio compuesto por letras y números.
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def generar_nueva_contrasena(longitud=8):
    """
    Genera una nueva contraseña aleatoria de una longitud específica.
    """
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))
