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
import os
import sys

# Libs
from PySide2.QtCore import Slot, QDate
from PySide2.QtWidgets import (QApplication, QDialog, QPushButton,
                               QHBoxLayout, QGroupBox, QGridLayout,
                               QLabel, QLineEdit, QFormLayout, QDateEdit,
                               QRadioButton, QProgressBar)

# Own modules
from src.module.gathering_target import Gathering_target


class TargetWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('target Gathering')

        self.okButton = QPushButton("ok", self)
        self.okButton.clicked.connect(self.slot_clicked_ok_button)

        gb_0 = QGroupBox("gathering folder 이름 지정", self)
        self.folder_name = QLineEdit()
        self.folder_name.setPlaceholderText("dependent")
        gb_layout_0 = QHBoxLayout(gb_0)
        gb_layout_0.addWidget(QLabel("폴더 이름 "))
        gb_layout_0.addWidget(self.folder_name)

        self.start_date = QLabel("주가 시작날짜: ", self)
        self.gathering_start_date = QDateEdit(self)
        self.gathering_start_date.setDate(QDate(2000, 1, 1))
        self.gathering_start_date.setDisplayFormat('yyyy-MM-dd')
        # self.de_train_start.setDate(QDate.currentDate())
        self.gathering_start_date.setCalendarPopup(True)

        datareaderBox = QGroupBox("datareader 설정", self)
        self.pdrButton = QRadioButton("pandas datareader", datareaderBox)
        self.fdrButton = QRadioButton("finance datareader", datareaderBox)
        self.pdrButton.setChecked(True)
        self.dopt = 'PDR'
        groupBoxLayout = QHBoxLayout(datareaderBox)
        groupBoxLayout.addWidget(self.pdrButton)
        groupBoxLayout.addWidget(self.fdrButton)
        self.pdrButton.toggled.connect(self.drClicked)
        self.fdrButton.toggled.connect(self.drClicked)

        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.help_layout = QGridLayout()

        self.depend_list = QLineEdit()
        self.depend_list.setPlaceholderText("ex) ^DJI")
        self.mainlayout = QFormLayout()
        self.mainlayout.addRow(QLabel("다운받을 주가 코드: "), self.depend_list)
        self.mainlayout.addRow(gb_0)

        self.mainlayout.addRow(self.start_date, self.gathering_start_date)
        self.mainlayout.setMargin(30)
        self.mainlayout.addRow(datareaderBox)
        self.mainlayout.addRow(self.progress)
        self.mainlayout.addRow(self.okButton)
        self.mainlayout.setVerticalSpacing(25)
        self.setLayout(self.mainlayout)

    def drClicked(self):
        if self.pdrButton.text() == "pandas datareader":
            self.dopt = 'PDR'
        if self.fdrButton.text() == "finance datareader":
            self.dopt = 'FDR'

    @Slot(name="clickedOkButton")
    def slot_clicked_ok_button(self):
        """
        'OK' 버튼 클릭시 marking module에 전달되는 정보
        """
        self.progress.setMaximum(len(self.depend_list.text()))

        gathering_info = {
            "depend_list": str(self.depend_list.text()),
            "folder_name": str(self.folder_name.text()),
            "gathering_start_date": str(self.gathering_start_date.text()),
            "datareader": str(self.dopt)
        }
        self.run_gathering(gathering_info)
        self.progress.setValue(len(self.depend_list.text()))

    def run_gathering(self, dic):

        gathering = Gathering_target()
        gathering.set_option(dic['depend_list'], dic['folder_name'],
                             dic['gathering_start_date'], dic['datareader'])
        gathering.gathering(os.curdir)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = TargetWidget()
    form.show()
    app.exec_()
