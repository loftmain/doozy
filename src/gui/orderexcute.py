#!interpreter [project-doozy]
# -*- coding: utf-8 -*-

"""
gui1 runcher
{License_info} 라이센스 정해야함
"""

# Built-in/Generic Imports
import sys
import os

from PySide2.QtCore import Slot, Qt
# Libs
from PySide2.QtWidgets import (QApplication, QWidget, QPushButton,
                               QVBoxLayout, QGroupBox, QLabel, QComboBox,
                               QFormLayout, QLineEdit, QGridLayout)

from gui.markingwidget import LineEdit
from module.tradesimulator import backtesting
from module.io import get_refined_path
from module.transform_order import run_transform_order
from module.simulator import run_simulator

class OrderRunWidget(QWidget):
    """

    """

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('orderexcute')

        self.run_button = QPushButton("run", self)
        self.run_button.clicked.connect(self.slot_clicked_run_button)

        gb_1 = QGroupBox(self)
        gb1_layout = QGridLayout(gb_1)

        self.etf_code = QLineEdit()
        self.etf_name = QLineEdit()
        self.start_money = QLineEdit()


        gb1_layout.addWidget(QLabel('ETF 종목 코드: '), 0, 0, Qt.AlignRight)
        gb1_layout.addWidget(self.etf_code, 0, 1, Qt.AlignLeft)
        # gb1_layout.setHorizontalSpacing(25)
        gb1_layout.addWidget(QLabel('ETF 종목 이름: '), 0, 2, Qt.AlignRight)
        gb1_layout.addWidget(self.etf_name, 0, 3, Qt.AlignCenter)
        gb1_layout.addWidget(QLabel('초기금액: '), 1, 0, Qt.AlignRight)
        gb1_layout.addWidget(self.start_money, 1, 1, Qt.AlignLeft)

        gb_2 = QGroupBox("경로 지정", self)
        formLayout = QFormLayout(gb_2)
        self.input_file_path = LineEdit()
        self.save_file_name = LineEdit()
        self.lb_info = QLabel("*drag in file view*")
        self.lb_info.setAlignment(Qt.AlignRight)
        formLayout.addRow(self.lb_info)
        formLayout.addRow(QLabel("order file path: "), self.input_file_path)
        formLayout.addRow(QLabel("save folder name: "), self.save_file_name)

        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(gb_1)
        self.mainlayout.addWidget(gb_2)
        self.mainlayout.addStretch()
        self.mainlayout.addWidget(self.run_button)

        self.setLayout(self.mainlayout)

    @Slot(name="clickedRunButton")
    def slot_clicked_run_button(self):
        serial_info = {
            "sim_file_path": get_refined_path(self.input_file_path.text()),
            "save_folder_name": self.save_file_name.text(),
            'etf_code': self.etf_code.text(),
            'etf_name': self.etf_name.text(),
            'starting_money' : int(self.start_money.text()),
            'path': os.curdir
        }
        print(serial_info)
        run_transform_order(serial_info)
        run_simulator(serial_info)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = OrderRunWidget()
    form.show()
    app.exec_()
