from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic
import pathlib
from models.purchase_model import PurchaseModel
from controllers.purchase_form import PurchaseForm

class PurchaseWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._purchase_model = PurchaseModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/compras.ui", self)
        self._new_purchase = PurchaseForm()
        self.load_purchase()
        self.actionNueva_compra.triggered.connect(lambda: self.load_product())

    def load_purchase(self):
        purchase_list = self._purchase_model.get_purchase()
        self.purchaseTable.setRowCount(len(purchase_list))
        for i, compra in enumerate(purchase_list):
            id_orden, ciudad, fecha_orden, precio_total, nombre_cliente, nombre_juego, nombre_categoria = compra
            self.purchaseTable.setItem(i, 0, QTableWidgetItem(str(id_orden)))
            self.purchaseTable.setItem(i, 1, QTableWidgetItem(str(fecha_orden)))
            self.purchaseTable.setItem(i, 2, QTableWidgetItem(str(precio_total)))
            self.purchaseTable.setItem(i, 3, QTableWidgetItem(str(nombre_cliente)))
            self.purchaseTable.setItem(i, 4, QTableWidgetItem(str(nombre_juego)))
            self.purchaseTable.setItem(i, 5, QTableWidgetItem(str(nombre_categoria)))

    def load_product(self):
        self._new_purchase.show()
