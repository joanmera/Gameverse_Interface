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
        self.id_categoria = None

    def save_category(self):
        if self.id_categoria:
            self._categoryHandler.update_category(
                self.id_categoria,
                self.category_lineEdit.text(),
            )
        else: 
            self._categoryHandler.create_category(
                self.category_lineEdit.text(),
            )

        self.category_saved.emit()
        self.close()

    def load_category_data(self,id_categoria):
        self.id_categoria = id_categoria
        category_data = self._categoryHandler.get_category_by_id(id_categoria)
        if category_data:
            self.category_lineEdit.setText(category_data[1])

    def reset_form(self):
        self.category_lineEdit.setText("")
        self.id_categoria = None