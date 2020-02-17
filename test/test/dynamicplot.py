import sys

from PySide2 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Plot(FigureCanvas):
    def __init__(self, parent=None, width=5.4, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = [self.fig.add_subplot(211), self.fig.add_subplot(212)]
        self.fig.set_facecolor("none")
        self.fig.set_tight_layout(True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_subplot(self, count):
        [self.fig.delaxes(ax) for ax in self.axes]
        self.axes = [self.fig.add_subplot(count, 1, i + 1) for i in range(count)]
        self.draw()


class PlotWidget(QtWidgets.QWidget):
    def __init__(self):
        super(PlotWidget, self).__init__()
        self.initPlot()
        self.initUI()

    def initPlot(self):
        self.plot = Plot()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        grid = QtWidgets.QGridLayout(self)
        grid.addWidget(self.plot, 3, 0, 1, 2)

        btn1 = QtWidgets.QPushButton('1 Subplot ', self)
        btn1.clicked.connect(lambda: self.plot.update_subplot(1))
        grid.addWidget(btn1, 5, 0)

        btn2 = QtWidgets.QPushButton('2 Subplots ', self)
        btn2.clicked.connect(lambda: self.plot.update_subplot(2))
        grid.addWidget(btn2, 5, 1)

        self.show()


app = QtWidgets.QApplication(sys.argv)
window = PlotWidget()
window.show()
sys.exit(app.exec_())
