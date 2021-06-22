import os
import re # expresiones regulares
import sys
import ctypes
import random


from pyreportjasper import PyReportJasper
from pyreportjasper.report import Report
import webbrowser
from DataBase import DataBaseConnection
from SQLGenerator import SQLGenerator
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = 'frmClientes2.ui'
PATH_FORM = os.path.join(BASE_DIR,'FormulariosUI',FILE_NAME)

class FrmClientes(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        uic.loadUi(PATH_FORM,self)
        self.myDB = DataBaseConnection()    # Conexión a la BBDD
        self.sql = SQLGenerator('clientes') # Genera sql de la tabla clientes
        self.__cargarEstadoInicial()

    def __cargarEstadoInicial(self):
        self.txtDNI.setFocus()
        self.__cargarTipoClientes()         # Carga el combobox con los tipos de clientes        
        self.txtDNI.editingFinished.connect(self.recuperarCliente)
        self.btnGuardar.clicked.connect(self.guardarCliente)        
        self.btnEliminar.clicked.connect(self.eliminarCliente)
        self.btnLimpiar.clicked.connect(self.limpiarFormulario)
        self.btnSalir.clicked.connect(self.salirFormularioCliente)
        self.btnImprimir.clicked.connect(self.generarReporte)

    def processing(self):
        REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reportesClientes')
        input_file = os.path.join(REPORTS_DIR, 'csv.jasper')
        print(input_file)
        output_file = os.path.join(REPORTS_DIR, 'csv')
        pyreportjasper = PyReportJasper()
        pyreportjasper.config(
            input_file,
            output_file,
            output_formats=["pdf", "rtf"]
            )
        pyreportjasper.process_report()

    def verPDF(self,fileSave):
        outputFile = os.path.join(BASE_DIR,'reportesClientes',fileSave)
        webbrowser.open_new(r'file://' + outputFile )  
        #os.startfile (outputFile) 
        #os.system (outputFile) 
        #return

    def generarReporte(self):
        #fileReport = 'reporteClientes.jrxml'
        fileReport = 'Cliente.jrxml'
        filename = 'temp.pdf'
        inputFile = os.path.join(BASE_DIR,'reportesClientes',fileReport)
        outputFile = os.path.join(BASE_DIR,'reportesClientes',filename)
        pathConnector = os.path.join(BASE_DIR,'mysql-connector-java-8.0.25.jar')
        conn = {                                             # datos de conexion a base de datos
            'driver': 'mariadb',
            'username': 'userpoo',
            'password': '123Admin',
            'host': 'localhost',
            'database': 'poo',
            'port': '3306',
            'jdbc_driver': 'org.mariadb.jdbc.Driver',
            #'jdbc_dir': BASE_DIR     # conector jdbc copiado a la carpeta del proyecto
        }

        pyreportjasper = PyReportJasper()
        #pyreportjasper.compile(write_jasper=True) # compilo el reporte habria que quitarlo si no va
        
        pyreportjasper.config(
                            inputFile,
                            outputFile,
                            output_formats=["pdf"],
                            db_connection={
                                            'driver': 'mysql',
                                            'username': 'userpoo',
                                            'password': '123Admin',
                                            'host': 'localhost',
                                            'database': 'poo',
                                            'port': '3306',
                                            'jdbc_driver': 'com.mysql.cj.jdbc.Driver',
                                            #'jdbc_dir' : pathConnector
                                        },
                            
                            parameters = {'dni':self.txtDNI.text(),'imageDir':os.path.join(BASE_DIR,'reportesClientes/')},
                            resource=os.path.join(BASE_DIR,'reportesClientes/')
                            )

        # genera el informe
        #pyreportjasper.process_report()
        
        
        report = Report(pyreportjasper.config, pyreportjasper.config.input)
        report.fill()
        report.export_pdf()
        report.export_rtf()
        del report
        del pyreportjasper
        #sys.exit(pyreportjasper)
        #report.close()
        #pdf = report.get_output_stream('.pdf')
        # Save locally
        #fw = open(outputFile,'w')
        #fw.write(pdf)
        # generate hash 
        hash = str(random.getrandbits(32))
        fileSave = os.path.join(BASE_DIR,'reportesClientes','reporteClientes_'+hash+'.pdf')
        import shutil
        shutil.copy(outputFile, fileSave)
        fw = open(outputFile,'r')
        fw.flush()
        fw.close()
        self.verPDF(fileSave)
        

        return
        #import psutil

        #for p in psutil.process_iter():
        #    print(p, p.name(), p.pid)
        #os.remove(outputFile)
        #webbrowser.open_new(outputFile)


    def recuperarCliente(self):
        # Comprobar si tengo que actualizar o guardar nuevo registro
        DNI = self.txtDNI.text()
        sqlQuery = self.sql.generateFind('nif',DNI)
        result = self.myDB.executeQuery(sqlQuery)
        if len(result) == 0:    # No tengo el registro en la BBDD
            self.limpiarFormulario()
            self.txtDNI.setText(DNI)           
            return

        # Poner los datos en el formularios
        result = result[0] # solo el primer registro
        self.txtNombre.setText(result[2])
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
    
    def guardarCliente(self):
        insertData = False
        if self.__validarFormulario() == True:
            # Copiar los datos del ui al generador de SQL
            self.sql.addCampo('nif',self.txtDNI.text())
            self.sql.addCampo('nombre',self.txtNombre.text())
            self.sql.addCampo('direccion',self.txtDireccion.text())
            self.sql.addCampo('poblacion',self.txtPoblacion.text())
            self.sql.addCampo('provincia',self.cmbProvincia.currentText())
            self.sql.addCampo('cp',self.txtCP.text())
            self.sql.addCampo('telefono',self.txtTelefono.text())
            self.sql.addCampo('email',self.txtEmail.text())
            self.sql.addCampo('recargo',int(self.chbRecargo.isChecked()))
            index = self.comboTipoCliente.currentIndex()
            codigoTipoCliente = self.comboTipoCliente.itemData(index)
            self.sql.addCampo('tipoCliente',codigoTipoCliente)
            self.sql.addCampo('fechaAlta',self.dtmFechaAlta.date().toString('yyyy-MM-dd'))
            self.sql.addCampo('observaciones',self.txtObservaciones.toPlainText())  
            self.sql.addCampo('tipoDocumento',self.chbTipoDocumento.currentIndex())              

            # Comprobar si tengo que actualizar o guardar nuevo registro
            DNI = self.txtDNI.text()
            sqlQuery = self.sql.generateFind('nif',DNI)
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
                QMessageBox.information(self, 'Gestión de MiEmpresa', 'Cliente introducido correctamente.')
            else:
                QMessageBox.warning(self, 'Gestión de MiEmpresa', 'Cliente NO se guardo correctamente.')
        else:
            # Actualizar datos
            sqlQuery = self.sql.generateUpdate('nif',DNI)
            self.myDB.executeQuery(sqlQuery)
            QMessageBox.information(self, 'Gestión de MiEmpresa', 'Cliente modificado correctamente.')
        self.limpiarFormulario()

    def eliminarCliente(self):
        if self.__validarNIF() == False:
            return        

        # compruebo que el registro exista en la base de datos        
        DNI = self.txtDNI.text()
        sqlQuery = self.sql.generateFind('nif',DNI)
        result = self.myDB.executeQuery(sqlQuery)
        if len(result) == 0:
            QMessageBox.information(self,"Gestión de MiEmpresa","El cliente "+DNI+" NO existe")
            return

        # Pregunto si esta de acuerdo con eliminar
        if QMessageBox.question(self,"Gestión de MiEmpresa","Esta seguro que desea eliminar? Los datos serán eliminados definitivamente") == QMessageBox.No:
                return
            
        # Elimino
        sqlQuery = self.sql.generateDelete('nif',DNI)
        self.myDB.executeQuery(sqlQuery)
        QMessageBox.information(self,"Gestión de MiEmpresa","Cliente eliminado correctamente.")
        self.limpiarFormulario()
    
    def limpiarFormulario(self):
        self.txtDNI.clear()
        self.txtNombre.clear()
        self.txtDireccion.clear()
        self.txtPoblacion.clear()
        self.cmbProvincia.setCurrentIndex(0)
        self.txtCP.clear()
        self.txtTelefono.clear()
        self.txtEmail.clear()
        self.chbRecargo.setChecked(False)
        self.comboTipoCliente.setCurrentIndex(0)
        self.dtmFechaAlta.setDate(QtCore.QDate.currentDate())
        self.txtObservaciones.clear()
        self.txtDNI.setFocus()
    
    def salirFormularioCliente(self):
        self.parent().close()

    def __validarFormulario(self):
        # validar NIF
        if self.__validarNIF() == False:
            return False
        # validar Nombre
        if self.txtNombre.text() == '':
            QMessageBox.information(self,"Gestión de MiEmpresa","El nombre no puede estar vacío")
            self.txtNombre.setFocus()
            return False   
        # validar telefono
        if self.txtTelefono.text() == '':
            QMessageBox.information(self,"Gestión de MiEmpresa","El telefono no puede estar vacío")
            self.txtTelefono.setFocus()
            return False   
        # validar telefono
        if self.txtEmail.text() == '': #~se permite el email vacio
            return True 
        regEmailValid = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        print(re.search(regEmailValid, self.txtEmail.text()))
        if re.search(regEmailValid, self.txtEmail.text()) == None:
            QMessageBox.information(self,"Gestión de MiEmpresa","Formato de email no valído")
            self.txtEmail.setFocus()
            return False  
        # validar dirección
        if self.txtDireccion.text() == '':
            QMessageBox.information(self,"Gestión de MiEmpresa","La dirección no puede estar vacío")
            self.txtDireccion.setFocus()
            return False        

        return True  

    def __validarNIF(self):
        # validar que no este vacio
        letrasDNI = {'0':"T",'1':"R",'2':"W",'3':"A",'4':"G",'5':"M",'6':"Y",'7':"F",'8':"P",'9':"D",'10':"X",'11':"B",}
        letrasDNI.update({'12':"N",'13':"J",'14':"Z",'15':"S",'16':"Q",'17':"V",'18':"H",'19':"L",'20':"C",'21':"K",'22':"E"})
        tipoDocumento = self.chbTipoDocumento.currentText()
        DNI = self.txtDNI.text()
        if  DNI == '':
            QMessageBox.information(self,"Gestión de MiEmpresa","El DNI del cliente no puede estar vacío")
            self.txtDNI.setFocus()
            return False
        # validar que tenga el formato
        if tipoDocumento == "NIF" or tipoDocumento == "DNI":
            numeroNIF = DNI[0:len(DNI)-1]
            letraNIF = DNI[-1].lower()
            if not numeroNIF.isdigit():
                QMessageBox.information(self,"Gestión de MiEmpresa","El número del NIF no es correcto")
                return False
            resto = int(numeroNIF)%23
            letrasDNI = letrasDNI.get(str(resto)).lower()
            if letraNIF != letrasDNI:
                QMessageBox.information(self,"Gestión de MiEmpresa","El letra de su NIF es incorrecta")
                return False
        return True

    def __cargarTipoClientes(self):
        # consulta a la base de datos tipoClientes
        sqlGen = SQLGenerator('tipoClientes')
        sqlQuery = sqlGen.generateSelect()
        tipoClientesList = self.myDB.executeQuery(sqlQuery)        
        for key,value in tipoClientesList:
            self.comboTipoCliente.addItem(value,key) # guarda el valor a mostrar y su clave
        self.comboTipoCliente.setCurrentIndex(0)
        #print(self.comboTipoCliente.itemData(self.comboTipoCliente.currentIndex()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow =  FrmClientes()
    myWindow.show()
    app.exec_()