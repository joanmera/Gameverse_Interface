import pathlib
from PyQt5 import uic   
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from models.videogame_model import VideogameModel
from controllers.videogame_form import VideogameForm

class VideogameWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._game_model = VideogameModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/videojuego.ui", self)
        self._new_game = VideogameForm()
        self.load_game()
        self.newGameAction.triggered.connect(lambda: self.create_game())
        self._new_game.game_saved.connect(self.load_game)
    
        
    def load_game(self):
        game_list = self._game_model.get_videogame()
        self.gameTable.setRowCount(len(game_list))
        for i, juego in enumerate(game_list):
            id_juego, nombre_juego,categoria, precio, desarrollador, fecha_lanzamiento, puntuacion_general = juego
            self.gameTable.setItem(i, 0, QTableWidgetItem(str(id_juego)))
            self.gameTable.setItem(i, 1, QTableWidgetItem(str(nombre_juego)))
            self.gameTable.setItem(i, 2, QTableWidgetItem(str(categoria)))
            self.gameTable.setItem(i, 3, QTableWidgetItem(str(precio)))
            self.gameTable.setItem(i, 4, QTableWidgetItem(str(desarrollador)))
            self.gameTable.setItem(i, 5, QTableWidgetItem(str(fecha_lanzamiento)))
            self.gameTable.setItem(i, 6, QTableWidgetItem(str(puntuacion_general)))


            edit_button = QPushButton ("Editar")
            edit_button.setIcon(QIcon("views/edit.png"))
            edit_button.setStyleSheet("background-color: transparent; border: none; color: black;")
            edit_button.setIconSize(QSize(25,25))
            edit_button.clicked.connect(self.edit_game)
            edit_button.setProperty("row", i)
            self.gameTable.setCellWidget(i, 7, edit_button)

            delete_button = QPushButton("Eliminar")
            delete_button.setIcon(QIcon("views/delete.png"))
            delete_button.setStyleSheet("background-color: transparent; border: none; color: black;")
            delete_button.setIconSize(QSize(25,25))
            delete_button.clicked.connect(self.delete_game)
            delete_button.setProperty("row", i)
            self.gameTable.setCellWidget(i, 8, delete_button)


    def edit_game(self):
        sender = self.sender()
        row = sender.property("row")
        game_id = self.gameTable.item(row, 0).text()
        self._new_game.load_game_data(game_id)
        self._new_game.show()
    
    def delete_game(self):
        sender = self.sender()
        row = sender.property("row")
        game_id = self.gameTable.item(row, 0).text()

        reply = QMessageBox.question(self, 'Eliminar Videojuego', '¿Estás seguro de que deseas eliminar este Videojuego?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            
            success = self._game_model.delete_game(game_id)
            if success:
                QMessageBox.information(self, 'Éxito', 'Videojuego eliminado correctamente.')
                self.load_game()
            else:
                QMessageBox.warning(self, 'Error', 'Error al eliminar el Videojuego.')

    def create_game(self):
        self._new_game.reset_form()
        self._new_game.show()

    def closeEvent(self, ev) -> None:
        self._game_model.close()
        return super().closeEvent(ev)
