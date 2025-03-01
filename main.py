import sys
import logging
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QMainWindow, QApplication, QHBoxLayout
from gui.login import LoginDialog
from gui.stock_window import StockWindow  
from gui.user_management_window import UserManagementWindow  
from gui.sales_window import SalesWindow  
from core.database import inicializar_db

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class MainWindow(QMainWindow):
    """Ventana principal según el rol del usuario."""
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Panel de Administración - ORDICO")
        self.setGeometry(100, 100, 400, 300)  

        if self.user_data["rol"] == "admin":
            self.show_admin_interface()
        else:
            self.show_cashier_interface()

    def show_admin_interface(self):
        """Interfaz para administrador."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)  

        self.btn_stock = QPushButton("Gestión de Stock")
        self.btn_users = QPushButton("Gestión de Usuarios")

        self.btn_stock.setFixedSize(200, 40)
        self.btn_users.setFixedSize(200, 40)

        btn_layout_stock = QHBoxLayout()
        btn_layout_stock.addStretch()
        btn_layout_stock.addWidget(self.btn_stock)
        btn_layout_stock.addStretch()

        btn_layout_users = QHBoxLayout()
        btn_layout_users.addStretch()
        btn_layout_users.addWidget(self.btn_users)
        btn_layout_users.addStretch()

        layout.addLayout(btn_layout_stock)
        layout.addLayout(btn_layout_users)

        self.btn_stock.clicked.connect(self.abrir_stock_window)
        self.btn_users.clicked.connect(self.abrir_users_window)

        self.central_widget.setLayout(layout)

    def abrir_stock_window(self):
        self.stock_window = StockWindow()
        self.stock_window.show()

    def abrir_users_window(self):
        self.user_management_window = UserManagementWindow()
        self.user_management_window.show()


def main():
    """Punto de entrada de la aplicación."""
    try:
        logging.info("✅ Inicializando la base de datos...")
        inicializar_db()  

        logging.info("✅ Creando la aplicación PyQt5...")
        app = QApplication(sys.argv)

        logging.info("✅ Mostrando ventana de inicio de sesión...")
        login_dialog = LoginDialog()

        if login_dialog.exec_():  
            user_data = login_dialog.get_authenticated_user()  

            if not user_data:
                logging.error("❌ No se obtuvo información del usuario autenticado. Saliendo del programa.")
                sys.exit(1)

            logging.info(f"✅ Usuario autenticado: {user_data}")
            main_window = MainWindow(user_data)  
            main_window.show()
            sys.exit(app.exec_())  
        else:
            logging.info("❌ El usuario cerró la ventana de login. Saliendo del programa.")
            sys.exit(0)

    except Exception as e:
        logging.error(f"❌ Error crítico en la aplicación: {e}", exc_info=True)
        print("❌ Ocurrió un error inesperado. Revisa el archivo de logs.")
        sys.exit(1)


if __name__ == "__main__":
    logging.info("🚀 Iniciando aplicación...")
    main()
