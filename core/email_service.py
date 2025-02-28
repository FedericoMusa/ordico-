import smtplib
import logging
from email.mime.text import MIMEText
from utils.config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD  # ✅ Usa config.py

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def enviar_correo(destinatario, asunto, mensaje):
    """Envía un correo electrónico asegurando codificación UTF-8."""
    try:
        # ✅ Especificar UTF-8 para evitar errores con caracteres especiales
        msg = MIMEText(mensaje, "plain", "utf-8")  
        msg['Subject'] = asunto
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = destinatario

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Habilita cifrado TLS
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Inicia sesión
            server.sendmail(EMAIL_ADDRESS, destinatario, msg.as_string())

        logging.info(f"✅ Correo enviado correctamente a {destinatario}")
        return True

    except smtplib.SMTPAuthenticationError:
        logging.error("❌ Error: Autenticación SMTP fallida. Verifica tu correo y contraseña.")
        return False
    except smtplib.SMTPException as e:
        logging.error(f"❌ Error SMTP al enviar correo: {e}")
        return False
    except Exception as e:
        logging.error(f"❌ Error inesperado al enviar correo: {e}")
        return False
