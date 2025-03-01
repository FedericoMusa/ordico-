from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from core.auth import registrar_usuario

class RegistroDialog(QDialog):
    """Ventana de registro de usuarios con validación y diseño optimizado."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Registro de Usuario - ORDICO")
        self.setGeometry(100, 100, 350, 400)  

        layout = QVBoxLayout()

        self.username_label = QLabel("Nombre de usuario:")
        self.username_input = QLineEdit()

        self.email_label = QLabel("Correo Electrónico:")
        self.email_input = QLineEdit()

        self.dni_label = QLabel("DNI:")
        self.dni_input = QLineEdit()

        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Registrarse")
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
        self.register_button.setStyleSheet(button_style)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.dni_label)
        layout.addWidget(self.dni_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)

        self.setLayout(layout)
        self.register_button.clicked.connect(self.register)

    def register(self):
        """Registra un usuario con validación."""
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        dni = self.dni_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not email or not dni or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        mensaje = registrar_usuario(username, password, email, dni, "usuario")

        if "exitosamente" in mensaje:
            QMessageBox.information(self, "Éxito", mensaje)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", mensaje)

