## ShapeWidget
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QTreeView, QDockWidget


def createDcokWindows(self):
    # table View
    dock = QDockWidget("Information", self)
    dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
    self.fileInfoTable = QTableWiew(dock)
    # 테이블 폰트를 설정한다.
    self.tableFont = QFont("Verdana", 8)
    self.fileinfoTable.setFont(self.tableFont)
    # 테이블 줄컬러를 설정한다.
    self.fileInfoTable.setAlternatingRowColors(True)
    self.fileInfoTable.setShowGrid(True)
    dock.setWidget(self.fileInfoTable)
    self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    # Tree View
    dock = QDockWidget("Structure", self)
    dock.setAllowedAreas(Qt.LeftDockWidgetArea |
                         Qt.RightDockWidgetArea)
    self.treefolder = QTreeView(dock)
    self.treeFolder.setAlternatingRowColors(True)
    dock.setWidget(self.treefolder)
    self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    # List View
    dock = QDockWidget("Debug & processing Log ...", self)
    dock.setAllowedAreas(Qt.LeftDockWidgetArea |
                         Qt.RightDockWidgetArea |
                         Qt.BottomDockWidgetArea)
    self.logInfo = QListWidget(dock)
    dock.setWidget(self.logInfo)
    self.addDockWidget(Qt.BottomDockWidgetArea, dock)