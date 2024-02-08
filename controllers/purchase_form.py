from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QCheckBox, QPushButton, QMessageBox, QComboBox
from PyQt5 import uic
import pathlib
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from models.purchase_model import PurchaseModel

class PurchaseForm(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._purchase_model = PurchaseModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/compras_form.ui", self)
        self.load_purchases()
        
        # Asigna la función save_purchase a la señal clicked del botón de guardar
        self.saveButton.clicked.connect(self.save_purchase)

        # Llama al método para cargar los clientes
        self.load_clients()

    def load_clients(self):
        clients = self._purchase_model.get_clients()
        # Limpia cualquier contenido anterior en el QComboBox
        self.clientComboBox.clear()
        # Agrega los clientes al QComboBox
        for client in clients:
            id_cliente, nombre_cliente = client
            self.clientComboBox.addItem(f"{nombre_cliente} ({id_cliente})", id_cliente)

    def save_purchase(self):
        try:
            id_cliente = self.clientComboBox.currentData()  # Obtén el ID del cliente seleccionado en el QComboBox

            for row in range(self.purchaseTable.rowCount()):
                check_box = self.purchaseTable.cellWidget(row, 0)  # Suponiendo que la casilla de verificación está en la columna 0
                if check_box.isChecked():
                    id_orden = int(self.purchaseTable.item(row, 1).text())  # Suponiendo que la columna 1 tiene el ID de la orden
                    nombre_juego = self.purchaseTable.item(row, 2).text()  # Suponiendo que la columna 2 tiene el nombre del juego
                    nombre_categoria = self.purchaseTable.item(row, 3).text()  # Suponiendo que la columna 3 tiene el nombre de la categoría

                    # Llama a tu función para crear la compra
                    self._purchase_model.create_purchase(id_cliente, id_orden, nombre_juego, nombre_categoria)


            QMessageBox.information(self, "Compra Exitosa", "La compra se ha registrado correctamente.")
            self.close()

        except Exception as e:
            print("Error en la transacción de la base de datos:", e)
            # Manejo de errores


    def load_purchases(self):
        purchases = self._purchase_model.get_products()
        self.purchaseTable.setRowCount(len(purchases))
        for i, purchase in enumerate(purchases):
            id_juego, nombre_juego, nombre_categoria = purchase
            self.purchaseTable.setItem(i, 1, QTableWidgetItem(str(id_juego)))
            self.purchaseTable.setItem(i, 2, QTableWidgetItem(str(nombre_juego)))
            self.purchaseTable.setItem(i, 3, QTableWidgetItem(str(nombre_categoria)))

            check_button = QCheckBox()
            check_button.setIcon(QIcon("views/check.png"))
            check_button.setStyleSheet("background-color: transparent; border: none; color: black;")
            check_button.setIconSize(QSize(25, 25))
            check_button.setProperty("row", i)
            self.purchaseTable.setCellWidget(i, 0, check_button)

            details_button = QPushButton("Detalles")
            details_button.setIcon(QIcon("views/details.png"))
            details_button.setStyleSheet("background-color: transparent; border: none; color: black;")
            details_button.setIconSize(QSize(25, 25))
            details_button.setProperty("row", i)
            self.purchaseTable.setCellWidget(i, 4, details_button)

    def closeEvent(self, ev) -> None:
        self._purchase_model.close()
        return super().closeEvent(ev)
