import sys
import threading
import time

import numpy as np
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QThread


class RandomDataGeneration(QThread):
    """
    Mandatory Class. This Class must exist.
    """
    new_data = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def data_generation(self):
        while True:
            waiting_time = np.random.randint(1, 4)  # waiting time is given by a random number.
            print(waiting_time)
            time.sleep(waiting_time)
            self.x = np.random.rand(10)
            self.y = np.random.rand(10)
            print(self.x)
            print(self.y)
            self.new_data.emit()

    def run(self):
        self.data_generation()


class Ui_MainWindow():

    def __init__(self):
        super().__init__()

    def start_download(self):
        download_info = threading.Thread(target=animation)
        download_info.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 1024)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(880, 80, 221, 32))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

        self.pushButton.clicked.connect(self.start_download)


class MyMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.download_thread = RandomDataGeneration(self)
        self.download_thread.new_data.connect(self.plot_data)
        self.ui.pushButton.clicked.connect(self.start_download)

    def start_download(self):
        if not self.download_thread.isRunning():
            self.download_thread.start()

    def plot_data(self):
        self.ui.MplWidget.update_plot(self.download_thread.x, self.download_thread.y)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
