from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,QPushButton,QMessageBox
from PyQt5 import uic
import pathlib
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from models.category_model import CategoryModel
from controllers.category_form import CategoryForm

class CategoryWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._category_model = CategoryModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/categoria.ui", self)
        self._new_category = CategoryForm()
        self.load_categories()
        self.newCategoryAction.triggered.connect(lambda: self.create_category())
        self._new_category.category_saved.connect(self.load_categories)

    def load_categories(self):
        categories=self._category_model.get_category()
        self.categoryTable.setRowCount(len(categories))
        for i, categories in enumerate(categories):
            id_categoria,nombre_categoria= categories
            self.categoryTable.setItem(i, 0, QTableWidgetItem(str(id_categoria)))
            self.categoryTable.setItem(i, 1, QTableWidgetItem(str(nombre_categoria)))

            edit_button= QPushButton ("Editar")
            edit_button.setIcon(QIcon("views/edit.png"))
            edit_button.setStyleSheet("background-color: transparent; border: none; color: black;")
            edit_button.setIconSize(QSize(25,25))
            edit_button.clicked.connect(self.edit_category)
            edit_button.setProperty("row",i)
            self.categoryTable.setCellWidget(i,2,edit_button)

            delete_button = QPushButton("Eliminar")
            delete_button.setIcon(QIcon("views/delete.png"))
            delete_button.setStyleSheet("background-color: transparent; border: none; color: black;")
            delete_button.setIconSize(QSize(25,25))
            delete_button.clicked.connect(self.delete_category)
            delete_button.setProperty("row", i)
            self.categoryTable.setCellWidget(i, 3, delete_button)

    def edit_category(self):
        sender= self.sender()
        row = sender.property("row")
        id_categoria= self.categoryTable.item(row,0).text()
        self._new_category.load_category_data(id_categoria)
        self._new_category.show()

    def delete_category(self):
        sender = self.sender()
        row = sender.property("row")
        category_id = self.categoryTable.item(row, 0).text()

        reply = QMessageBox.question(self, 'Eliminar Categoria', '¿Estás seguro de que deseas eliminar esta categoria?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            
            success = self._category_model.delete_category(category_id)
            if success:
                QMessageBox.information(self, 'Éxito', 'Categoria eliminada correctamente.')
                self.load_categories()
            else:
                QMessageBox.warning(self, 'Error', 'Error al eliminar categoria.')

    def create_category(self):
        self._new_category.reset_form()
        self._new_category.show()

    def closeEvent(self, ev) -> None:
        self._category_model.close()
        return super().closeEvent(ev)
