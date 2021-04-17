from PyQt5 import QtWidgets, QtGui
from gidecfg_class import GIDEConfig
from gidecfg import Ui_MainWindow
import sys, pickle
from pathlib import Path
CWD = Path.cwd()
CWD = CWD.absolute().as_posix()

class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.__configurate)
        self.ui.pushButton_2.clicked.connect(QtWidgets.qApp.quit)
        self.setWindowTitle('GIDE configuration')
        self.setWindowIcon(QtGui.QIcon(CWD + '/gide_res/gideconfig.png'))
        #QtWidgets.qApp.quit

    def __configurate(self):
        with open('gide.cfg', 'wb+') as oCfg:
            cfg = GIDEConfig(self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), self.ui.lineEdit_3.text())
            pickle.dump(cfg, oCfg)

    
app = QtWidgets.QApplication([])
application = MainForm()
application.show()

sys.exit(app.exec())