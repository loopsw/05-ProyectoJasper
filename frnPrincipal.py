from PyQt5.uic.uiparser import QtCore
from frmClientes import FrmClientes
from frmTipoClientes import FrmTipoClientes
from frmProductos import FrmProductos
import os, sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication,QMdiSubWindow,QMessageBox
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = 'frmPrincipal.ui'
PATH_FORM = os.path.join(BASE_DIR,'FormulariosUI',FILE_NAME)

class FrmPrincipal(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        uic.loadUi(PATH_FORM,self)
        self.showMaximized()
        self.menuClientes.triggered.connect(self.abrirClientes)
        self.menuTipoClientes.triggered.connect(self.abrirTipoclientes)
        self.menuProductos.triggered.connect(self.abrirProductos)
        self.menuSalir.triggered.connect(self.salir)

    def salir(self):
        if QMessageBox.question(self, 'Gestión MiEmpresa', 'Desea realmente salir?') == QMessageBox.No:
            return
        self.close()

    def abrirProductos(self):
        sub = QMdiSubWindow()
        sub.setWidget(FrmProductos())
        sub.setAttribute(QtCore.Qt.WA_DeleteOnClose,True)        
        self.mdiArea.addSubWindow(sub)
        #sub.showMaximized()
        sub.show()

    def abrirClientes(self):
        sub = QMdiSubWindow()
        sub.setWidget(FrmClientes())
        sub.setAttribute(QtCore.Qt.WA_DeleteOnClose,True)        
        self.mdiArea.addSubWindow(sub)
        #sub.showMaximized()
        sub.show()
    
    def abrirTipoclientes(self):
        sub = QMdiSubWindow()
        sub.setWidget(FrmTipoClientes())
        sub.setAttribute(QtCore.Qt.WA_DeleteOnClose,True)        
        self.mdiArea.addSubWindow(sub)        
        #sub.showMaximized()
        sub.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = FrmPrincipal()
    myWindow.show()
    sys.exit(app.exec_())