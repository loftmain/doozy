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
import sys
# Libs
from PySide2.QtCore import QFileInfo, QDir, QFile
from PySide2.QtWidgets import QTreeView, QAbstractItemView, QApplication, QFileSystemModel


class Tree(QTreeView):
    """
    Treeview file system UI
    default path: 실행시 current directory
    """

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
        """
        파일을 drag 할 수 있게 함
        """
        m = event.mimeData()
        if m.hasUrls():
            for url in m.urls():
                if url.isLocalFile():
                    event.accept()
                    return
        event.ignore()

    def dropEvent(self, event):
        """
        drag 한 파일의 경로를 output합니다.
        """

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
        """
        프로젝트를 바꿀시에 경로를 반영합니다.
        """

        self.setRootIndex(self.model.index(path))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = Tree()
    mainWindow.show()

    app.exec_()