from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class SalesWindow(QDialog):
    "ventana de ventas (para cajeros)"
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle("Ventas-Cajero")
        self.setGeometry(150, 150, 600, 400) # Ajustar tamaño proporcional

        layout=QVBoxLayout()
        label=QLabel("en desarrollo")
        layout.addWidget(label)
        self.setLayout(layout)
