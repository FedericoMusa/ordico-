import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env (opcional)
load_dotenv()

# Configuración de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio actual
DB_PATH = "ordico.db"

# Configuración del correo electrónico
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "tu_correo@gmail.com")  # Reemplaza con tu correo
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "tu_contraseña_de_aplicación")  # Usa una contraseña de aplicación de Gmail

# Otras configuraciones generales
APP_NAME = "ORDICO"
VERSION = "1.0"
DEBUG_MODE = True  # Cambia a False en producción
