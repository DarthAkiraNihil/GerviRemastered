from PyQt5 import QtWidgets
from gidecfg_class import GIDEConfig
from gidecfg import Ui_MainWindow
import sys, pickle
class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.__configurate)

    def __configurate(self):
        with open('gide.cfg', 'wb+') as oCfg:
            cfg = GIDEConfig(self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), self.ui.lineEdit_3.text())
            pickle.dump(cfg, oCfg)

    
app = QtWidgets.QApplication([])
application = MainForm()
application.show()

sys.exit(app.exec())