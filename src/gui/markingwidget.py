#!interpreter [project-doozy]
# -*- coding: utf-8 -*-

"""
gui runcher
{License_info} 라이센스 정해야함
"""

import os
# Built-in/Generic Imports
import sys

import pandas as pd
from PySide2.QtCore import Slot
# Libs
from PySide2.QtWidgets import (QApplication, QWidget, QPushButton,
                               QVBoxLayout, QHBoxLayout, QGroupBox,
                               QGridLayout, QLabel, QComboBox, QSpinBox,
                               QLineEdit, QFormLayout, QRadioButton)

from src.module.marking import Marking


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


class MarkingWidget(QWidget):
    def __init__(self, path):
        QWidget.__init__(self)
        self.path = path
        self.setWindowTitle('create Label')

        self.okButton = QPushButton("ok", self)
        self.okButton.clicked.connect(self.slot_clicked_ok_button)

        gb_0 = QGroupBox("label 이름지정", self)
        self.te_label_name = QLineEdit()
        self.te_label_name.setPlaceholderText("ex) HM%UP, LM%DN")
        gb_layout_0 = QHBoxLayout(gb_0)
        gb_layout_0.addWidget(QLabel("label name: "))
        gb_layout_0.addWidget(self.te_label_name)

        self.bt_0 = QRadioButton("한달간")
        self.bt_0.toggled.connect(self.one_monthly_clicked)
        self.bt_1 = QRadioButton("월간")
        self.bt_1.toggled.connect(self.several_monthly_clicked)

        self.gb_1 = QGroupBox("label 범위", self)
        gb_layout_1 = QHBoxLayout()
        gb_layout_1.addWidget(self.bt_0)
        gb_layout_1.addWidget(self.bt_1)
        self.gb_Layout_0 = QVBoxLayout(self.gb_1)
        self.gb_Layout_0.addLayout(gb_layout_1)

        self.help_layout = QGridLayout()

        self.file_name = LineEdit()
        self.save_name = LineEdit()
        self.save_name.setPlaceholderText("sample.csv")
        self.mainlayout = QFormLayout()
        self.mainlayout.addRow(QLabel("file name(Drag in file view): "), self.file_name)
        self.mainlayout.addRow(gb_0)
        self.mainlayout.addRow(self.gb_1)
        self.mainlayout.setMargin(30)
        self.mainlayout.addRow(QLabel("save file name: "), self.save_name)
        self.mainlayout.addRow(self.okButton)
        self.mainlayout.setVerticalSpacing(25)
        self.setLayout(self.mainlayout)

    def one_monthly_clicked(self):
        if self.bt_0.isChecked():
            self.firstIndexSpinBox = QSpinBox(self)
            self.firstIndexSpinBox.setValue(0)
            self.firstIndexSpinBox.setMinimum(0)
            self.firstIndexSpinBox.setMaximum(5)

            self.secondIndexSpinBox = QSpinBox(self)
            self.secondIndexSpinBox.setValue(0)
            self.secondIndexSpinBox.setMinimum(0)
            self.secondIndexSpinBox.setMaximum(5)

            self.firstColumnComboBox = QComboBox(self)
            self.secondColumnComboBox = QComboBox(self)
            self._fill_columns_info()
            self.sb_per = QSpinBox(self)
            self.sb_per.setMinimum(-10)
            self.cb_updown = QComboBox(self)
            self.cb_updown.addItems(["up", "down"])  # 다수 아이템 추가시
            self.help_layout.addWidget(QLabel("한달간 Open가에서 "), 0, 1)
            self.help_layout.addWidget(self.secondColumnComboBox, 0, 2)
            self.help_layout.addWidget(QLabel("가 대비"), 0, 3)
            self.help_layout.addWidget(self.sb_per, 0, 4)
            self.help_layout.addWidget(QLabel('%'), 0, 5)
            self.help_layout.addWidget(self.cb_updown, 0, 6)

            self.gb_Layout_0.addLayout(self.help_layout)

        else:
            self.clearLayout(self.help_layout)

    def several_monthly_clicked(self):
        if self.bt_1.isChecked():
            self.firstIndexSpinBox = QSpinBox(self)
            self.firstIndexSpinBox.setValue(0)
            self.firstIndexSpinBox.setMinimum(-5)
            self.firstIndexSpinBox.setMaximum(5)

            self.secondIndexSpinBox = QSpinBox(self)
            self.secondIndexSpinBox.setValue(0)
            self.secondIndexSpinBox.setMinimum(-4)
            self.secondIndexSpinBox.setMaximum(5)

            self.firstColumnComboBox = QComboBox(self)
            self.secondColumnComboBox = QComboBox(self)
            self._fill_columns_info()

            self.sb_per = QSpinBox(self)
            self.sb_per.setMinimum(-10)
            self.cb_updown = QComboBox(self)
            self.cb_updown.addItems(["up", "down"])  # 다수 아이템 추가시

            self.help_layout.addWidget(QLabel("현재"), 0, 0)
            self.help_layout.addWidget(self.firstIndexSpinBox, 0, 1)
            self.help_layout.addWidget(QLabel("월을 기준으로 "), 0, 2)
            self.help_layout.addWidget(self.firstColumnComboBox, 0, 3)
            self.help_layout.addWidget(QLabel("가에서 "), 0, 4)
            self.help_layout.addWidget(self.secondIndexSpinBox, 1, 0)
            self.help_layout.addWidget(QLabel("달 뒤에 "), 1, 1)
            self.help_layout.addWidget(self.secondColumnComboBox, 1, 2)
            self.help_layout.addWidget(QLabel("가 대비"), 1, 3)
            self.help_layout.addWidget(self.sb_per, 2, 0)
            self.help_layout.addWidget(QLabel('%'), 2, 1)
            self.help_layout.addWidget(self.cb_updown, 2, 2)

            self.gb_Layout_0.addLayout(self.help_layout)

        else:
            self.clearLayout(self.help_layout)

    def _fill_columns_info(self):
        cloumn_name = ["Open", "High", "Low", "Close"]
        self.firstColumnComboBox.insertItems(0, [x for x in cloumn_name])
        self.secondColumnComboBox.insertItems(0, [x for x in cloumn_name])

    @Slot(name="clickedOkButton")
    def slot_clicked_ok_button(self):
        marking_info = {
            "file_root": str(self.file_name.text()),
            "base_index": str(self.firstIndexSpinBox.value()),
            "base_column": str(self.firstColumnComboBox.currentText()),
            "compare_index": str(self.secondIndexSpinBox.value()),
            "compare_column": str(self.secondColumnComboBox.currentText()),
            "per": str(self.sb_per.value() * 0.01),
            "updown": str(self.cb_updown.currentText()),
            "name": str(self.te_label_name.text()),
            "save_name": self.save_name.text()
        }
        print(marking_info)
        self.run_markiing(marking_info)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def run_markiing(self, dic):
        if not os.path.exists(os.path.join(self.path, 'save')):
            os.mkdir(os.path.join(self.path, 'save'))
        save_path = os.path.join(self.path, 'save')
        if not os.path.exists(os.path.join(save_path, 'marking')):
            os.mkdir(os.path.join(save_path, 'marking'))
        save_path = os.path.join(save_path, 'marking')
        df = pd.read_csv(dic["file_root"])
        mark = Marking()
        mark.set_option(df, [dic["compare_index"], dic["base_index"], dic["per"]],
                        [dic["compare_column"], dic['base_column'], dic["name"]], dic["updown"])
        result = mark.create_label()
        result.to_csv(save_path + '\\' + dic["save_name"], header=True, index=False, encoding='ms949')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MarkingWidget(os.path.curdir)
    form.show()
    app.exec_()