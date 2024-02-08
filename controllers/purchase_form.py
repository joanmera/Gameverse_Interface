from PyQt5.QtWidgets import QWidget, QTableWidgetItem,QCheckBox,QPushButton
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

    def load_purchases(self):
        purchases = self._purchase_model.get_products()
        self.purchaseTable.setRowCount(len(purchases))
        for i, purchases in enumerate(purchases):
            id_orden,nombre_juego,nombre_categoria= purchases
            self.purchaseTable.setItem(i, 1, QTableWidgetItem(str(id_orden)))
            self.purchaseTable.setItem(i, 2, QTableWidgetItem(str(nombre_juego)))
            self.purchaseTable.setItem(i, 3, QTableWidgetItem(str(nombre_categoria)))

            check_button= QCheckBox ()
            check_button.setIcon(QIcon("views/check.png"))
            check_button.setStyleSheet("background-color: transparent; border: none; color: black;")
            check_button.setIconSize(QSize(25,25))
            #check_button.clicked.connect(self.select_purchase)
            check_button.setProperty("row",i)
            self.purchaseTable.setCellWidget(i,0,check_button)

            details_button= QPushButton("Detalles")
            details_button.setIcon(QIcon("views/details.png"))
            details_button.setStyleSheet("background-color: transparent; border: none; color: black;")
            details_button.setIconSize(QSize(25,25))
            #details_button.clicked.connect()
            details_button.setProperty("row",i)
            self.purchaseTable.setCellWidget(i,4,details_button)


    def closeEvent(self, ev) -> None:
        self._purchase_model.close()
        return super().closeEvent(ev)