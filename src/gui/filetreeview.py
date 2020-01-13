#!interpreter [project-doozy]
# -*- coding: utf-8 -*-

"""
gui runcher
{License_info} 라이센스 정해야함
"""

# Built-in/Generic Imports
import sys

# Libs
from PySide2.QtWidgets import QTreeView, QAbstractItemView, QApplication, QFileSystemModel
from PySide2.QtCore import QFileInfo, QDir, QFile


class Tree(QTreeView):
    def __init__(self):
        QTreeView.__init__(self)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())

        self.setModel(self.model)
        self.setRootIndex(self.model.index(QDir.currentPath()))
        self.model.setReadOnly(False)

        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event):
        m = event.mimeData()
        if m.hasUrls():
            for url in m.urls():
                if url.isLocalFile():
                    event.accept()
                    return
        event.ignore()

    def dropEvent(self, event):
        if event.source():
            QTreeView.dropEvent(self, event)
        else:
            ix = self.indexAt(event.pos())
            if not self.model().isDir(ix):
                ix = ix.parent()
            pathDir = self.model().filePath(ix)
            m = event.mimeData()
            if m.hasUrls():
                urlLocals = [url for url in m.urls() if url.isLocalFile()]
                accepted = False
                for urlLocal in urlLocals:
                    path = urlLocal.toLocalFile()
                    info = QFileInfo(path)
                    n_path = QDir(pathDir).filePath(info.fileName())
                    o_path = info.absoluteFilePath()
                    if n_path == o_path:
                        continue
                    if info.isDir():
                        QDir().rename(o_path, n_path)
                    else:
                        qfile = QFile(o_path)
                        if QFile(n_path).exists():
                            n_path += "(copy)"
                        qfile.rename(n_path)
                    accepted = True
                if accepted:
                    event.acceptProposedAction()

    def change_root_index(self, path):
        self.setRootIndex(self.model.index(path))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = Tree()
    #mainWindow.resize(1200, 800)
    mainWindow.show()

    app.exec_()