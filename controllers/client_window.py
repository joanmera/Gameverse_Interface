from psycopg2 import Error
import pathlib
from PyQt5 import uic   
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from models.client_model import ClientModel
from controllers.client_form import ClientForm

class ClientWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._client_model = ClientModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/clientes.ui", self)
        self._new_client = ClientForm()
        self.load_client()
        self.newClientAction.triggered.connect(lambda: self.create_client())
        self._new_client.client_saved.connect(self.load_client)
    
        
    def load_client(self):
        client_list = self._client_model.get_clients()
        self.clientTable.setRowCount(len(client_list))
        for i, cliente in enumerate(client_list):
            id_cliente, nombre_cliente, cedula, edad, genero, telefono = cliente
            self.clientTable.setItem(i, 0, QTableWidgetItem(str(id_cliente)))
            self.clientTable.setItem(i, 1, QTableWidgetItem(str(nombre_cliente)))
            self.clientTable.setItem(i, 2, QTableWidgetItem(str(cedula)))
            self.clientTable.setItem(i, 3, QTableWidgetItem(str(edad)))
            self.clientTable.setItem(i, 4, QTableWidgetItem(str(genero)))
            self.clientTable.setItem(i, 5, QTableWidgetItem(str(telefono)))
            self.clientTable.item(i, 0).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)


            edit_button = QPushButton ("Editar")
            edit_button.setIcon(QIcon("views/edit.png"))
            edit_button.setStyleSheet("background-color: transparent; border: none; color: black;")
            edit_button.setIconSize(QSize(25,25))
            edit_button.clicked.connect(self.edit_client)
            edit_button.setProperty("row", i)
            self.clientTable.setCellWidget(i, 6, edit_button)

            delete_button = QPushButton("Eliminar")
            delete_button.setIcon(QIcon("views/delete.png"))
            delete_button.setStyleSheet("background-color: transparent; border: none; color: black;")
            delete_button.setIconSize(QSize(25,25))
            delete_button.clicked.connect(self.delete_client)
            delete_button.setProperty("row", i)
            self.clientTable.setCellWidget(i, 7, delete_button)


    def edit_client(self):
        try:
            sender = self.sender()
            row = sender.property("row")
            client_id = self.clientTable.item(row, 0).text()
            
            self._new_client.load_client_data(client_id)
            self._new_client.show()
        except Exception as e:
            print("Error en la carga de datos del cliente:", e)

    def delete_client(self):
        sender = self.sender()
        row = sender.property("row")
        client_id = self.clientTable.item(row, 0).text()

        reply = QMessageBox.question(self, 'Eliminar Cliente', '¿Estás seguro de que deseas eliminar este cliente?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            
            success = self._client_model.delete_client(client_id)
            if success:
                QMessageBox.information(self, 'Éxito', 'Cliente eliminado correctamente.')
                self.load_client()
            else:
                QMessageBox.warning(self, 'Error', 'Error al eliminar el cliente.')

    def create_client(self):
        self._new_client.reset_form()
        self._new_client.show()

    def closeEvent(self, ev) -> None:
        self._client_model.close()
        return super().closeEvent(ev)

    
    


    