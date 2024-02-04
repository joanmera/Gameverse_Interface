from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic
import pathlib
from PyQt5 import QtCore

from models.category_model import CategoryModel
from controllers.category_form import CategoryForm

class CategoryWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._category = CategoryModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/categoria.ui", self)
        self._new_category = CategoryForm()
        self.load_categories()
        self.newCategoryAction.triggered.connect(lambda: self._new_category.show())
        self._new_category.category_saved.connect(self.load_categories)

    def load_categories(self):
        categories=self._category.get_category()
        self.tableWidget.setRowCount(len(categories))
        for i, categories in enumerate(categories):
            id_categoria,nombre_categoria= categories
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(id_categoria)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(nombre_categoria)))