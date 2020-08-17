import sys

from PySide2.QtWidgets import QApplication
from gui.gui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.resize(1600, 1200)
    mainWindow.show()

    app.exec_()
