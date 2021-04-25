from PyQt5 import QtWidgets, QtGui

from main import Ui_MainWindow
import sys, pickle, os, traceback
from pathlib import Path
from setup import Ui_Dialog
from gidecfg_class import GIDEConfig
#from loguru import logger
CWD = Path.cwd() / '..'
CWD = CWD.absolute().as_posix()
#print(CWD)
sys.path.append(CWD + '/core/GRE')
#logger.add('dev.log', format='[{time:HH:mm:ss}] <lvl>{message}</lvl>', level = 'DEBUG')
#logger.add(sys.stdout, format='[{time:HH:mm:ss}] <lvl>{message}</lvl>', level = 'INFO')
#logger.info(CWD, style = 'braces')
class ConfigDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(ConfigDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('GIDE configuration')
        self.setWindowIcon(QtGui.QIcon(CWD + '/util/gide_res/gideconfig.png'))
    
    def setupGide(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            return self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text()
        else:
            return None

class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.__ver = '0.5'

        self.exit = QtWidgets.QAction('Exit', self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.triggered.connect(QtWidgets.qApp.quit)

        self.vmPath = ''
        self.defaultVM = ''
        self.progPath = ''
        self.wasCalled = False
        self.fname = ''

        self.open = QtWidgets.QAction('Open', self)
        self.open.setShortcut('Ctrl+O')
        self.open.triggered.connect(self.__open)
        #self.ui.tableWidget.setColumnCount(2)
        #self.ui.tableWidget.setRowCount(4)
        self.ui.menuFile.addAction(self.open)
        self.ui.menuFile.addAction(self.exit)
        self.run = QtWidgets.QAction('Run', self)
        self.run.setShortcut('Ctrl+R')
        self.run.triggered.connect(self.__run)
        self.ui.menuRun.addAction(self.run)
        self.__extractConfig()
        self.fileIsEdited = False
        self.fileName = ''

        self.about = QtWidgets.QAction('About Gide', self)
        self.about.triggered.connect(self.__about)
        self.ui.menuHelp.addAction(self.about)
        self.config = QtWidgets.QAction('Setup GIDE...', self)
        #self.config.setShortcut('Ct')
        self.config.triggered.connect(self.__launchConfig)
        self.ui.menuAbout.addAction(self.config)
        self.setWindowTitle(f'GIDE version {self.__ver}')
        self.setWindowIcon(QtGui.QIcon(CWD + '/util/gide_res/gide.png'))

        

    def __bonk(self, msg):
        QtWidgets.QMessageBox.critical(self, 'Error!', msg)


    def __about(self):
        QtWidgets.QMessageBox.information(self, 'About GIDE', f'GIDE version {self.__ver}.\nA IDE for writing Gervi scripts\nBy TheSwagVader. github.com/TheSwagVader')
    def __open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', CWD + '/examples')[0]
        with open(fname, 'r') as fin:
            fileData = fin.read()
            self.ui.textEdit.setText(fileData)
            self.fname = fname
            self.wasCalled = True

    def __extractConfig(self):
        with open('gide.cfg', 'rb') as iCfg:
            cfg = pickle.load(iCfg)

            self.vmPath = cfg.vmPath
            self.defaultVM = cfg.defaultVM
            self.progPath = cfg.programsPath
    
    def __launchConfig(self):
        setupWin = ConfigDialog()
        res = setupWin.setupGide()
        if res:
            v1, v2, v3 = res
            with open('gide.cfg', 'wb+') as oCfg:
                cfg = GIDEConfig(v1, v2, v3)
                pickle.dump(cfg, oCfg)
        self.__extractConfig()

    def __run(self):
        self.fname, stat = QtWidgets.QInputDialog.getText(self, 'File saving', 'Enter file name:')
        if stat:
            if self.fname == 'i_want_to_be_boss_of_this_gym' and self.ui.textEdit.toPlainText() == 'JABRONI':
                QtWidgets.QMessageBox.information(self,'You picked wrong door!', ' Leatherclub two blocks down!')
            else:
                try:
                    with open(CWD + f'/{self.progPath}/{self.fname}', 'w+', encoding='utf8') as fout:
                        fout.write(self.ui.textEdit.toPlainText())
                except Exception as e:
                    self.__bonk(traceback.format_exc())
                    return
                if self.vmPath != '':
                    try:
                        with open(CWD + f'/{self.vmPath}/{self.defaultVM}', 'rb') as vmf:
                            vm = pickle.load(vmf)
                            vm.runFile(CWD + f'/{self.progPath}/{self.fname}')
                            self.ui.textBrowser_2.setText(vm.getOutputStream())
                            self.ui.textBrowser.setText(vm.getState())
                    except Exception as e:
                        self.__bonk(traceback.format_exc())
                        return
                else:
                    pass

app = QtWidgets.QApplication([])
application = MainForm()
application.show()

sys.exit(app.exec())