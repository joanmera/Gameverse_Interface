import pathlib
from psycopg2 import Error
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic   
from models.videogame_model import VideogameModel

class VideogameForm(QWidget):
    game_saved = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._gameHandler = VideogameModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/videojuego_form.ui", self)

        # Asegúrate de que el nombre del QComboBox sea el mismo que especificaste en el formulario
        self.categoryComboBox.addItems(self._gameHandler.get_categories())  # Método que obtiene las categorías desde tu modelo
        self.saveButton.clicked.connect(lambda: self.save_game())
        self.cancelButton.clicked.connect(lambda: self.close())
        self.game_id = None

    def save_game(self):
        try:
            if self.game_id:
                self._gameHandler.update_game (
                    self.game_id,
                    self.name_lineEdit.text(),
                    self.categoryComboBox.currentText(),  # Obtén el texto seleccionado en el QComboBox
                    self.price_lineEdit.text(),
                    self.developer_lineEdit.text(),
                    self.date_lineEdit.text(),
                    self.score_lineEdit.text()
                )
            else:
                self._gameHandler.create_game(
                    self.name_lineEdit.text(),
                    self.categoryComboBox.currentText(),  # Obtén el texto seleccionado en el QComboBox
                    self.price_lineEdit.text(),
                    self.developer_lineEdit.text(),
                    self.date_lineEdit.text(),
                    self.score_lineEdit.text()
                )

            self.game_saved.emit()
            self.close()

        except Exception as e:
            print("Error en la transacción de la base de datos:", e)
            error_box = QMessageBox()
            error_box.setStyleSheet("color: white") 
            QMessageBox.critical(self, "Error", "Ha ocurrido un error en la creación del juego. Revisa que los datos sean ingresados correctamente.")
            self._gameHandler.rollback()


    def load_game_data(self, game_id):
        self.game_id = game_id
        try:
            game_data = self._gameHandler.get_game_by_id(game_id)
            if game_data:
                self.name_lineEdit.setText(str(game_data[1]))

                # Actualizado para cargar la categoría en el QComboBox
                category_index = self.categoryComboBox.findText(str(game_data[2]))
                if category_index != -1:
                    self.categoryComboBox.setCurrentIndex(category_index)

                self.price_lineEdit.setText(str(game_data[3]))
                self.developer_lineEdit.setText(str(game_data[4]))
                self.date_lineEdit.setText(str(game_data[5]))
                self.score_lineEdit.setText(str(game_data[6]))

        except Error as e:
            print("Error en la transacción de la base de datos:", e)
            self.invalid_information.setText("Ingresa una identificación válida")
            self.invalid_information_2.setText("Ingresa una edad válida")

    def reset_form(self):
        self.name_lineEdit.setText("")
        
        # Restablecer el QComboBox a un espacio en blanco
        self.categoryComboBox.setCurrentIndex(-1)

        self.price_lineEdit.setText("")
        self.developer_lineEdit.setText("")
        self.date_lineEdit.setText("")
        self.score_lineEdit.setText("")
        self.game_id = None
