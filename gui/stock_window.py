from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
from core.database import obtener_productos, agregar_producto, actualizar_producto, eliminar_producto
import logging
import pandas as pd

class StockWindow(QWidget):
    """Ventana para la gestión del stock de productos."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de gestión de stock."""
        self.setWindowTitle("Gestión de Stock")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Gestión de Stock")
        layout.addWidget(self.label)

        self.tabla_stock = QTableWidget()
        self.tabla_stock.setColumnCount(4)
        self.tabla_stock.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Precio"])
        layout.addWidget(self.tabla_stock)

        self.btn_actualizar = QPushButton("Actualizar Stock")
        self.btn_agregar = QPushButton("Agregar Producto")
        self.btn_editar = QPushButton("Editar Producto")
        self.btn_eliminar = QPushButton("Eliminar Producto")
        self.btn_importar = QPushButton("Importar desde Excel")
        
        layout.addWidget(self.btn_importar)
        layout.addWidget(self.btn_actualizar)
        layout.addWidget(self.btn_agregar)
        layout.addWidget(self.btn_editar)
        layout.addWidget(self.btn_eliminar)

        self.btn_importar.clicked.connect(self.importar_desde_excel)
        self.btn_actualizar.clicked.connect(self.cargar_stock)
        self.btn_agregar.clicked.connect(self.agregar_producto)
        self.btn_editar.clicked.connect(self.editar_producto)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)

        self.setLayout(layout)
        self.cargar_stock()

    def cargar_stock(self):
        """Carga los productos en la tabla desde la base de datos."""
        try:
            productos = obtener_productos()

            if productos is None:
                logging.error("Error: obtener_productos() devolvió None")
                productos = []  # Evita el error asignando una lista vacía

            print("Productos obtenidos:", productos)  # Muestra en la consola
            logging.debug(f"Productos obtenidos: {productos}")  # Registro en logs

            self.tabla_stock.setRowCount(len(productos))

            for i, producto in enumerate(productos):
                for j, dato in enumerate(producto):
                    self.tabla_stock.setItem(i, j, QTableWidgetItem(str(dato)))

        except Exception as e:
            logging.error(f"Error al cargar stock: {e}")
            print(f"❌ Error al cargar stock: {e}")

                
    def agregar_producto(self):
        """Agrega un nuevo producto al stock."""
        nombre = "Nuevo Producto"
        cantidad = 10
        precio = 100.0

        if agregar_producto(nombre, cantidad, precio):
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            self.cargar_stock()
        else:
            QMessageBox.warning(self, "Error", "No se pudo agregar el producto.")

    def editar_producto(self):
        """Edita el producto seleccionado en la tabla."""
        fila = self.tabla_stock.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione un producto para editar.")
            return

        id_producto = self.tabla_stock.item(fila, 0).text()
        nuevo_precio = 120.0  # Ejemplo

        if actualizar_producto(id_producto, nuevo_precio):
            QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")
            self.cargar_stock()
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar el producto.")

    def eliminar_producto(self):
        """Elimina el producto seleccionado."""
        fila = self.tabla_stock.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Seleccione un producto para eliminar.")
            return

        id_producto = self.tabla_stock.item(fila, 0).text()

        if eliminar_producto(id_producto):
            QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
            self.cargar_stock()
        else:
            QMessageBox.warning(self, "Error", "No se pudo eliminar el producto.")
    def importar_desde_excel(self):
        """Abre un diálogo para importar productos desde un archivo Excel."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Archivos Excel (*.xlsx *.csv);;Todos los archivos (*)", options=options)
        
        if not file_path:
            return  # Si el usuario cancela, no hacer nada
        
        try:
            # 📌 Detectar si es CSV o Excel
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            # 📌 Verificar que el archivo tenga las columnas necesarias
            columnas_requeridas = {"ID", "Nombre", "Cantidad", "Precio"}
            if not columnas_requeridas.issubset(df.columns):
                QMessageBox.warning(self, "Error", "El archivo no tiene las columnas requeridas: ID, Nombre, Cantidad, Precio")
                return

            # 📌 Insertar productos en la base de datos
            for _, row in df.iterrows():
                id_producto = row["ID"]
                nombre = row["Nombre"]
                cantidad = row["Cantidad"]
                precio = row["Precio"]
                agregar_producto(nombre, cantidad, precio)  # Se usa la función de la BD

            QMessageBox.information(self, "Éxito", "Productos importados correctamente.")
            self.cargar_stock()  # Actualizar la tabla de stock

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al importar el archivo: {str(e)}")