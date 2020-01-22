#!interpreter [project-doozy]
# -*- coding: utf-8 -*-

"""
gui runcher
{License_info} 라이센스 정해야함
"""

# Built-in/Generic Imports
import sys

from PySide2.QtCore import Slot, Qt
# Libs
from PySide2.QtWidgets import (QApplication, QWidget, QPushButton,
                               QVBoxLayout, QGroupBox, QLabel,
                               QFormLayout, QLineEdit, QGridLayout)

from src.gui.markingwidget import LineEdit
from src.module.backtesting import backtesting
from src.module.io import get_refined_path


class OrderRunWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('orderexcute')

        self.run_button = QPushButton("run", self)
        self.run_button.clicked.connect(self.slot_clicked_run_button)

        gb_1 = QGroupBox(self)
        gb1_layout = QGridLayout(gb_1)

        self.stock_name = QLineEdit()
        self.start_value = QLineEdit()

        gb1_layout.addWidget(QLabel('종목명: '), 0, 0, Qt.AlignRight)
        gb1_layout.addWidget(self.stock_name, 0, 1, Qt.AlignLeft)
        # gb1_layout.setHorizontalSpacing(25)
        gb1_layout.addWidget(QLabel('초기금액: '), 0, 2, Qt.AlignRight)
        gb1_layout.addWidget(self.start_value, 0, 3, Qt.AlignCenter)
        gb1_layout.addWidget(QLabel("만원"), 0, 4, Qt.AlignLeft)

        gb_2 = QGroupBox("경로 지정", self)
        formLayout = QFormLayout(gb_2)
        self.input_file_path = LineEdit()
        self.save_file_name = LineEdit()
        self.lb_info = QLabel("*drag in file view*")
        self.lb_info.setAlignment(Qt.AlignRight)
        formLayout.addRow(self.lb_info)
        formLayout.addRow(QLabel("order file path: "), self.input_file_path)
        formLayout.addRow(QLabel("save file name: "), self.save_file_name)

        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(gb_1)
        self.mainlayout.addWidget(gb_2)
        self.mainlayout.addStretch()
        self.mainlayout.addWidget(self.run_button)

        self.setLayout(self.mainlayout)

    @Slot(name="clickedRunButton")
    def slot_clicked_run_button(self):
        serial_info = {
            "order_file_path": get_refined_path(self.input_file_path.text()),
            "save_file_name": self.save_file_name.text(),
            'stock_name': self.stock_name.text(),
            'start_value': int(self.start_value.text()) * 10000
        }
        print(serial_info)
        backtesting(serial_info)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = OrderRunWidget()
    form.show()
    app.exec_()