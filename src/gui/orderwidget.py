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
                               QFormLayout, QRadioButton, QSpinBox, QHBoxLayout)

from src.gui.markingwidget import LineEdit
from src.module.createorder import run_create_order


class CreateOrderWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('orderexcute')

        self.run_button = QPushButton("run", self)
        self.run_button.clicked.connect(self.slot_clicked_run_button)

        gb_1 = QGroupBox("create order", self)
        formLayout = QFormLayout(gb_1)
        self.dependent_file_path = LineEdit()
        self.column_name = LineEdit()
        self.column_name.setPlaceholderText("predicted column 이름을 적어주세요.")
        self.yahoo_index = LineEdit()
        self.yahoo_index.setPlaceholderText("야후 stock에서 사용되는 종목 코드를 적어주세요.")
        self.lb_info = QLabel("*drag in file view*")
        self.lb_info.setAlignment(Qt.AlignRight)
        formLayout.addRow(self.lb_info)
        formLayout.addRow(QLabel("order file path: "), self.dependent_file_path)
        formLayout.addRow(QLabel("column name: "), self.column_name)
        formLayout.addRow(QLabel("yahoo stock 종목 코드: "), self.yahoo_index)

        gb_2 = QGroupBox("전략선택", self)
        self.rb_1 = QRadioButton('HMBS: 예측한 mark가 1일 때, 월초 매수하여 월중 n%상승 등장일에 매도')
        self.rb_2 = QRadioButton('HMBLS: 예측한 mark가 1일 때, 월초 매수하여 월말에 매도')
        self.rb_3 = QRadioButton('LMBS: 예측한 mark가 0일 때, 월초 매수하여 월중 n%상승 등장일에 매도')
        self.rb_4 = QRadioButton('LMBNS: 예측한 mark가 0일 때, 월초 매수하여 월말에 매도')
        self.rb_layout = QVBoxLayout(gb_2)
        self.rb_layout.addWidget(self.rb_1)
        self.rb_layout.addWidget(self.rb_2)
        self.rb_layout.addWidget(self.rb_3)
        self.rb_layout.addWidget(self.rb_4)

        gb_3 = QGroupBox("퍼센트", self)
        self.sb_per = QSpinBox(self)
        self.sb_per.setMinimum(-10)
        gb_Layout_2 = QHBoxLayout(gb_3)
        gb_Layout_2.addWidget(self.sb_per)
        gb_Layout_2.addWidget(QLabel("%", self))

        gb_4 = QGroupBox('save', self)
        formLayout4 = QFormLayout(gb_4)
        self.save_file_name = LineEdit()
        self.save_file_name.setPlaceholderText("ex) sample.csv")
        formLayout4.addRow(QLabel('save file name: '), self.save_file_name)

        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(gb_1)
        self.mainlayout.addWidget(gb_2)
        self.mainlayout.addWidget(gb_3)
        self.mainlayout.addWidget(gb_4)
        self.mainlayout.addStretch()
        self.mainlayout.addWidget(self.run_button)
        self.mainlayout.setMargin(30)
        self.setLayout(self.mainlayout)

    def rb_clicked(self):
        if self.rb_1.isChecked():
            return self.rb_1.text().split(':')[0]
        elif self.rb_2.isChecked():
            return self.rb_2.text().split(':')[0]
        elif self.rb_3.isChecked():
            return self.rb_3.text().split(':')[0]
        elif self.rb_4.isChecked():
            return self.rb_4.text().split(':')[0]
        else:
            print("ERROR: radio button is unchecked")

    @Slot(name="clickedRunButton")
    def slot_clicked_run_button(self):
        dependent_file_path = self.dependent_file_path.text().split('file://')[1]
        setting_info = {
            "order_file_path": dependent_file_path,
            "column_name": self.column_name.text(),
            "yahoo_code": self.yahoo_index.text(),
            "strategy": self.rb_clicked(),
            "per": 0.01 * int(self.sb_per.text()),
            "save_name": self.save_file_name.text()
        }
        print(setting_info)
        run_create_order(setting_info)
        print('order create OK!')
        # .currentText()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CreateOrderWidget()
    form.show()
    app.exec_()
