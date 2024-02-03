from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic
import pathlib
from PyQt5 import QtCore

from models.category_model import CategoryModel

class CategoryWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._category = CategoryModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/categoria.ui", self)

    def load_categories(self):
        categories=self._category.get_category()
        self.tableWidget.setRowCount(len(categories))
        for i, categories in enumerate(categories):
            id_categoria,nombre_categoria,nombre_juego= categories
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(id_categoria)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(nombre_categoria)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(nombre_juego)))