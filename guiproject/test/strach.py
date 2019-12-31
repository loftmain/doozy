import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit ,QWidget
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl

class Screen(QWidget):
    def __init__(self):
        super(Screen, self).__init__()
        self.setLayout(QVBoxLayout())

        widget1 = QPushButton("Text1", self)
        widget3 = QLabel("Text3", self)

        self.widget2_layout = QHBoxLayout()
        self.change_widget2()

        self.layout().addWidget(widget1)
        self.layout().addLayout(self.widget2_layout)
        self.layout().addWidget(widget3)

        widget1.clicked.connect(self.change_widget2)

    def clearLayout(self, layout):
        item = layout.takeAt(0)
        while item:
            w = item.widget()
            if w:
                w.deleteLater()
            lay = item.layout()
            if lay:
                self.clearLayout(item.layout())
            item = layout.takeAt(0)

    def change_widget2(self):
        self.clearLayout(self.widget2_layout)

        # change the widget.
        import random
        widgets = [QLabel, QLineEdit, QPushButton]
        widget2 = widgets[random.randint(0, len(widgets)-1)]("widget2", self)

        self.widget2_layout.addWidget(widget2)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QPushButton
    from PyQt5.QtWidgets import QTextEdit
    app = QApplication(sys.argv)
    excepthook = sys.excepthook
    sys.excepthook = lambda t, val, tb: excepthook(t, val, tb)
    form = Screen()
    form.show()
    exit(app.exec_())