import os
import sys
from DataBase import DataBaseConnection
from SQLGenerator import SQLGenerator
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = 'frmTipoClientes.ui'
PATH_FORM = os.path.join(BASE_DIR,'FormulariosUI',FILE_NAME)

class FrmTipoClientes(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        uic.loadUi(PATH_FORM,self)
        self.myDB = DataBaseConnection()    # Instancia de conexión con la base de datos
        self.sql = SQLGenerator('tipoClientes') # generador de SQL de la tabla tipoClientes
        self.txtCodigo.setFocus()   # Pongo el foco al primer campo
        self.btnGuardar.clicked.connect(self.guardar)
        self.btnLimpiar.clicked.connect(self.limpiar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.txtCodigo.editingFinished.connect(self.recuperar)
        self.btnSalir.clicked.connect(self.salir)

    def salir(self):
        self.parent().close()

    def recuperar(self):
        # validar código
        if self.txtCodigo.text() == '':
            QMessageBox.information(self,"Gestión de MiEmpresa","El código del tipo de cliente no puede estar vacío")
            self.txtCodigo.setFocus()
            return 
        # consultar si existe registro con ese código
        codigo = self.txtCodigo.text()    
        sqlQuery = self.sql.generateFind('codigo',codigo)
        result = self.myDB.executeQuery(sqlQuery)
        if len(result) == 0:
            self.txtNombre.setText('')
            return
        self.txtNombre.setText(result[0][1])

    def limpiar(self):
        self.txtCodigo.clear()
        self.txtNombre.clear()
        self.txtCodigo.setFocus()

    def guardar(self):
        insertData = False     # si es True debe insertar nuevo registro, si es False actualiza registro
        if self.__validarFormulario() == True:
            codigo = self.txtCodigo.text();
            nombre = self.txtNombre.text();            
            self.sql.addCampo('codigo',codigo)
            self.sql.addCampo('tipo',nombre)
            sqlQuery = self.sql.generateFind('codigo',codigo)
            result = self.myDB.executeQuery(sqlQuery)
            if not result: # lista vacía -> inserto los datos
                insertData = True
            else:   # lista no esta vacia -> update
                insertData = False    
        else:
            return

        # Confirmar que va a guardar los datos
        if QMessageBox.question(self,"Gestión de MiEmpresa","Los datos se guardarán en el disco?") == QMessageBox.No:
            return
        
        if insertData == True:        
            sqlQuery = self.sql.generateInsert()
            self.myDB.executeQuery(sqlQuery)
        else:   # Update
            sqlQuery = self.sql.generateUpdate("codigo",codigo)
            self.myDB.executeQuery(sqlQuery) 
        self.limpiar()
        return

    def eliminar(self):
        if self.__validarFormulario() == False:
            return        

        # compruebo que el registro exista en la base de datos        
        codigo = self.txtCodigo.text()
        sqlQuery = self.sql.generateFind('codigo',codigo)
        result = self.myDB.executeQuery(sqlQuery)
        if len(result) == 0:
            QMessageBox.information(self,"Gestión de MiEmpresa","El tipo de cliente no existe")
            return

        if QMessageBox.question(self,"Gestión de MiEmpresa","Los datos serán eliminados?") == QMessageBox.No:
                return

        # Comprobar que no existan clientes asignados
        sqlGen = SQLGenerator('clientes')
        sqlQuery = sqlGen.generateFind('tipoCliente',codigo)
        result = self.myDB.executeQuery(sqlQuery)
        if result:
            QMessageBox.information(self,"Gestión de MiEmpresa","No se puede eliminar el tipo de cliente porque tiene clientes aceptados. Elimínelos previamente")
            return
        
        # Elimino
        sqlQuery = self.sql.generateDelete('codigo',codigo)
        self.myDB.executeQuery(sqlQuery)
        self.limpiar()

    def __validarFormulario(self):
        # validar código
        if self.txtCodigo.text() == '':
            QMessageBox.information(self,"Gestión de MiEmpresa","El código del tipo de cliente no puede estar vacío")
            self.txtCodigo.setFocus()
            return False
        if self.txtNombre.text() == '':
            QMessageBox.information(self,"Gestión de MiEmpresa","El nombre no puede estar vacío")
            self.txtCodigo.setFocus()
            return False
        return True    

if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindows = FrmTipoClientes()
    myWindows.show()
    app.exec_()