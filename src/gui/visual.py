#!/usr/bin/env python
# coding: utf-8

# visualization part

import platform
import sys

import pandas as pd
from PySide2.QtGui import QIcon, QDropEvent
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QSpacerItem, QSizePolicy, QPushButton, QComboBox
from matplotlib import font_manager
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from module.io import get_refined_path

if platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
elif platform.system() == 'Linux':
    font_name = font_manager.FontProperties(fname="/src/doozy.git/setup/font/GSTTF.ttf").get_name()
#rc('font', family=font_name)

__author__ = 'Jinjae Lee <leejinjae7@gmail.com>'


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
        # self.setLayout(QVBoxLayout())
        self.setAcceptDrops(True)
        self.canvas = PlotCanvas(self, width=10, height=8)
        self.toolbar = NavigationToolbar(self.canvas, self)
        # self.layout().addWidget(self.toolbar)
        # self.layout().addWidget(self.canvas)

        self.path = ''

        self.cb_option = QComboBox(self)
        self.cb_option.addItem('자산변동흐름', 'moneyflow')
        self.cb_option.addItem('수익률', 'per')
        self.cb_option.currentTextChanged.connect(self.change_subplot)


        # self.fig = plt.Figure()
        # self.canvas = FigureCanvas(self.fig)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.toolbar)
        leftLayout.addWidget(self.canvas)

        # Right Layout
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.cb_option)
        rightLayout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)

        self.setLayout(layout)

    def change_subplot(self):
        if self.cb_option.currentData() == 'moneyflow':
            self.canvas.update_subplot(1)
        elif self.cb_option.currentData() == 'per':
            self.canvas.update_subplot(1)

    def dropEvent(self, event: QDropEvent):
        print("Drop!")
        path = get_refined_path(event.mimeData().text())
        print(get_refined_path(event.mimeData().text()))
        # self.canvas._plot_money_flow(path)
        self.path = path
        if self.cb_option.currentData() == 'moneyflow':
            self.canvas._plot_money_flow(path)
        elif self.cb_option.currentData() == 'per':
            self.canvas._plot_per(path)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = [self.fig.add_subplot(111)]

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.plot()

    def _plot_per(self, path):
        """
        DJI -> 형태 변경해야함

        :param path:
        :return:
        """
        data = pd.read_csv(path, index_col=0, parse_dates=[0])
        # ax = self.figure.add_subplot(111)
        style.use("ggplot")
        self.axes[0].plot(data.portfolio_value.pct_change().fillna(0).add(1).cumprod().sub(1), label='portfolio')
        self.axes[0].plot(data.DJI.pct_change().fillna(0).add(1).cumprod().sub(1), label='benchmark')
        # data.portfolio_value.pct_change().fillna(0).add(1).cumprod().sub(1).plot(label='portfolio')
        # data.DJI.pct_change().fillna(0).add(1).cumprod().sub(1).plot(label='benchmark')
        self.axes[0].legend(loc=2)
        self.axes[0].set_title('수익률')
        self.draw()

    def _plot_money_flow(self, path):
        data = pd.read_csv(path, index_col=0, parse_dates=[0])
        # ax = self.figure.add_subplot(111)
        self.axes[0].plot(data.index, data.portfolio_value)
        self.axes[0].legend(loc='best')

        self.axes[0].plot(data.ix[data.buy == True].index, data.portfolio_value[data.buy == True], '^')
        self.axes[0].plot(data.ix[data.sell == True].index, data.portfolio_value[data.sell == True], 'v')
        self.axes[0].set_title('money flow')
        self.draw()

    def update_subplot(self, count):
        [self.fig.delaxes(ax) for ax in self.axes]
        self.axes = [self.fig.add_subplot(count, 1, i + 1) for i in range(count)]
        self.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
