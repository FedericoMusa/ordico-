from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from core.auth import registrar_usuario
import logging
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from core.auth import registrar_usuario
import logging

class AdminUsersDialog(QDialog):
    """Ventana de administración de usuarios."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz de administración de usuarios."""
        self.setWindowTitle("Administrar Usuarios")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.label_username = QLabel("Nombre de Usuario:")
        self.input_username = QLineEdit()

        self.label_email = QLabel("Correo Electrónico:")
        self.input_email = QLineEdit()

        self.label_dni = QLabel("DNI:")
        self.input_dni = QLineEdit()

        self.label_password = QLabel("Contraseña:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.label_rol = QLabel("Selecciona el rol:")
        self.combo_roles = QComboBox()
        self.combo_roles.addItems(["admin", "cajero", "vendedor"])

        self.btn_registrar = QPushButton("Registrar Usuario")
        self.btn_registrar.clicked.connect(self.crear_usuario)

        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)
        layout.addWidget(self.label_dni)
        layout.addWidget(self.input_dni)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_rol)
        layout.addWidget(self.combo_roles)
        layout.addWidget(self.btn_registrar)

        self.setLayout(layout)

    def crear_usuario(self):
        """Registra un usuario con el rol seleccionado."""
        username = self.input_username.text().strip()
        email = self.input_email.text().strip()
        dni = self.input_dni.text().strip()
        password = self.input_password.text().strip()
        rol = self.combo_roles.currentText()

        if not username or not email or not dni or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        mensaje = registrar_usuario(username, password, email, dni, rol)

        if "exitosamente" in mensaje:
            QMessageBox.information(self, "Éxito", mensaje)
            logging.info(f"✅ Usuario creado: {username} con rol {rol}")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", mensaje)
