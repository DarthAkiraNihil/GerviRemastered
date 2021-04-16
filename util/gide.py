from PyQt5 import QtWidgets

from main import Ui_MainWindow
import sys, pickle, os
from pathlib import Path
CWD = Path.cwd() / '..'
CWD = CWD.absolute().as_posix()
print(CWD)
sys.path.append(CWD + '/core/GRE')


class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setRowCount(4)
        self.ui.menuFile.addAction(self.open)
        self.ui.menuFile.addAction(self.exit)
        self.run = QtWidgets.QAction('Run', self)
        self.run.setShortcut('Ctrl+R')
        self.run.triggered.connect(self.__run)
        self.ui.menuRun.addAction(self.run)
        self.__extractConfig()
        self.fileIsEdited = False
        self.fileName = ''

    def __open(self):
        with open(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', CWD + '/examples')[0]) as fin:
            fileData = fin.read()
            self.ui.textEdit.setText(fileData)

    def __extractConfig(self):
        with open('gide.cfg', 'rb') as iCfg:
            cfg = pickle.load(iCfg)

            self.vmPath = cfg.vmPath
            self.defaultVM = cfg.defaultVM
            self.progPath = cfg.programsPath
    
    def __run(self):
        #if not self.wasCalled:
        self.fname, stat = QtWidgets.QInputDialog.getText(self, 'File saving', 'Enter file name:')
        if stat:
            #print(self.ui.textEdit.toPlainText())
            with open(CWD + f'/{self.progPath}/{self.fname}', 'w+', encoding='utf8') as fout:
                fout.write(self.ui.textEdit.toPlainText())
            #path = os.getcwd()
            # os.chdir('..')
            if self.vmPath != '':
                with open(CWD + f'/{self.vmPath}/{self.defaultVM}', 'rb') as vmf:
                    vm = pickle.load(vmf)
                    vm.runFile(CWD + f'/{self.progPath}/{self.fname}')
                #os.system(f'python ../gervi.py {self.vmPath}/{self.defaultVM} -f {self.progPath}/{self.fname}')
            else:
                pass#os.system(f'python ../gervi.py {self.defaultVM} -f {self.progPath}/{self.fname}')
        #self.wasCallded = True
        #else:
        #    with open(f'../{self.progPath}/{self.fname}', 'w+', encoding='utf8') as fout:
        #        fout.write(self.ui.textEdit.toPlainText())
        #    path = os.getcwd()
        #    os.chdir('..')
        #    if self.vmPath != '':
        #        os.system(f'python gervi.py {self.vmPath}/{self.defaultVM} -f {self.progPath}/{self.fname}')
        #    else:
        #        os.system(f'python gervi.py {self.defaultVM} -f {self.progPath}/{self.fname}')



app = QtWidgets.QApplication([])
application = MainForm()
application.show()

sys.exit(app.exec())