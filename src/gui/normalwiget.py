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
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (QApplication, QWidget, QPushButton,
                               QRadioButton, QVBoxLayout, QLineEdit,
                               QHBoxLayout, QGroupBox, QGridLayout,
                               QLabel, QComboBox, QFormLayout, QDateEdit)
from module.classifier import run_modeling
from module.io import set_save_folder

# Own modules
from gui.markingwidget import LineEdit
from module.normalizing_data import Normalization

class NormalWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Button Demo')

        self.okButton = QPushButton("ok", self)
        self.okButton.clicked.connect(self.slot_clicked_ok_button)

        normalizationBox = QGroupBox("정규화 선택", self)
        self.rateButton = QRadioButton("Rate", normalizationBox)
        self.logexpButton = QRadioButton("Log and Exp", normalizationBox)
        self.customButton = QRadioButton("User Customizing", normalizationBox)
        self.multicustomButton = QRadioButton("Multi User Customizing", normalizationBox)

        self.folder_name = LineEdit()

        groupBoxLayout2 = QHBoxLayout(normalizationBox)
        groupBoxLayout2.addWidget(self.rateButton)
        groupBoxLayout2.addWidget(self.logexpButton)
        groupBoxLayout2.addWidget(self.customButton)
        groupBoxLayout2.addWidget(self.multicustomButton)
        self.rateButton.toggled.connect(self.rateClicked)
        self.logexpButton.toggled.connect(self.logexpClicked)
        self.customButton.toggled.connect(self.customClicked)
        self.multicustomButton.toggled.connect(self.multiCustomClicked)


        self.gb = QGroupBox(self.tr("정규화 설명 및 사용자 커스터마이즈"))
        self.grid_box = QGridLayout()

        hb_2 = QHBoxLayout()
        hb_2.addWidget(QLabel("folder name(Drag in file view): "))
        hb_2.addWidget(self.folder_name)
        hb_3 = QHBoxLayout()

        self.mainlayout = QVBoxLayout()
        self.mainlayout.addLayout(hb_2)
        self.mainlayout.addWidget(normalizationBox)
        self.mainlayout.addWidget(self.gb)

        self.mainlayout.addSpacing(15)

        self.mainlayout.addLayout(hb_3)
        self.mainlayout.addStretch()
        self.mainlayout.setMargin(30)
        self.mainlayout.addWidget(self.okButton)

        self.setLayout(self.mainlayout)

    def rateClicked(self):
        """
        Random Forest Radio Button 을 클릭시 나오는 UI
        """
        if self.rateButton.text() == "Rate":
            if self.rateButton.isChecked():

                self.grid_box.addWidget(
                    QLabel(self.tr("지표데이터의 변화율을 나타내는 rate를 얻을 수 있습니다.")), 0, 0)

                self.gb.setLayout(self.grid_box)

                self.update()
            else:
                self.clearLayout(self.grid_box)
                self.update()

    def logexpClicked(self):
        """
        K-NN Radio Button 을 클릭시 나오는 UI
        """
        if self.logexpButton.text() == "Log and Exp":
            if self.logexpButton.isChecked():
                self.grid_box.addWidget(QLabel(
                    self.tr("지표데이터에 Log와 Exp를 사용한 값을 얻을 수 있습니다.")), 0, 0)

                self.gb.setLayout(self.grid_box)
                self.update()
            else:
                self.clearLayout(self.grid_box)
                self.update()

    def customClicked(self):
        """
        K-NN Radio Button 을 클릭시 나오는 UI
        """
        if self.customButton.text() == "User Customizing":
            if self.customButton.isChecked():
                self.grid_box.addWidget(QLabel(
                    self.tr("사용자가 원하는 정규화식을 직접 입력할 수 있습니다.")), 0, 0)
                self.grid_box.addWidget(QLabel(
                    self.tr("데이터는 df[tag]라는 이름으로 통일합니다.")), 1, 0)
                self.grid_box.addWidget(QLabel(
                    self.tr("예시) df[tag] * 100")), 2, 0)
                self.grid_box.addWidget(QLabel(
                    self.tr("사용자 정의 정규화식을 입력한다. 위는 단순히 데이터에 100을 곱한 것이다.")), 3, 0)
                self.save_name = LineEdit()
                self.grid_box.addWidget(self.save_name, 4, 0)

                self.gb.setLayout(self.grid_box)
                self.update()
            else:
                self.clearLayout(self.grid_box)
                self.update()

    def multiCustomClicked(self):
        """
        K-NN Radio Button 을 클릭시 나오는 UI
        """
        if self.multicustomButton.text() == "Multi User Customizing":
            if self.multicustomButton.isChecked():
                self.grid_box.addWidget(QLabel(
                    self.tr("사용자가 원하는 정규화식을 직접 여러개 입력할 수 있습니다.")), 0, 0)
                self.grid_box.addWidget(QLabel(
                    self.tr("데이터는 df[tag]라는 이름으로 통일합니다. \n"
                            "df['나만의정규화데이터'] = df[tag] * 100 - 1과 같이 \n"
                            "equal까지 모두 기입한다. 여러줄을 입력하여도 상관없다. \n"
                            "파이썬 스타일 문법이라면 모두 적용된다.")), 1, 0)

                self.grid_box.addWidget(QLabel(
                    self.tr("예시) df['example'] = df[tag] * 100")), 2, 0)
                self.grid_box.addWidget(QLabel(
                    self.tr("사용자 정의 정규화식을 입력한다. 위는 단순히 데이터에 100을 곱한 것이다.")), 3, 0)
                self.save_name = LineEdit()
                self.grid_box.addWidget(self.save_name, 4, 0)

                self.gb.setLayout(self.grid_box)
                self.update()
            else:
                self.clearLayout(self.grid_box)
                self.update()

    def clicked_all(self):
        """
        독립변수 설정 -> 독립변수 조합을 이용 Radio 버튼을 클릭시 나오는 UI
        """
        if self.bt_all.isChecked():
            self.startNum = QComboBox()
            self.startNum.insertItems(0, [str(x) for x in range(10)])
            self.endNum = QComboBox()
            self.endNum.insertItems(0, [str(x) for x in range(10)])
            self.groupBoxLayout3 = QHBoxLayout()
            self.groupBoxLayout3.addWidget(self.startNum)
            self.groupBoxLayout3.addWidget(QLabel(self.tr("            ~")))
            self.groupBoxLayout3.addWidget(self.endNum)
            self.gb_layout3.addLayout(self.groupBoxLayout3)
        else:
            self.clearLayout(self.groupBoxLayout3)

    def clicked_subset(self):
        """
        독립변수 설정 -> 지정 독립변수 사용 Radio 버튼을 클릭시 나오는 UI
        """
        if self.bt_subset.isChecked():
            self.le_column_list = QLineEdit()
            self.le_column_list.setText("column1, column2, column3")
            self.groupBoxLayout3 = QHBoxLayout()
            self.groupBoxLayout3.addWidget(QLabel(self.tr("column list")))
            self.groupBoxLayout3.addWidget(self.le_column_list)
            self.gb_layout3.addLayout(self.groupBoxLayout3)
        else:
            self.clearLayout(self.groupBoxLayout3)

    def clearLayout(self, layout):
        """
        다른 Radio 벼튼을 눌렀을시 기존 정보들을 Clear 해주는 역할
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    @Slot(name="clickedOkButton")
    def slot_clicked_ok_button(self):
        """
        OK button 눌렀을 시 프로그램에게 딕셔너리 정보를 구성하는 역할
        :return:
        """
        sig = True
        save_path = set_save_folder(os.curdir, 'normalization')
        folder_name = self.folder_name.text().split('file://')[1]
        folder = os.listdir(folder_name)
        index_list = [file.split('.')[0] for file in folder]
        index_df_list = [pd.read_csv(folder_name+'/' + file) for file in folder]
        mod = Normalization()
        # =============================================================================
        #     RATE
        # =============================================================================
        if self.rateButton.isChecked():
            mod.set_option(index_df_list,
                           index_list, 'normalization', 'RATE', "")
            mod.scaling(os.curdir)

        elif self.logexpButton.isChecked():
            mod.set_option(index_df_list,
                           index_list, 'normalization', 'LOGEXP', "")
            mod.scaling(os.curdir)
        elif self.customButton.isChecked():
            #n_neighbors_list = [int(col.strip()) for col in self.le_n_neighbors.text().split(',')]
            #column_list = [col.strip() for col in self.le_column_list.text().split(',')]
            moon = self.save_name.text()
            mod.set_option(index_df_list,
                           index_list, 'normalization', 'USER', moon)
            mod.scaling(os.curdir)

        elif self.multicustomButton.isChecked():
            moon = self.save_name.text()
            mod.set_option(index_df_list,
                           index_list, 'normalization', 'USERS', moon)
            mod.scaling(os.curdir)
        else:
            print("미구현\n")
            sig = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = NormalWidget()
    form.show()
    app.exec_()
