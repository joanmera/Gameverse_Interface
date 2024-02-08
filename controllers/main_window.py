from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QIcon
import pathlib  
from PyQt5 import QtCore

from controllers.client_window import ClientWindow
from controllers.category_window import CategoryWindow
from controllers.videogame_window import VideogameWindow
from controllers.purchase_window import PurchaseWindow

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/MainWindow.ui", self)
        pixmap = QPixmap('logo3.png')
        pixmap = pixmap.scaledToWidth(310)
        pixmap = pixmap.scaledToHeight(210)

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(90, 20, 471, 251)

        


        self.clientes_window = ClientWindow()
        self.categorias_window = CategoryWindow()
        self.juego_window = VideogameWindow()
        self.compras_window = PurchaseWindow()
        self.clientButton.clicked.connect(self.abrir_ventana_clientes)
        self.categoryButton.clicked.connect(self.abrir_ventana_categorias)
        self.gameButton.clicked.connect(self.abrir_ventana_juego)
        self.purchaseButton.clicked.connect(self.abrir_ventana_compras)
        
    def abrir_ventana_clientes(self):
        # Muestra la ventana de clientes usando la instancia existente
        self.clientes_window.load_client()  # llamar a load_client
        self.clientes_window.show()
        self.close()

    def abrir_ventana_categorias(self):
        self.categorias_window.load_categories()
        self.categorias_window.show()

    def abrir_ventana_juego(self):
        self.juego_window.load_game()
        self.juego_window.show()

    def abrir_ventana_compras(self):
        self.compras_window.load_purchases()
        self.compras_window.show()

   


