import sys

from PySide2.QtWidgets import (QApplication, QWidget, QPushButton,
                                QVBoxLayout, QGroupBox, QLabel,
                               QFormLayout)
from PySide2.QtCore import Slot, Qt
from labelingoption import LineEdit

class OrderRunWidget(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setWindowTitle('orderexcute')


        self.run_button = QPushButton("run", self)
        self.run_button.clicked.connect(self.slot_clicked_run_button)


        gb_3 = QGroupBox("경로 지정", self)
        formLayout = QFormLayout(gb_3)
        self.dependent_file_path = LineEdit()
        self.independent_file_path = LineEdit()
        self.lb_info = QLabel("*drag in file view*")
        self.lb_info.setAlignment(Qt.AlignRight)
        formLayout.addRow(self.lb_info)
        formLayout.addRow(QLabel("order file path: "), self.dependent_file_path)
        formLayout.addRow(QLabel("saved folder path: "), self.independent_file_path)





        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(gb_3)
        self.mainlayout.addStretch()
        self.mainlayout.addWidget(self.run_button)

        self.setLayout(self.mainlayout)

    @Slot(name="clickedRunButton")
    def slot_clicked_run_button(self):
        serial_info = {
            "order_file_path": self.dependent_file_path.text(),
            "saved_folder_path": self.independent_file_path.text()
        }
        print(serial_info)
        #.currentText()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = OrderRunWidget()
    form.show()
    app.exec_()