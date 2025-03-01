from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QLineEdit, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QLabel
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
        self.setGeometry(200, 200, 800, 500)  # Aumentar el tamaño de la ventana

        layout = QVBoxLayout()

        # 🔹 Título
        self.label = QLabel("Gestión de Stock")
        layout.addWidget(self.label)

        # 🔹 Campo de búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Buscar producto...")
        layout.addWidget(self.campo_busqueda)
        self.campo_busqueda.textChanged.connect(self.filtrar_productos)  # 🔍 Filtrar productos en tiempo real

        # 🔹 Tabla de productos
        self.tabla_stock = QTableWidget()
        self.tabla_stock.setColumnCount(4)
        self.tabla_stock.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Precio"])
        self.tabla_stock.setSortingEnabled(True)  # Habilita la ordenación de columnas

        # 🔹 Ajuste automático de columnas y filas
        self.tabla_stock.horizontalHeader().setStretchLastSection(True)
        self.tabla_stock.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_stock.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.tabla_stock)

        # 🔹 Estilo tipo Excel
        self.tabla_stock.setStyleSheet("""
            QTableWidget {
                border: 1px solid gray;
                gridline-color: gray;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                padding: 4px;
            }
            QTableWidget::item {
                padding: 4px;
            }
        """)

        # 🔹 Botones de acciones organizados horizontalmente
        botones_layout = QHBoxLayout()
        self.btn_actualizar = QPushButton("Actualizar Stock")
        self.btn_agregar = QPushButton("Agregar Producto")
        self.btn_editar = QPushButton("Editar Producto")
        self.btn_eliminar = QPushButton("Eliminar Producto")
        self.btn_importar = QPushButton("Importar desde Excel")

        for btn in [self.btn_actualizar, self.btn_agregar, self.btn_editar, self.btn_eliminar, self.btn_importar]:
            btn.setFixedSize(200, 40)  # Establecer tamaño uniforme
            botones_layout.addWidget(btn)

        layout.addLayout(botones_layout)  # Agregar botones al layout principal

        # 🔹 Conectar botones a sus funciones
        self.btn_actualizar.clicked.connect(self.cargar_stock)
        self.btn_agregar.clicked.connect(self.agregar_producto)
        self.btn_editar.clicked.connect(self.editar_producto)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)
        self.btn_importar.clicked.connect(self.importar_desde_excel)

        self.setLayout(layout)
        self.cargar_stock()  # Cargar productos al abrir la ventana

    def cargar_stock(self):
        """Carga los productos en la tabla desde la base de datos."""
        try:
            productos = obtener_productos() or []  # Asegurar que no sea None

            self.tabla_stock.setRowCount(len(productos))
            for i, producto in enumerate(productos):
                for j, dato in enumerate(producto):
                    self.tabla_stock.setItem(i, j, QTableWidgetItem(str(dato)))

        except Exception as e:
            logging.error(f"❌ Error al cargar stock: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo cargar el stock: {e}")

    def filtrar_productos(self):
        """Filtra los productos en la tabla según el texto ingresado."""
        texto = self.campo_busqueda.text().lower()
        for fila in range(self.tabla_stock.rowCount()):
            visible = any(texto in self.tabla_stock.item(fila, col).text().lower() if self.tabla_stock.item(fila, col) else False
                          for col in range(self.tabla_stock.columnCount()))
            self.tabla_stock.setRowHidden(fila, not visible)

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
        """Permite importar productos desde un archivo Excel."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Archivos Excel (*.xlsx *.csv);;Todos los archivos (*)", options=options)

        if not file_path:
            return  # Si el usuario cancela, no hacer nada

        try:
            # 📌 Detectar si es CSV o Excel
            df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)

            # 📌 Verificar que el archivo tenga las columnas necesarias
            columnas_requeridas = {"Nombre", "Cantidad", "Precio"}
            if not columnas_requeridas.issubset(df.columns):
                QMessageBox.warning(self, "Error", "El archivo no tiene las columnas requeridas: Nombre, Cantidad, Precio")
                return

            # 📌 Insertar productos en la base de datos
            for _, row in df.iterrows():
                agregar_producto(row["Nombre"], row["Cantidad"], row["Precio"])

            QMessageBox.information(self, "Éxito", "Productos importados correctamente.")
            self.cargar_stock()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema al importar el archivo: {str(e)}")
