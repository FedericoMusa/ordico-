from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from core.auth import registrar_usuario

class RegistroDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(100, 100, 300, 300)
        layout = QVBoxLayout()

        self.username_label = QLabel("Nombre de usuario:")
        self.username_input = QLineEdit()
        self.email_label = QLabel("Correo Electrónico:")
        self.email_input = QLineEdit()
        self.dni_label = QLabel("DNI:")  # ✅ Se agrega el campo para DNI
        self.dni_input = QLineEdit()
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton("Registrarse")

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.dni_label)  # ✅ Campo agregado
        layout.addWidget(self.dni_input)  # ✅ Campo agregado
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)

        self.setLayout(layout)
        self.register_button.clicked.connect(self.register)

    def register(self):
        """Registra un usuario con email y DNI."""
        username = self.username_input.text()
        email = self.email_input.text()
        dni = self.dni_input.text()
        password = self.password_input.text()

        mensaje = registrar_usuario(username, password, email, dni, "usuario")

        if "exitosamente" in mensaje:
            QMessageBox.information(self, "Éxito", mensaje)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", mensaje)

