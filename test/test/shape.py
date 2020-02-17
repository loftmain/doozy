## ShapeWidget
from PySide2.QtCore import Signal, Qt, QRect, QPointF
from PySide2.QtGui import QPalette, QPainter
from PySide2.QtWidgets import QWidget


class ShapeWidget(QWidget):
    mousePositionChanged = Signal(str)  # mousePositionChanged(pos)
    NONE, RECTANGLE, TRIANGLE, CIRCLE = 0, 1, 2, 3  # constants

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setBackgroundRole(QPalette.Light)
        self.setAutoFillBackground(True)

        self.shape = ShapeWidget.NONE
        self.color = Qt.blue

    # slots
    def rectangle(self):
        self.shape = ShapeWidget.RECTANGLE
        self.update()

    def triangle(self):
        self.shape = ShapeWidget.TRIANGLE
        self.update()

    def circle(self):
        self.shape = ShapeWidget.CIRCLE
        self.update()

    def red(self):
        self.color = Qt.red
        self.update()

    def green(self):
        self.color = Qt.green
        self.update()

    def blue(self):
        self.color = Qt.blue
        self.update()

    def setMouseTracking(self, track):
        QWidget.setMouseTracking(self, track)

    # event handler
    def mouseMoveEvent(self, event):
        pos = "({},{})".format(event.x(), event.y())
        self.mousePositionChanged.emit(pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.color)
        r = QRect(self.width() / 4, self.height() / 4, self.width() / 2, self.height() / 2)
        if self.shape == ShapeWidget.RECTANGLE:
            painter.drawRect(r)
        elif self.shape == ShapeWidget.TRIANGLE:
            points = [QPointF(r.left() + r.width() / 2, r.top()),
                      r.bottomLeft(), r.bottomRight()]
            painter.drawPolygon(points)

        elif self.shape == ShapeWidget.CIRCLE:
            painter.drawEllipse(r)


from PySide2.QtWidgets import (QMainWindow, QAction, QActionGroup, QLabel, QMessageBox)
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSettings


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Shape')
        self.setWindowIcon(QIcon(":/images/qt.png"))

        self.shapeWidget = ShapeWidget()
        self.setCentralWidget(self.shapeWidget)

        self.createActions();

        self.createMenus();
        """
        self.createContextMenu();
        self.createToolBar();
        self.createStatusBar();
        self.readSettings();
        """

    def createActions(self):

        # create actions
        self.exitAction = QAction("E&xit", self)
        self.exitAction.setIcon(QIcon(":/images/exit.png"))
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip("Exit the application")
        self.exitAction.triggered.connect(self.close)

        self.triangleAction = QAction("&Triangle", self)
        self.triangleAction.setIcon(QIcon(":/images/triangle.png"))
        self.triangleAction.setShortcut("Ctrl+T");
        self.triangleAction.setStatusTip("Draw a triangle")
        self.triangleAction.triggered.connect(self.shapeWidget.triangle)

        self.rectangleAction = QAction("&Rectangle", self)
        self.rectangleAction.setIcon(QIcon(":/images/rectangle.png"));
        self.rectangleAction.setShortcut("Ctrl+R")
        self.rectangleAction.setStatusTip("Draw a rectangle");
        self.rectangleAction.triggered.connect(self.shapeWidget.rectangle)

        self.circleAction = QAction("&Circle", self)
        self.circleAction.setIcon(QIcon(":/images/circle.png"))
        self.circleAction.setShortcut("Ctrl+C")
        self.circleAction.setStatusTip("Draw a circle")
        self.circleAction.triggered.connect(self.shapeWidget.circle)

        # actions for colors
        self.redAction = QAction("&Red", self)
        self.redAction.setStatusTip("Set red color")
        self.redAction.setCheckable(True)
        self.redAction.triggered.connect(self.shapeWidget.red)

        self.greenAction = QAction("&Green", self)
        self.greenAction.setStatusTip("Set green color")
        self.greenAction.setCheckable(True);
        self.greenAction.triggered.connect(self.shapeWidget.green)

        self.blueAction = QAction("&Blue", self)
        self.blueAction.setStatusTip("Set blue color")
        self.blueAction.setCheckable(True)
        self.blueAction.triggered.connect(self.shapeWidget.blue)

        self.colorActionGroup = QActionGroup(self)
        self.colorActionGroup.addAction(self.redAction);
        self.colorActionGroup.addAction(self.greenAction);
        self.colorActionGroup.addAction(self.blueAction);
        self.redAction.setChecked(True);
        self.colorActionGroup.triggered.connect(self.setColor)
        # (triggered(QAction*)),this,SLOT(setColor(QAction*)));

        # mouse tracking
        self.mouseTrackingAction = QAction("M&ouse tracking", self)
        self.mouseTrackingAction.setStatusTip("mouse tracking on/off")
        self.mouseTrackingAction.setCheckable(True)
        self.mouseTrackingAction.setChecked(self.shapeWidget.hasMouseTracking())
        self.mouseTrackingAction.triggered.connect(self.shapeWidget.setMouseTracking)
        # connect(mouseTrackingAction,SIGNAL(triggered(bool)), shapeWidget, SLOT(setMouseTracking(bool)));

        # about
        self.aboutAction = QAction("&About", self)
        self.aboutAction.setStatusTip("Show the application's About box")
        self.aboutAction.triggered.connect(self.about)

    def createMenus(self):
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.exitAction)

        shapeMenu = self.menuBar().addMenu("&Shape")
        shapeMenu.addAction(self.triangleAction);
        shapeMenu.addAction(self.rectangleAction);
        shapeMenu.addAction(self.circleAction);

        colorMenu = self.menuBar().addMenu("&Color")
        colorMenu.addAction(self.redAction)
        colorMenu.addAction(self.greenAction)
        colorMenu.addAction(self.blueAction)

        mouseMenu = self.menuBar().addMenu("&Mouse")
        mouseMenu.addAction(self.mouseTrackingAction)

        aboutMenu = self.menuBar().addMenu("&About")
        aboutMenu.addAction(self.aboutAction)

    def createContextMenu(self):
        self.shapeWidget.addAction(self.triangleAction)
        self.shapeWidget.addAction(self.rectangleAction)
        self.shapeWidget.addAction(self.circleAction)
        self.shapeWidget.addAction(self.redAction)
        self.shapeWidget.addAction(self.greenAction)
        self.shapeWidget.addAction(self.blueAction)

        self.shapeWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

    def createToolBar(self):
        shapeToolBar = self.addToolBar("&Shape")
        shapeToolBar.setObjectName("ShapeToolBar")
        shapeToolBar.addAction(self.triangleAction)
        shapeToolBar.addAction(self.rectangleAction)
        shapeToolBar.addAction(self.circleAction)

    def createStatusBar(self):
        locationLabel = QLabel(" (  0,  0) ")
        locationLabel.setAlignment(Qt.AlignHCenter)
        locationLabel.setMinimumSize(locationLabel.sizeHint())
        self.shapeWidget.mousePositionChanged.connect(locationLabel.setText)
        # shapeWidget.mousePositionChanged(str) - QLabel.setText(str)

        self.statusBar().addWidget(locationLabel)

    def readSettings(self):
        settings = QSettings("Qt5Programming Inc.", "Shape")

        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("state"))

    def writeSettings(self):
        settings = QSettings("Qt5Programming Inc.", "Shape")

        self.saveGeometry()
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())

    # event
    def closeEvent(self, event):
        self.writeSettings()

    # slot
    def setColor(self, action):
        if action == self.redAction:
            self.shapeWidget.red()
        elif action == self.greenAction:
            self.shapeWidget.green()
        else:
            self.shapeWidget.blue()

    def about(self):
        QMessageBox.about(self, "About Shape",
                          "<h2>Shape 1.0</h2>"
                          "<p>Copyright &copy; 2014 Q5Programming Inc."
                          "<p>Shape is a small application that "
                          "demonstrates QAction, QMainWindow, QMenuBar, "
                          "QStatusBar, QToolBar, and many other "
                          "Qt classes.")


import sys
from PySide2.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    app.exec_()
