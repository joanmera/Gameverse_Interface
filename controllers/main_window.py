from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton
from PyQt5 import uic
import pathlib
from PyQt5 import QtCore
from controllers.client_form import ClientForm

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/MainWindow.ui", self)
        self.clientes_window = ClientForm()
        self.clientButton.clicked.connect(self.abrir_ventana_clientes)
        self.setGeometry(0, 0, 600, 600)

    def abrir_ventana_clientes(self):
        # Muestra la ventana de clientes usando la instancia existente
        self.clientes_window.show()


