#!interpreter [project-doozy]
# -*- coding: utf-8 -*-
#
# Copyright 2019 doozy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Built-in/Generic Imports
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "\\..\\"))

# Libs
import PySide2
from PySide2.QtCore import QEventLoop, QSettings
from PySide2.QtCore import Qt
from PySide2.QtGui import QTextCursor, QIcon
from PySide2.QtWidgets import (QDockWidget, QTabWidget, QTextBrowser, QFileDialog \
    , QMainWindow, QAction, QLabel, QMessageBox)

# Own modules
from .download import DlIndependentDialog
from .filetreeview import Tree
from .markingwidget import MarkingWidget
from .modelingoption import ModelingOption
from .orderexcute import OrderRunWidget
from .orderwidget import CreateOrderWidget
from .output import StdoutRedirect
from .visual import PlotWidget
from .indewidget import IndiWidget
from .targetwidget import TargetWidget
from .normalwiget import NormalWidget

__author__ = 'jinjae lee'
__copyright__ = 'Copyright 2020, doozy'
__credits__ = ['loftmain']
__license__ = '{license}'
__version__ = '0.0.1'
__maintainer__ = 'jinjae lee'
__email__ = 'leejinjae7@gmail.com'
__status__ = 'Dev'

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class MainWindow(QMainWindow):
    """
    MainWindow는 Gui시작할 때 나오는 첫 화면의 구성을 담당합니다.
    메뉴의 구성은 "Project, File, View, Marking, Modeling, Simulation, Visualization"으로 되어있습니다.
    Project: 자신이 원하는 프로젝트를 지정(폴더단위)
    FIle: 경제지표 download
    View: filesystem treeview와 하단 log view를 끄거나 킬수 있음
    Marking: 주가 데이터 파일에 예측을 원하는 signal을 추가합니다.
    Modeling: 경제지표파일들을 가지고 주가 signal을 예측하고 backtesting할 order file을 생성합니다.
    Simulation: order 전략을 토대로 backtesting합니다.
    Visualization: backtesting한 결과를 시각화합니다.

    진행간의 파일들은 csv 형식을 사용해야합니다.
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

        # Debug & Processing Log text output dock
        self.logDock = QDockWidget("Debug & Processing Log ...", self)
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

    def createActions(self):
        """
        메인 window 메뉴의 내부 항목 action 들을 추가합니다.
        """
        # Project Menu
        self.newProject = QAction("&New Project", self)
        self.newProject.setShortcut("Ctrl+N")
        self.newProject.setStatusTip("create a new project")
        self.newProject.triggered.connect(self.load_folder)

        self.openProject = QAction("&Open Project", self)
        self.openProject.setShortcut("Ctrl+O")
        self.openProject.setStatusTip("Open a project in treeview")
        self.openProject.triggered.connect(self.load_folder)

        # File Menu
        self.saveDataAction = QAction("&지표 데이터 파일저장", self)
        self.saveDataAction.setStatusTip("import files")
        self.saveDataAction.triggered.connect(self.dl_independents)

        self.savedeDataAction = QAction("&주가 데이터 파일저장", self)
        self.savedeDataAction.setStatusTip("import files")
        self.savedeDataAction.triggered.connect(self.dl_dependents)

        self.normalDataAction = QAction("&데이터 정규화", self)
        self.normalDataAction.setStatusTip("Data Normalization")
        self.normalDataAction.triggered.connect(self.createNormalTab)

        self.exitAction = QAction("&Exit", self)
        self.exitAction.setIcon(QIcon(":/images/exit.png"))
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip("Exit the application")
        self.exitAction.triggered.connect(self.close)

        # view menu
        self.fileViewAction = QAction("&File system view", self, checkable=True)
        # self.triangleAction.setShortcut("Ctrl+T")
        self.fileViewAction.setStatusTip("toggle File system view")
        self.fileViewAction.setChecked(True)
        self.fileViewAction.triggered.connect(self.toggleFileView)

        self.logViewAction = QAction("&System log view", self, checkable=True)
        # self.rectangleAction.setShortcut("Ctrl+R")
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

        # Simulation menu
        self.orderexcuteAction = QAction("&order excute", self)
        self.orderexcuteAction.setStatusTip("order excute")
        self.orderexcuteAction.triggered.connect(self.createOrderExecuteTab)

        # visualization menu
        self.chartAction = QAction("&단일 그래프 chart", self)
        self.chartAction.setStatusTip("단일 그래프 chart")
        self.chartAction.triggered.connect(self.createPlotTab)

    def createMenus(self):
        """
        window 상단 메뉴바에 메뉴들을 추가합니다.
        """

        projectMenu = self.menuBar().addMenu("&Project")
        projectMenu.addAction(self.newProject)
        projectMenu.addAction(self.openProject)
        projectMenu.addAction(self.exitAction)

        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.saveDataAction)
        fileMenu.addAction(self.savedeDataAction)
        fileMenu.addAction(self.normalDataAction)

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

    def createStatusBar(self):
        """
        기능 미구현
        :return:
        """
        locationLabel = QLabel(" (  0,  0) ")
        locationLabel.setAlignment(Qt.AlignHCenter)
        locationLabel.setMinimumSize(locationLabel.sizeHint())

        # shapeWidget.mousePositionChanged(str) - QLabel.setText(str)

        self.statusBar().addWidget(locationLabel)

    def readSettings(self):
        settings = QSettings("doozy", "Shape")

        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("state"))

    def writeSettings(self):
        settings = QSettings("doozy Inc.", "Shape")

        self.saveGeometry()
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())

    # event
    def closeEvent(self, event):
        self.writeSettings()

    # slot
    def load_folder(self):
        """
        Treeview의 기본 Root 설정
        """
        self.path_to_file = QFileDialog.getExistingDirectory(self, self.tr("Load folder"), self.tr("~/Desktop/"),
                                                             QFileDialog.ShowDirsOnly
                                                             | QFileDialog.DontResolveSymlinks)
        print(self.path_to_file)
        self.treeview_widget.change_root_index(self.path_to_file)
        os.chdir(self.path_to_file)

    def dl_independents(self):
        """
        경제 지표 저장하는 window를 실행합니다.
        """
        #dlg = DlIndependentDialog(os.curdir)
        dlg = IndiWidget()
        dlg.exec_()

    def dl_dependents(self):
        """
        경제 지표 저장하는 window를 실행합니다.
        """
        #dlg = DlIndependentDialog(os.curdir)
        dlg = TargetWidget()
        dlg.exec_()

    def _append_text(self, msg):
        """
        텍스트 추가부
        """
        self.textBrowser.moveCursor(QTextCursor.End)
        self.textBrowser.insertPlainText(msg)
        # refresh textedit show, refer) https://doc.qt.io/qt-5/qeventloop.html#ProcessEventsFlag-enum
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def createNormalTab(self):
        widget = NormalWidget()
        self.tabWidget.addTab(widget, "Normalization")

    def createLabelTab(self):
        widget = MarkingWidget()
        """
        # 디버깅용
        widget.destroyed.connect(
            lambda obj: print(
                "deleted {}, count: {}".format(obj, self.tabWidget.count())
            )
        )
        """
        self.tabWidget.addTab(widget, "Marking")

    def createModelOptionTab(self):
        widget = ModelingOption()
        self.tabWidget.addTab(widget, "modeling option setting")

    def createOrderTab(self):
        widget = CreateOrderWidget()
        self.tabWidget.addTab(widget, "order create")

    def createOrderExecuteTab(self):
        widget = OrderRunWidget()
        self.tabWidget.addTab(widget, "order execute")

    def createPlotTab(self):
        widget = PlotWidget()
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
