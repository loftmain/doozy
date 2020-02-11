import sys

from PySide2.QtCore import *
from PySide2.QtWidgets import *


class Tree(QTreeView):
    def __init__(self):
        QTreeView.__init__(self)
        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())

        self.setModel(model)
        self.setRootIndex(model.index(QDir.currentPath()))
        model.setReadOnly(False)

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

class combo(QComboBox):

    def __init__(self, title, parent):
        super(combo, self).__init__(parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print(e)

        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.addItem(e.mimeData().text())

class LineEdit(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print(e)

        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        lo = QFormLayout()
        lo.addRow(QLabel("Type some text in textbox and drag it into combo box"))

        edit = LineEdit()
        edit.setDragEnabled(True)
        com = Tree()
        lo.addRow(edit, com)
        self.setLayout(lo)
        self.setWindowTitle('Simple drag & drop')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()


if __name__ == '__main__':
    main()