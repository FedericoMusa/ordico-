#Interfaz de Administración de Usuarios#
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from core.database import conectar_db, eliminar_usuario
import logging

class AdminUsersDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Administrar Usuarios")
        self.setGeometry(100, 100, 500, 400)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre de Usuario", "Correo Electrónico", "Rol", "Acciones"])
        self.cargar_usuarios()

        layout.addWidget(self.table)
        self.setLayout(layout)

    def cargar_usuarios(self):
        """
        Carga los usuarios desde la base de datos y los muestra en la tabla.
        """
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, email, rol FROM usuarios")
            usuarios = cursor.fetchall()

        self.table.setRowCount(len(usuarios))

        for i, usuario in enumerate(usuarios):
            self.table.setItem(i, 0, QTableWidgetItem(usuario[0]))  # Username
            self.table.setItem(i, 1, QTableWidgetItem(usuario[1]))  # Email
            self.table.setItem(i, 2, QTableWidgetItem(usuario[2]))  # Rol
            
            delete_button = QPushButton("Eliminar")
            delete_button.clicked.connect(lambda ch, row=i: self.eliminar_usuario(row))
            self.table.setCellWidget(i, 3, delete_button)

    def eliminar_usuario(self, row):
        """
        Elimina un usuario seleccionado y actualiza la tabla.
        """
        username = self.table.item(row, 0).text()
        if eliminar_usuario(username):
            logging.info(f"Usuario eliminado: {username}")
            self.table.removeRow(row)
        else:
            logging.error(f"No se pudo eliminar al usuario: {username}")
# Compare this snippet from ui/main_window.py:
