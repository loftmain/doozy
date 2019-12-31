## ShapeWidget
import os
from PySide2.QtWidgets import QWidget, QTreeView, QFileSystemModel, QGridLayout, QDockWidget\
    ,QVBoxLayout, QTabWidget, QListWidget, QTextBrowser
from PySide2.QtGui import QPalette, QPainter, QTextCursor
from PySide2.QtCore import Signal,Qt, QRect, QPointF, QEventLoop
from output import StdoutRedirect
from modelingoption import ModelingOption
from labelingoption import labeling
from filetreeview import Tree
from PySide2.QtCore import Slot, Qt

class Mytreeview(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self)

        self.m_TreeView = QTreeView()
        self.m_TreeView.dragEnabled()

        m = QFileSystemModel()
        m.setRootPath("")
        self.m_TreeView.setModel(m)
        self.m_TreeView.setRootIndex(m.index(os.getcwd()))
        layout = QGridLayout()
        layout.addWidget(self.m_TreeView)
        self.setLayout(layout)


from PySide2.QtWidgets import (QMainWindow, QAction, QActionGroup, QToolBar,
                               QLabel,QMessageBox, QTextEdit)
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSettings


class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.setWindowTitle('stock')
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QTextEdit())

        self.treeview_widget = Tree()

        self.dockTree = QDockWidget("TreeView", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockTree)
        self.dockTree.setWidget(self.treeview_widget)

        # text output part
        self.textBrowser = QTextBrowser()
        self._stdout = StdoutRedirect()
        self._stdout.start()
        self._stdout.printOccur.connect(lambda x: self._append_text(x))

        # text output dock
        self.logDock = QDockWidget("Debug & processing Log ...", self)
        self.logDock.setAllowedAreas(Qt.LeftDockWidgetArea |
                             Qt.RightDockWidgetArea |
                             Qt.BottomDockWidgetArea)
        self.logInfo = self.textBrowser
        self.logDock.setWidget(self.logInfo)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.logDock)

        # tab widget
        self.tabWidget = QTabWidget(tabsClosable=True)
        self.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)
        self.setCentralWidget(self.tabWidget)

        # menu bar
        self.createActions()
        self.createMenus()

        self.createStatusBar();
        self.readSettings();
        """
        self.createContextMenu()
        self.createToolBar()
        
        """
    def createActions(self):

        # create actions
        self.importAction = QAction("&import", self)
        #self.exitAction.setIcon(QIcon(":/images/exit.png"))
        self.importAction.setShortcut("Ctrl+I")
        self.importAction.setStatusTip("import files")
        self.importAction.triggered.connect(self.close)

        self.saveDataAction = QAction("&지표 데이터 파일저장", self)
        self.saveDataAction.setStatusTip("import files")
        self.saveDataAction.triggered.connect(self.close)

        self.errorCheckDataAction = QAction("&지표 데이터 에러체크", self)
        self.errorCheckDataAction.setStatusTip("import files")
        self.errorCheckDataAction.triggered.connect(self.close)

        self.exitAction = QAction("&Exit",self)
        self.exitAction.setIcon(QIcon(":/images/exit.png"))
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip("Exit the application")
        self.exitAction.triggered.connect(self.close)

        # view menu
        self.fileViewAction = QAction("&File system view",self, checkable=True)
        #self.triangleAction.setShortcut("Ctrl+T")
        self.fileViewAction.setStatusTip("toggle File system view")
        self.fileViewAction.setChecked(True)
        self.fileViewAction.triggered.connect(self.toggleFileView)

        self.logViewAction = QAction("&System log view",self, checkable=True)
        #self.rectangleAction.setShortcut("Ctrl+R")
        self.logViewAction.setStatusTip("toggle System log view");
        self.logViewAction.setChecked(True)
        self.logViewAction.triggered.connect(self.toggleLogView)

        self.settingViewAction = QAction("&Option setting view",self, checkable=True)
        #self.circleAction.setShortcut("Ctrl+C")
        self.settingViewAction.setStatusTip("toggle Option setting view")
        self.settingViewAction.triggered.connect(self.close)

        # signal menu
        self.labelCreateAction = QAction("&Create", self)
        # self.circleAction.setShortcut("Ctrl+C")
        self.labelCreateAction.setStatusTip("create signal")
        self.labelCreateAction.triggered.connect(self.createLabelTab)

        # modeling menu
        self.modelCreateAction = QAction("&Create", self)
        self.modelCreateAction.setStatusTip("create best modeling")
        self.modelCreateAction.triggered.connect(self.close)

        self.modelOptionAction = QAction("&Modeling option setting", self)
        self.modelOptionAction.setStatusTip("Modeling option setting")
        self.modelOptionAction.triggered.connect(self.createModelOptionTab)

        self.orderCreateAction = QAction("&order create", self)
        self.orderCreateAction.setStatusTip("order create")
        self.orderCreateAction.triggered.connect(self.close)

        self.loginXingAction = QAction("&XingApi Login", self)
        self.loginXingAction.setStatusTip("XingApi Login")
        self.loginXingAction.triggered.connect(self.close)

        self.orderexcuteAction = QAction("&order excute", self)
        self.orderexcuteAction.setStatusTip("order excute")
        self.orderexcuteAction.triggered.connect(self.close)

        # visualization menu
        self.chartAction = QAction("&단일 그래프 chart", self)
        self.chartAction.setStatusTip("단일 그래프 chart")
        self.chartAction.triggered.connect(self.close)

        """
        # actions for colors
        self.redAction = QAction("&Red",self)
        self.redAction.setStatusTip("Set red color")
        self.redAction.setCheckable(True)
        self.redAction.triggered.connect(self.shapeWidget.red)

        self.greenAction = QAction("&Green",self)
        self.greenAction.setStatusTip("Set green color")
        self.greenAction.setCheckable(True);
        self.greenAction.triggered.connect(self.shapeWidget.green)

        self.blueAction = QAction("&Blue",self)
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
        """

    def createMenus(self):
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.importAction)
        fileMenu.addAction(self.saveDataAction)
        fileMenu.addAction(self.errorCheckDataAction)
        fileMenu.addAction(self.exitAction)

        viewMenu = self.menuBar().addMenu("&View")
        viewMenu.addAction(self.fileViewAction);
        viewMenu.addAction(self.logViewAction);
        viewMenu.addAction(self.settingViewAction);

        labelMenu = self.menuBar().addMenu("&Label")
        labelMenu.addAction(self.labelCreateAction)

        modelingMenu = self.menuBar().addMenu("&Modeling")
        modelingMenu.addAction(self.modelCreateAction)
        modelingMenu.addAction(self.modelOptionAction)
        modelingMenu.addAction(self.orderCreateAction)

        simulationMenu = self.menuBar().addMenu("&Simulation")
        simulationMenu.addAction(self.orderexcuteAction)

        visualizationMenu = self.menuBar().addMenu("&Visualization")
        visualizationMenu.addAction(self.chartAction)

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
        settings.setValue("state",self.saveState())

    # event
    def closeEvent(self,event):
        self.writeSettings()

    # slot
    def _append_text(self, msg):
        self.textBrowser.moveCursor(QTextCursor.End)
        self.textBrowser.insertPlainText(msg)
        # refresh textedit show, refer) https://doc.qt.io/qt-5/qeventloop.html#ProcessEventsFlag-enum
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def setColor(self,action):
        if action == self.redAction:
            self.shapeWidget.red()
        elif action == self.greenAction:
            self.shapeWidget.green()
        else:
            self.shapeWidget.blue()

    def createLabelTab(self):
        widget = labeling()
        widget.destroyed.connect(
            lambda obj: print(
                "deleted {}, count: {}".format(obj, self.tabWidget.count())
            )
        )
        self.tabWidget.addTab(widget, "labeling")

    def createModelOptionTab(self):
        widget = ModelingOption()
        widget.destroyed.connect(
            lambda obj: print(
                "deleted {}, count: {}".format(obj, self.tabWidget.count())
            )
        )
        self.tabWidget.addTab(widget, "modeling option setting")

    def toggleFileView(self, state):
        if state:
            self.dockTree.show()
        else:
            self.dockTree.hide()

    def toggleLogView(self, state):
        if state:
            self.logDock.show()
        else:
            self.logDock.hide()



    def onTabCloseRequested(self, index):
        widget = self.tabWidget.widget(index)
        widget.deleteLater()

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
    mainWindow.resize(1200, 800)
    mainWindow.show()

    app.exec_()