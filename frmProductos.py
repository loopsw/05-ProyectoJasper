import sys,os
from PyQt5 import uic
from SQLGenerator import SQLGenerator
from DataBase import DataBaseConnection
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
FILE_NAME = 'frmProductos.ui'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_FORM = os.path.join(BASE_DIR,'FormulariosUI',FILE_NAME)

class FrmProductos(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        uic.loadUi(PATH_FORM,self)
        self.sql = SQLGenerator('articulos')
        self.myDB = DataBaseConnection()
        self.txtCodigo.editingFinished.connect(self.recuperarProducto)
        self.btnLimpiar.clicked.connect(self.limpiarFormulario)
        self.btnGuardar.clicked.connect(self.guardar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnSalir.clicked.connect(self.salir)

    def recuperarProducto(self):
        # Recuperar producto
        codigo = self.txtCodigo.text()
        sqlQuery = self.sql.generateFind('codigo',codigo)
        result = self.myDB.executeQuery(sqlQuery)
        if len(result) == 0:    # No tengo el registro en la BBDD
            self.limpiarFormulario()
            self.txtCodigo.setText(codigo)           
            return

        # Poner los datos en el formularios
        print(result)
        
        result = result[0] # solo el primer registro
        
        self.txtNombre.setText(result[1])
        self.spinBoxPrecio.setValue(result[2])
        self.spinBoxStock.setValue(result[3])
        self.spinBoxStockMinimo.setValue(result[4])        
        self.spinBoxPVP.setValue(result[5])        
        self.txtObservaciones.setText(result[6])        
        self.comboTipoIVA.setCurrentIndex(result[7])
        self.chbDescatalogado.setChecked(result[8])
        """
        self.txtDireccion.setText(result[3])
        self.txtPoblacion.setText(result[4])
        self.cmbProvincia.setCurrentText(result[5])
        self.txtCP.setText(result[6])
        self.txtTelefono.setText(result[7])
        self.txtEmail.setText(result[8])
        self.chbRecargo.setChecked(int(result[9]))
        index = self.comboTipoCliente.findData(result[10])  # busca el código tipocliente en el combobox
        #print(index)
        self.comboTipoCliente.setCurrentIndex(index)
        self.dtmFechaAlta.setDate(result[11])
        self.txtObservaciones.setText(result[12])
        self.chbTipoDocumento.setCurrentIndex(result[13])
        """

    def eliminar(self):
        # compruebo que el registro exista en la base de datos        
        codigo= self.txtCodigo.text()
        sqlQuery = self.sql.generateFind('codigo',codigo)
        result = self.myDB.executeQuery(sqlQuery)
        if len(result) == 0:
            QMessageBox.information(self,"Gestión de MiEmpresa","El producto "+codigo+" NO existe")
            return

        # Pregunto si esta de acuerdo con eliminar
        if QMessageBox.question(self,"Gestión de MiEmpresa","Esta seguro que desea eliminar? Los datos serán eliminados definitivamente") == QMessageBox.No:
                return
            
        # Elimino
        sqlQuery = self.sql.generateDelete('codigo',codigo)
        self.myDB.executeQuery(sqlQuery)
        QMessageBox.information(self,"Gestión de MiEmpresa","Cliente eliminado correctamente.")
        self.limpiarFormulario()

    def salir(self):
        self.parent().close()

    def limpiarFormulario(self):
        self.txtCodigo.clear()
        self.txtNombre.clear()
        self.spinBoxPrecio.setValue(0)
        self.spinBoxPVP.setValue(0)
        self.txtObservaciones.clear()
        self.spinBoxStock.setValue(0)
        self.spinBoxStockMinimo.setValue(0)
        self.chbDescatalogado.setChecked(False)
        self.comboTipoIVA.setCurrentIndex(-1)

    def guardar(self):
        insertData = False
        if self.__validarFormulario() == True:
            self.sql.addCampo('codigo',self.txtCodigo.text())
            self.sql.addCampo('nombre',self.txtNombre.text())
            self.sql.addCampo('precio_compra',self.spinBoxPrecio.value())
            self.sql.addCampo('pvp',self.spinBoxPVP.value())
            self.sql.addCampo('observaciones',self.txtObservaciones.toPlainText())
            self.sql.addCampo('descatalogado',int(self.chbDescatalogado.isChecked()))
            self.sql.addCampo('stock',self.spinBoxStock.value())
            self.sql.addCampo('stock_minimo',self.spinBoxStockMinimo.value())
            self.sql.addCampo('tipo_iva',self.comboTipoIVA.currentIndex())
            # Comprobar si tengo que actualizar o guardar nuevo registro
            codigo = self.txtCodigo.text()
            sqlQuery = self.sql.generateFind('codigo',codigo)
            print(sqlQuery)
            result = self.myDB.executeQuery(sqlQuery)
            if len(result) == 0:
                insertData = True

        else:
            return

        # Confirmar que va a guardar los datos
        if QMessageBox.question(self,"Gestión de MiEmpresa","Los datos se guardarán en el disco?") == QMessageBox.No:
            return

        if insertData == True:
            # Inserción nuevo registro
            sqlQuery = self.sql.generateInsert()
            if self.myDB.executeQuery(sqlQuery):
                QMessageBox.information(self, 'Gestión de MiEmpresa', 'Producto introducido correctamente.')
            else:
                QMessageBox.warning(self, 'Gestión de MiEmpresa', 'Producto NO se guardo correctamente.')
        else:
            # Actualizar datos
            sqlQuery = self.sql.generateUpdate('codigo',codigo)
            self.myDB.executeQuery(sqlQuery)
            QMessageBox.information(self, 'Gestión de MiEmpresa', 'Producto modificado correctamente.')
        self.limpiarFormulario()

    def __validarFormulario(self):
        # validar código
        if self.txtCodigo.text() == '':
            QMessageBox.information(self,"Gestión de MiEmpresa","El código no puede estar vacío")
            self.txtCodigo.setFocus()
            return False

        # validar nombre
        if self.txtNombre.text() == '':
            QMessageBox.information(self,"Gestión de MiEmpresa","El nombre no puede estar vacío")
            self.txtNombre.setFocus()
            return False

        # validar Precio
        if self.spinBoxPrecio.value() == '':
            QMessageBox.information(self,"Gestión de MiEmpresa","El precio no puede estar vacío")
            self.spinBoxPrecio.setFocus()
            return False 
        if  self.spinBoxPrecio.value() <= 0:
            QMessageBox.information(self,"Gestión de MiEmpresa","El precio de compra no puede ser cero")
            self.spinBoxPrecio.setFocus()
            return False 
        # validar PVP
        if  self.spinBoxPVP.value() <= 0:
            QMessageBox.information(self,"Gestión de MiEmpresa","El PVP no puede ser cero")
            self.spinBoxPVP.setFocus()
            return False 
        # validar Stock
        if  self.spinBoxStock.value() <= 0:
            QMessageBox.information(self,"Gestión de MiEmpresa","El Stock no puede ser cero")
            self.spinBoxStock.setFocus()
            return False
        return True  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = FrmProductos()
    myWindow.show()    
    sys.exit(app.exec_())