from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from core.database import obtener_usuario_por_dni, actualizar_password
from utils.helpers import generar_nueva_contrasena
import logging

class RecuperarContrasenaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Recuperar Contraseña")
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()

        self.dni_label = QLabel("DNI:")
        self.dni_input = QLineEdit()
        self.recover_button = QPushButton("Recuperar")

        layout.addWidget(self.dni_label)
        layout.addWidget(self.dni_input)
        layout.addWidget(self.recover_button)

        self.setLayout(layout)
        self.recover_button.clicked.connect(self.recover)

    def recover(self):
        dni = self.dni_input.text()

        usuario = obtener_usuario_por_dni(dni)
        if not usuario:
            QMessageBox.warning(self, "Error", "No se encontró un usuario con ese DNI")
            return

        nueva_contrasena = generar_nueva_contrasena()
        if actualizar_password(dni, nueva_contrasena):
            QMessageBox.information(self, "Éxito", f"Tu nueva contraseña es: {nueva_contrasena}")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Ocurrió un problema al actualizar la contraseña")

