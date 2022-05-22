from PyQt5 import QtWidgets, QtGui
from pathlib import Path
import sys, pickle, os, traceback
CWDR = Path.cwd()
CWD = Path.cwd() / '..'
CWD = CWD.absolute().as_posix()
CWDR = CWDR.absolute().as_posix()
#print(CWD)
sys.path.append(CWDR)
sys.path.append(CWD + '/core/GRE')
print(sys.path)
from main import Ui_MainWindow


from setup import Ui_Dialog
from gidecfg_class import GIDEConfig
#from loguru import logger

#logger.add('dev.log', format='[{time:HH:mm:ss}] <lvl>{message}</lvl>', level = 'DEBUG')
#logger.add(sys.stdout, format='[{time:HH:mm:ss}] <lvl>{message}</lvl>', level = 'INFO')
#logger.info(CWD, style = 'braces')

 
class ConfigDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(ConfigDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('GIDE configuration')
        self.setWindowIcon(QtGui.QIcon(CWD + '/util/gide_res/gideconfig.png'))
        self.pushButton.clicked.connect(self.__browse)
        self.pushButton_2.clicked.connect(self.__chooseDir)
        self.configFile = GIDEConfig('config.ini')
        self.configuration = self.configFile.extract()
        self.lineEdit.setText(self.configuration['INTERPRETER']['vmpath'])
        self.lineEdit_2.setText(self.configuration['INTERPRETER']['progsdir'])
        self.hasItChanged = {
            'vmpath' : False,
            'progsDir' : False
        }
    
    def __browse(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Select default VM', CWD)[0]
        self.hasItChanged['vmpath'] = True
        self.lineEdit.setText(fname[2:])
    
    def __chooseDir(self):
        dirName =str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select programs directory'))
        self.hasItChanged['progsDir'] = True
        self.lineEdit_2.setText(dirName[2:])

    def setupGide(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            #vmPath, progsDir = self.lineEdit.text() if self.hasItChanged['vmpath'] else 'PREVIOUS', self.lineEdit_2.text() if self.hasItChanged['progsDir'] else 'PREVIOUS'
            return ['INTERPRETER', 'INTERPRETER'], ['VMPath', 'ProgsDir'], [self.lineEdit.text(), self.lineEdit_2.text()]
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

        self.configFile = GIDEConfig('config.ini')
        self.configuration = {}
        self.wasCalled = False
        self.fname = ''

        self.open = QtWidgets.QAction('Open', self)
        self.open.setShortcut('Ctrl+O')
        self.open.triggered.connect(self.__open)
        self.ui.menuFile.addAction(self.open)
        self.ui.menuFile.addAction(self.exit)
        self.run = QtWidgets.QAction('Run', self)
        self.run.setShortcut('Ctrl+R')
        self.run.triggered.connect(self.__run)
        self.ui.menuRun.addAction(self.run)
        self.__extractConfig()
        self.fileIsEdited = False
        self.fileName = ''
        print(self.configuration)
        self.about = QtWidgets.QAction('About Gide', self)
        self.about.triggered.connect(self.__about)
        self.ui.menuHelp.addAction(self.about)
        self.config = QtWidgets.QAction('Setup GIDE...', self)
        self.config.triggered.connect(self.__launchConfig)
        self.ui.menuAbout.addAction(self.config)
        self.setWindowTitle(f'GIDE version {self.__ver}')
        self.setWindowIcon(QtGui.QIcon(CWD + '/util/gide_res/gide.png'))

        

    def __bonk(self, msg):
        QtWidgets.QMessageBox.critical(self, 'Error!', msg)


    def __about(self):
        QtWidgets.QMessageBox.information(self, 'About GIDE', f'GIDE version {self.__ver}.\nGIDE - It just works!\nA IDE for writing Gervi scripts\nBy TheSwagVader. github.com/TheSwagVader')

    def __open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', self.configuration['INTERPRETER']['progsdir'])[0]
        if fname != '':
            with open(fname, 'r') as fin:
                fileData = fin.read()
                self.ui.textEdit.setText(fileData)
                self.fname = fname
                self.wasCalled = True

    def __extractConfig(self):
        self.configuration = self.configFile.extract()
    
    def __launchConfig(self):
        setupWin = ConfigDialog()
        res = setupWin.setupGide()
        if res:
            sections, parameters, values = res
            self.configFile.setOptions(sections, parameters, values)
            self.configFile.update()
            self.__extractConfig()

    def __run(self):
        self.fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', self.configuration['INTERPRETER']['progsdir'])[0]
        if self.fname != '':
            if self.fname == 'i_want_to_be_boss_of_this_gym' and self.ui.textEdit.toPlainText() == 'JABRONI':
                QtWidgets.QMessageBox.information(self,'You picked wrong door!', ' Leatherclub two blocks down!')
            else:
                #prog = os.path.expanduser('%s/%s' % (self.configuration['INTERPRETER']['progsdir'], self.fname))
                try:
                    with open(self.fname, 'w+', encoding='utf8') as fout:
                        fout.write(self.ui.textEdit.toPlainText())
                except Exception as e:
                    self.__bonk(traceback.format_exc())
                    return
                if self.configuration['INTERPRETER']['vmpath'] != '':
                    try:
                        with open(self.configuration['INTERPRETER']['vmpath'], 'rb') as vmf:
                            vm = pickle.load(vmf)
                            vm.runFile(self.fname)
                            self.ui.textBrowser_2.setText(vm.getOutputStream())
                            self.ui.textBrowser.setText(vm.getState())
                    except Exception as e:
                        self.__bonk(traceback.format_exc())
                        return
                else:
                    pass
print(sys.path)
app = QtWidgets.QApplication([])
application = MainForm()
application.show()

sys.exit(app.exec())