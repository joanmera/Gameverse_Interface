from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QCheckBox, QPushButton, QMessageBox, QComboBox
from PyQt5 import uic
import pathlib
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize,Qt, pyqtSignal
from models.purchase_model import PurchaseModel

class PurchaseForm(QWidget):
    purchase_saved = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self._purchase_model = PurchaseModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/compras_form.ui", self)
        self.load_purchases()
        

        
        # Asigna la función save_purchase a la señal clicked del botón de guardar
        self.saveButton.clicked.connect(self.save_purchase)
        self.cancelButton.clicked.connect(self.close)

        # Llama al método para cargar los clientes
        self.load_clients()

    def load_clients(self):
        clients = self._purchase_model.get_clients()
        # Limpia cualquier contenido anterior en el QComboBox
        self.clientComboBox.clear()
        # Agrega los clientes al QComboBox
        for client in clients:
            id_cliente, nombre_cliente = client
            self.clientComboBox.addItem(f"{nombre_cliente}", id_cliente)

    def save_purchase(self):
        selected_row = self.purchaseTable.currentRow()

        if selected_row != -1:
            id_cliente = self.clientComboBox.currentData()
            date = self.dateTimeEdit.dateTime().toPyDateTime()

            # Modificación: Obtener la lista de juegos seleccionados y el precio total
            id_juegos_seleccionados, precio_total = self.get_selected_games()

            if id_juegos_seleccionados:
                # Llamar a la función para guardar la compra en tu modelo
                self._purchase_model.create_purchase(id_cliente, date, id_juegos_seleccionados, precio_total)

                # Emitir señal de que la compra ha sido guardada
                self.purchase_saved.emit()

                # Cerrar la ventana
                self.close()
            else:
                # Manejar el caso en que no se seleccionó ningún juego
                print("No se seleccionó ningún juego.")

        else:
            # Manejar el caso en que no se seleccionó ninguna fila
            print("No se seleccionó ninguna fila.")



    def get_selected_games(self):
        selected_games = []
        total_price = 0.0  # Inicializa el precio total
        
        for row in range(self.purchaseTable.rowCount()):
            checkbox = self.purchaseTable.cellWidget(row, 0)
            if checkbox.isChecked():
                id_juego_item = self.purchaseTable.item(row, 1)
                if id_juego_item is not None:
                    id_juego = int(id_juego_item.text())
                    price = self._purchase_model.get_total(id_juego)
                    total_price += price  # Suma el precio de cada juego al precio total
                    selected_games.append(id_juego)

        # Muestra el precio total en tu etiqueta (si es necesario)
        total_str = "{:.2f}".format(total_price)
        self.label_4.setText(total_str)

        return selected_games, total_price  # Retorna la lista de juegos seleccionados y el precio total


    def load_purchases(self):
        purchases = self._purchase_model.get_products()
        self.purchaseTable.setRowCount(len(purchases))
        for i, purchase in enumerate(purchases):
            id_juego,nombre_juego, nombre_categoria = purchase
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
            self.purchaseTable.setCellWidget(i, 5, details_button)
