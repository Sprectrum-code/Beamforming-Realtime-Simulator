import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from helper_function.compile_qrc import compile_qrc
from icons_setup.compiledIcons import *

compile_qrc()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Beam Forming')
        self.setWindowIcon(QIcon('icons_setup\icons\logo.png'))

        logoPixmap = QPixmap('icons_setup\icons\logo2.png')

        self.logoLabel = self.findChild(QLabel, 'logoLabel')
        self.logoLabel.setPixmap(logoPixmap)
        self.logoLabel.setAlignment(Qt.AlignCenter) 

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())