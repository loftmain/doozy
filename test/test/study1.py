from PySide2.QtCore import QUrl
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QApplication

app = QApplication([])
view = QQuickView()
url = QUrl("view.qml")

view.setSource(url)
view.show()
app.exec_()
