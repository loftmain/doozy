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
import pandas as pd
from PySide2.QtCore import Slot, QDate
from PySide2.QtWidgets import (QApplication,  QPushButton,
                               QDialog, QHBoxLayout, QGroupBox,
                               QGridLayout, QLabel, QProgressBar,
                               QLineEdit, QFormLayout, QDateEdit)
# Own modules
from module.io import set_save_folder
from module.gathering_feature import Gathering_Feature

class IndiWidget(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('Independent Gathering')

        self.okButton = QPushButton("ok", self)
        self.okButton.clicked.connect(self.slot_clicked_ok_button)

        gb_0 = QGroupBox("gathering folder 이름 지정", self)
        self.folder_name = QLineEdit()
        self.folder_name.setPlaceholderText("independent")
        gb_layout_0 = QHBoxLayout(gb_0)
        gb_layout_0.addWidget(QLabel("폴더 이름 "))
        gb_layout_0.addWidget(self.folder_name)


        self.start_date = QLabel("경제지표 시작날짜: ", self)
        self.gathering_start_date = QDateEdit(self)
        self.gathering_start_date.setDate(QDate(2000, 1, 1))
        self.gathering_start_date.setDisplayFormat('yyyy-MM-dd')
        # self.de_train_start.setDate(QDate.currentDate())
        self.gathering_start_date.setCalendarPopup(True)

        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.help_layout = QGridLayout()

        self.inde_list = QLineEdit()
        self.private_key = QLineEdit()
        self.mainlayout = QFormLayout()
        self.mainlayout.addRow(QLabel("다운받을 경제지표 목록: "), self.inde_list)
        self.mainlayout.addRow(gb_0)

        self.mainlayout.addRow(self.start_date, self.gathering_start_date)
        self.mainlayout.setMargin(30)
        self.mainlayout.addRow(QLabel("private_key: "), self.private_key)
        self.mainlayout.addRow(self.progress)
        self.mainlayout.addRow(self.okButton)
        self.mainlayout.setVerticalSpacing(25)
        self.setLayout(self.mainlayout)

    @Slot(name="clickedOkButton")
    def slot_clicked_ok_button(self):
        """
        'OK' 버튼 클릭시 marking module에 전달되는 정보
        """
        self.progress.setMaximum(len(self.inde_list.text()))
        inde_list = [col.strip() for col in self.inde_list.text().split(',')]
        gathering_info = {
            "inde_list": inde_list,
            "folder_name": str(self.folder_name.text()),
            "gathering_start_date": str(self.gathering_start_date.text()),
            "private_key": self.private_key.text()
        }
        self.run_gathering(gathering_info)
        self.progress.setValue(len(self.inde_list.text()))

    def run_gathering(self, dic):

        gathering = Gathering_Feature()
        gathering.set_option(dic['inde_list'], dic['folder_name'],
                              dic['gathering_start_date'], dic['private_key'])
        gathering.gathering(os.curdir)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = IndiWidget()
    form.show()
    app.exec_()
