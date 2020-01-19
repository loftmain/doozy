import random
import sys

import pandas as pd
from PySide2.QtGui import QIcon, QDropEvent
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QSpacerItem, QSizePolicy, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from src.module.io import get_refined_path


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.title = 'test'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 800

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage('Ready')

        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('File')
        helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        vlay = QVBoxLayout(widget)
        hlay = QHBoxLayout()
        vlay.addLayout(hlay)

        self.nameLabel = QLabel('Name:', self)
        self.line = QLineEdit(self)
        self.nameLabel2 = QLabel('Result', self)

        hlay.addWidget(self.nameLabel)
        hlay.addWidget(self.line)
        hlay.addWidget(self.nameLabel2)
        hlay.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))

        pybutton = QPushButton('Click me', self)
        pybutton.clicked.connect(self.clickMethod)
        hlay2 = QHBoxLayout()
        hlay2.addWidget(pybutton)
        hlay2.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
        vlay.addLayout(hlay2)
        m = PlotWidget(self)
        vlay.addWidget(m)

    def clickMethod(self):
        print('Clicked Pyqt button.')
        if self.line.text() == '':
            self.statusBar().showMessage('Not a Number')
        else:
            print('Number: {}'.format(float(self.line.text()) * 2))
            self.statusBar().showMessage('Introduction of a number')
            self.nameLabel2.setText(str(float(self.line.text()) * 2))


class PlotWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.setAcceptDrops(True)
        self.canvas = PlotCanvas(self, width=10, height=8)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

    def dropEvent(self, event: QDropEvent):
        print("Drop!")
        path = get_refined_path(event.mimeData().text())
        print(get_refined_path(event.mimeData().text()))
        self.canvas._plot_money_flow(path)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.plot()

    def plot(self):
        data = [random.random() for i in range(250)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-', linewidth=0.5)
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

    def _plot_money_flow(self, path):
        data = pd.read_csv(path, index_col=0, parse_dates=[0])
        ax = self.figure.add_subplot(111)
        ax.plot(data.index, data.portfolio_value)
        ax.legend(loc='best')

        ax.plot(data.ix[data.buy == True].index, data.portfolio_value[data.buy == True], '^')
        ax.plot(data.ix[data.sell == True].index, data.portfolio_value[data.sell == True], 'v')
        ax.set_title('money flow')
        self.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
