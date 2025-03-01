from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from core.auth import autenticar_usuario
from gui.register import RegistroDialog  
from gui.recovery import RecuperarContrasenaDialog  
import logging

class LoginDialog(QDialog):
    """Ventana de inicio de sesión con diseño optimizado."""

    def __init__(self):
        super().__init__()
        self.authenticated_user = None  
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Inicio de Sesión - ORDICO")
        self.setGeometry(100, 100, 400, 250)  
        self.setMinimumSize(400, 250)

        layout = QVBoxLayout()

        self.username_label = QLabel("Usuario o Email:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Iniciar Sesión")
        self.register_button = QPushButton("Registrarse")  
        self.forgot_password_button = QPushButton("¿Olvidaste tu contraseña?")  

        button_style = """
            QPushButton {
                background-color: #8B0000;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #A52A2A;
            }
        """
        self.login_button.setStyleSheet(button_style)
        self.register_button.setStyleSheet(button_style)
        self.forgot_password_button.setStyleSheet("color: #8B0000; font-weight: bold;")

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)  
        layout.addWidget(self.forgot_password_button)  

        self.setLayout(layout)
        self.show()
        logging.info("✅ Ventana de inicio de sesión mostrada correctamente.")

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.open_register)  
        self.forgot_password_button.clicked.connect(self.open_recovery)  

    def login(self):
        entrada = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not entrada or not password:
            QMessageBox.warning(self, "Error", "Debe ingresar usuario/email y contraseña.")
            return

        logging.info(f"Intentando iniciar sesión con usuario/email: {entrada}")
        usuario = autenticar_usuario(entrada, password)

        if usuario:
            logging.info(f"✅ Inicio de sesión exitoso. Usuario: {usuario['username']}")
            self.authenticated_user = usuario  
            QMessageBox.information(self, "Éxito", f"Bienvenido {usuario['username']} ({usuario['rol']})")
            self.accept()  
        else:
            logging.warning("❌ Nombre de usuario o contraseña incorrectos.")
            QMessageBox.warning(self, "Error", "Nombre de usuario o contraseña incorrectos.")

    def open_register(self):
        self.registro_dialog = RegistroDialog()
        self.registro_dialog.exec_()

    def open_recovery(self):
        self.recuperar_contrasena_dialog = RecuperarContrasenaDialog()
        self.recuperar_contrasena_dialog.exec_()

    def get_authenticated_user(self):
        return self.authenticated_user  
    