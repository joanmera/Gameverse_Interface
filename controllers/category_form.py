import pathlib
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic   
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton

from models.category_model import CategoryModel

class CategoryForm(QWidget):
    category_saved= pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self._categoryHandler = CategoryModel()
        mod_path= pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/categoria_form.ui",self)
        self.categorySaveButton.clicked.connect(lambda: self.save_category())
        self.categoryCancelButton.clicked.connect(lambda: self.close())
        self.client_id = None

    def save_category(self):
            self._categoryHandler.create_category(
                self.category_lineEdit.text()
            )
            self.category_saved.emit()
            self.close()