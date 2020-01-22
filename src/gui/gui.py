#!interpreter [project-doozy]
# -*- coding: utf-8 -*-

"""
gui runcher
{License_info} 라이센스 정해야함
"""

# Built-in/Generic Imports
import os

# Libs
import PySide2
from PySide2.QtCore import QEventLoop, QSettings
from PySide2.QtCore import Qt
from PySide2.QtGui import QTextCursor, QIcon
from PySide2.QtWidgets import (QDockWidget, QTabWidget, QTextBrowser, QFileDialog \
    , QMainWindow, QAction, QLabel, QMessageBox)

from src.gui.download import DlIndependentDialog
from src.gui.filetreeview import Tree
from src.gui.markingwidget import MarkingWidget
from src.gui.modelingoption import ModelingOption
from src.gui.orderexcute import OrderRunWidget
from src.gui.orderwidget import CreateOrderWidget
# Own modules
from src.gui.output import StdoutRedirect
from src.gui.visual import PlotWidget

__author__ = 'loftmain'
__copyright__ = 'Copyright 2020, doozy'
__credits__ = ['loftmain']
__license__ = '{license}'
__version__ = '0.0.1'
__maintainer__ = 'loftmain'
__email__ = 'leejinjae7@gmail.com'
__status__ = 'Dev'

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class MainWindow(QMainWindow):
    """
          main window

    """

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('doozy stock')

        # current directory
        self.path_to_file = os.getcwd()

        # tree system file view dock widget
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

        # tab widget setting
        self.tabWidget = QTabWidget(tabsClosable=True)
        self.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)
        self.setCentralWidget(self.tabWidget)

        # menu bar
        self.createActions()
        self.createMenus()

        self.createStatusBar()
        self.readSettings()
        """
        self.createContextMenu()
        self.createToolBar()
        
        """
    def createActions(self):

        # create actions
        self.newProject = QAction("&New Project", self)
        self.newProject.setShortcut("Ctrl+N")
        self.newProject.setStatusTip("create a new project")
        self.newProject.triggered.connect(self.load_folder)

        self.openProject = QAction("&Open Project", self)
        self.openProject.setShortcut("Ctrl+O")
        self.openProject.setStatusTip("Open a project in treeview")
        self.openProject.triggered.connect(self.load_folder)

        self.saveDataAction = QAction("&지표 데이터 파일저장", self)
        self.saveDataAction.setStatusTip("import files")
        self.saveDataAction.triggered.connect(self.dl_independents)

        self.errorCheckDataAction = QAction("&지표 데이터 에러체크", self)
        self.errorCheckDataAction.setStatusTip("import files")
        self.errorCheckDataAction.triggered.connect(self.close)

        self.exitAction = QAction("&Exit", self)
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
        self.logViewAction.setStatusTip("toggle System log view")
        self.logViewAction.setChecked(True)
        self.logViewAction.triggered.connect(self.toggleLogView)

        self.settingViewAction = QAction("&Option setting view", self, checkable=True)
        # self.circleAction.setShortcut("Ctrl+C")
        self.settingViewAction.setStatusTip("toggle Option setting view")
        self.settingViewAction.triggered.connect(self.close)

        # signal menu
        self.MarkingCreateAction = QAction("&Create", self)
        # self.circleAction.setShortcut("Ctrl+C")
        self.MarkingCreateAction.setStatusTip("create Mark")
        self.MarkingCreateAction.triggered.connect(self.createLabelTab)

        # modeling menu
        self.modelCreateAction = QAction("&Create", self)
        self.modelCreateAction.setStatusTip("create best modeling")
        self.modelCreateAction.triggered.connect(self.close)

        self.modelOptionAction = QAction("&Modeling option setting", self)
        self.modelOptionAction.setStatusTip("Modeling option setting")
        self.modelOptionAction.triggered.connect(self.createModelOptionTab)

        self.orderCreateAction = QAction("&order create", self)
        self.orderCreateAction.setStatusTip("order create")
        self.orderCreateAction.triggered.connect(self.createOrderTab)

        self.loginXingAction = QAction("&XingApi Login", self)
        self.loginXingAction.setStatusTip("XingApi Login")
        self.loginXingAction.triggered.connect(self.close)

        self.orderexcuteAction = QAction("&order excute", self)
        self.orderexcuteAction.setStatusTip("order excute")
        self.orderexcuteAction.triggered.connect(self.createOrderExecuteTab)

        # visualization menu
        self.chartAction = QAction("&단일 그래프 chart", self)
        self.chartAction.setStatusTip("단일 그래프 chart")
        self.chartAction.triggered.connect(self.createPlotTab)


    def createMenus(self):

        projectMenu = self.menuBar().addMenu("&Project")
        projectMenu.addAction(self.newProject)
        projectMenu.addAction(self.openProject)
        projectMenu.addAction(self.exitAction)

        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.saveDataAction)
        fileMenu.addAction(self.errorCheckDataAction)

        viewMenu = self.menuBar().addMenu("&View")
        viewMenu.addAction(self.dockTree.toggleViewAction())
        viewMenu.addAction(self.logDock.toggleViewAction())
        viewMenu.addAction(self.settingViewAction)

        MarkingMenu = self.menuBar().addMenu("&Marking")
        MarkingMenu.addAction(self.MarkingCreateAction)

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
        settings = QSettings("doozy Inc.", "Shape")

        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("state"))

    def writeSettings(self):
        settings = QSettings("doozy Inc.", "Shape")

        self.saveGeometry()
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state",self.saveState())

    # event
    def closeEvent(self,event):
        self.writeSettings()

    # slot
    def load_folder(self):
        self.path_to_file = QFileDialog.getExistingDirectory(self, self.tr("Load folder"), self.tr("~/Desktop/"), QFileDialog.ShowDirsOnly
                                             | QFileDialog.DontResolveSymlinks)
        print(self.path_to_file)
        self.treeview_widget.change_root_index(self.path_to_file)
        os.chdir(self.path_to_file)

    def dl_independents(self):
        dlg = DlIndependentDialog(self.path_to_file)
        dlg.exec_()


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
        widget = MarkingWidget(self.path_to_file)
        widget.destroyed.connect(
            lambda obj: print(
                "deleted {}, count: {}".format(obj, self.tabWidget.count())
            )
        )
        self.tabWidget.addTab(widget, "Marking")

    def createModelOptionTab(self):
        widget = ModelingOption(self.path_to_file)
        widget.destroyed.connect(
            lambda obj: print(
                "deleted {}, count: {}".format(obj, self.tabWidget.count())
            )
        )
        self.tabWidget.addTab(widget, "modeling option setting")

    def createOrderTab(self):
        widget = CreateOrderWidget(self.path_to_file)
        widget.destroyed.connect(
            lambda obj: print(
                "deleted {}, count: {}".format(obj, self.tabWidget.count())
            )
        )
        self.tabWidget.addTab(widget, "order create")

    def createOrderExecuteTab(self):
        widget = OrderRunWidget(self.path_to_file)
        widget.destroyed.connect(
            lambda obj: print(
                "deleted {}, count: {}".format(obj, self.tabWidget.count())
            )
        )
        self.tabWidget.addTab(widget, "order execute")

    def createPlotTab(self):
        widget = PlotWidget()
        widget.destroyed.connect(
            lambda obj: print(
                "deleted {}, count: {}".format(obj, self.tabWidget.count())
            )
        )
        self.tabWidget.addTab(widget, "Plot")

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
        QMessageBox.about(self, "About doozy",
                          "<h2>Shape 1.0</h2>"
                          "<p>Copyright doozy;"
                          "<p>")

import sys
from PySide2.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.resize(1600, 1200)
    mainWindow.show()

    app.exec_()