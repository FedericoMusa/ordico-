from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from core.auth import autenticar_usuario
from gui.register import RegistroDialog  # ✅ Importamos la ventana de registro
from gui.recovery import RecuperarContrasenaDialog  # ✅ Importamos la recuperación de contraseña
import logging

class LoginDialog(QDialog):
    """Ventana de inicio de sesión."""
    
    def __init__(self):
        super().__init__()
        self.authenticated_user = None  # ✅ Asegurar que existe el atributo
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz gráfica del login."""
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 400, 250)  # ✅ Ajuste de tamaño
        self.setMinimumSize(400, 250)

        layout = QVBoxLayout()

        self.username_label = QLabel("Usuario o Email:")  # ✅ Ahora permite email o usuario
        self.username_input = QLineEdit()
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Iniciar Sesión")
        self.register_button = QPushButton("Registrarse")  # ✅ Botón de registro
        self.forgot_password_button = QPushButton("¿Olvidaste tu contraseña?")  # ✅ Recuperación de contraseña

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)  # ✅ Se agrega el botón de "Registrarse"
        layout.addWidget(self.forgot_password_button)  # ✅ Se agrega la opción de recuperación

        self.setLayout(layout)
        self.show()
        logging.info("✅ Ventana de inicio de sesión mostrada correctamente.")

        # ✅ Conectar botones con sus funciones
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.open_register)  # ✅ Abre ventana de registro
        self.forgot_password_button.clicked.connect(self.open_recovery)  # ✅ Abre recuperación de contraseña

    def login(self):
        """Función para manejar el inicio de sesión."""
        entrada = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not entrada or not password:
            QMessageBox.warning(self, "Error", "Debe ingresar usuario/email y contraseña.")
            return

        logging.info(f"Intentando iniciar sesión con usuario/email: {entrada}")
        usuario = autenticar_usuario(entrada, password)

        if usuario:
            logging.info(f"✅ Inicio de sesión exitoso. Usuario: {usuario['username']}")
            self.authenticated_user = usuario  # ✅ Guardamos los datos del usuario autenticado
            QMessageBox.information(self, "Éxito", f"Bienvenido {usuario['username']} ({usuario['rol']})")
            self.accept()  # ✅ Se cierra el diálogo correctamente
        else:
            logging.warning("❌ Nombre de usuario o contraseña incorrectos.")
            QMessageBox.warning(self, "Error", "Nombre de usuario o contraseña incorrectos.")

    def open_register(self):
        """Abre la ventana de registro."""
        self.registro_dialog = RegistroDialog()
        self.registro_dialog.exec_()

    def open_recovery(self):
        """Abre la ventana de recuperación de contraseña."""
        self.recuperar_contrasena_dialog = RecuperarContrasenaDialog()
        self.recuperar_contrasena_dialog.exec_()

    def get_authenticated_user(self):
        """Devuelve el usuario autenticado."""
        return self.authenticated_user  # ✅ Devuelve la información del usuario autenticado correctamente
