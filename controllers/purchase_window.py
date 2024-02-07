from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,QCheckBox
from PyQt5 import uic
import pathlib
from PyQt5 import QtCore

from models.purchase_model import PurchaseModel

class PurchaseWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._purchase_model = PurchaseModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/compras.ui", self)
        self.load_purchases()

    def load_purchases(self):
        purchases = self._purchase_model.get_purchase()
        self.purchaseTable.setRowCount(len(purchases))
        for i, purchases in enumerate(purchases):
            id_orden,nombre_juego,nombre_categoria= purchases
            self.purchaseTable.setItem(i, 1, QTableWidgetItem(str(id_orden)))
            self.purchaseTable.setItem(i, 2, QTableWidgetItem(str(nombre_juego)))
            self.purchaseTable.setItem(i, 3, QTableWidgetItem(str(nombre_categoria)))

            check_button= QCheckBox ()
            #check_button.clicked.connect(self.select_purchase)
            check_button.setProperty("row",i)
            self.purchaseTable.setCellWidget(i,0,check_button)

    def closeEvent(self, ev) -> None:
        self._purchase_model.close()
        return super().closeEvent(ev)