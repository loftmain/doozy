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
from PySide2.QtCore import QDate
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (QApplication, QWidget, QPushButton,
                               QRadioButton, QVBoxLayout, QLineEdit,
                               QHBoxLayout, QGroupBox, QGridLayout,
                               QLabel, QComboBox, QFormLayout, QDateEdit)
from module.classifier import run_modeling
from module.io import set_save_folder

# Own modules
from gui.markingwidget import LineEdit
from module.rnn_modeling import RNN_modeling


class ModelingOption(QWidget):
    """
    Modeling Menu의 UI
    예측
    | 일간 예측 | 월간 예측|
    일간 예측 미구현
    사용할 알고리즘
    | Random Forest | K-NN | Linear Regression | XGBoost |
    Linear Regression 과 XGBoost 세팅 미구현
    지정 독립변수 사용
    -> , 로 독립변수마다 띄어주어야함
    경로 지정
    dependent file path: MARKING 된 주가 CSV파일경로 ( Drag & Drop )
    condition list: HM4UP, LN4DN 과 같은 MARKING과 같은 이름 넣어줌
    indepentdent folder path: 경제지표가 들은 폴더 경로 ( Drag & Drop )

    """
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Button Demo')

        predBox = QGroupBox("예측", self)

        self.okButton = QPushButton("ok", self)
        self.okButton.clicked.connect(self.slot_clicked_ok_button)

        # self.button1 = QRadioButton("일간 예측", predBox)
        self.button2 = QRadioButton("월간 예측", predBox)
        self.button2.setChecked(True)

        algorithmBox = QGroupBox("사용할 알고리즘", self)
        self.rfButton = QRadioButton("Random Forest", algorithmBox)
        self.knnButton = QRadioButton("K-NN", algorithmBox)
        self.rnnButton = QRadioButton("RNN", algorithmBox)
        self.xgbButton = QRadioButton("XGBoost", algorithmBox)

        groupBoxLayout1 = QHBoxLayout(predBox)
        # groupBoxLayout1.addWidget(self.button1)
        groupBoxLayout1.addWidget(self.button2)

        groupBoxLayout2 = QHBoxLayout(algorithmBox)
        groupBoxLayout2.addWidget(self.rfButton)
        groupBoxLayout2.addWidget(self.knnButton)
        groupBoxLayout2.addWidget(self.rnnButton)
        groupBoxLayout2.addWidget(self.xgbButton)
        self.rfButton.toggled.connect(self.rfClicked)
        self.knnButton.toggled.connect(self.knnClicked)
        self.rnnButton.toggled.connect(self.rnnClicked)

        gb_independent_opt = QGroupBox("독립변수 설정", self)
        self.bt_all = QRadioButton("독립변수 조합을 이용", gb_independent_opt)
        self.bt_all.toggled.connect(self.clicked_all)
        self.bt_subset = QRadioButton("지정 독립변수 사용", gb_independent_opt)
        self.bt_subset.toggled.connect(self.clicked_subset)
        self.gb_layout3 = QVBoxLayout(gb_independent_opt)
        gb_Hlayout3 = QHBoxLayout()
        gb_Hlayout3.addWidget(self.bt_all)
        gb_Hlayout3.addWidget(self.bt_subset)
        self.gb_layout3.addLayout(gb_Hlayout3)

        # numberOfCombinationBox = QGroupBox("사용할 조합의 개수", self)

        self.gb = QGroupBox(self.tr("알고리즘 설정"))
        self.grid_box = QGridLayout()

        gb_3 = QGroupBox("경로 지정", self)
        formLayout = QFormLayout(gb_3)
        self.dependent_file_path = LineEdit()
        self.condition_list = QLineEdit()
        self.condition_list.setPlaceholderText("ex) HM4UP, LM4DN")
        self.independent_file_path = LineEdit()
        formLayout.addRow(QLabel("dependent file path: "), self.dependent_file_path)
        formLayout.addRow(QLabel("condition list: "), self.condition_list)
        formLayout.addRow(QLabel("independent folder path: "), self.independent_file_path)

        hb_2 = QHBoxLayout()
        hb_3 = QHBoxLayout()

        self.lb_train = QLabel("training date: ", self)
        self.de_train_start = QDateEdit(self)
        self.de_train_start.setDate(QDate(1999, 1, 3))
        self.de_train_start.setDisplayFormat('yyyy-MM-dd')
        # self.de_train_start.setDate(QDate.currentDate())
        self.de_train_start.setCalendarPopup(True)

        self.de_train_end = QDateEdit(self)
        # self.de_train_end.setDate(QDate(2017, 1, 3))
        self.de_train_end.setDisplayFormat('yyyy-MM-dd')
        self.de_train_end.setDate(QDate.currentDate())
        self.de_train_end.setCalendarPopup(True)

        self.lb_test = QLabel("test date: ", self)
        self.de_test_start = QDateEdit(self)
        # self.de_test_start.setDate(QDate(2017, 1, 3))
        self.de_test_start.setDisplayFormat('yyyy-MM-dd')
        self.de_test_start.setDate(QDate.currentDate())
        self.de_test_start.setCalendarPopup(True)

        self.de_test_end = QDateEdit(self)
        # self.de_test_end.setDate(QDate(2017, 1, 3))
        self.de_test_end.setDisplayFormat('yyyy-MM-dd')
        self.de_test_end.setDate(QDate.currentDate())
        self.de_test_end.setCalendarPopup(True)

        hb_2.addWidget(self.lb_train)
        hb_2.addWidget(self.de_train_start)
        hb_2.addWidget(QLabel(" ~ ", self))
        hb_2.addWidget(self.de_train_end)

        hb_3.addWidget(self.lb_test)
        hb_3.addWidget(self.de_test_start)
        hb_3.addWidget(QLabel(" ~ ", self))
        hb_3.addWidget(self.de_test_end)

        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(predBox)
        self.mainlayout.addWidget(algorithmBox)
        self.mainlayout.addWidget(self.gb)

        self.mainlayout.addSpacing(15)
        self.mainlayout.addWidget(gb_independent_opt)
        # self.mainlayout.addWidget(numberOfCombinationBox)
        self.mainlayout.addWidget(gb_3)
        self.mainlayout.addLayout(hb_2)

        self.mainlayout.addLayout(hb_3)
        self.mainlayout.addStretch()
        self.mainlayout.setMargin(30)
        self.mainlayout.addWidget(self.okButton)

        self.setLayout(self.mainlayout)

    def rfClicked(self):
        """
        Random Forest Radio Button 을 클릭시 나오는 UI
        """
        if self.rfButton.text() == "Random Forest":
            if self.rfButton.isChecked():
                # self.gb = QGroupBox(self.tr("Serial"))

                self.cb_estimators = QComboBox()
                self.cb_estimators.addItems(['100', '200', '300', '400', '500'])
                self.cb_max_depth = QComboBox()
                self.cb_max_depth.addItems(['2', '4', '6', '8', '10'])
                self.cb_max_depth.setCurrentIndex(3)
                self.le_max_features = LineEdit()
                self.le_max_features.setText("auto")
                self.cb_bootstrap = QComboBox()
                self.cb_bootstrap.addItems(['True', 'False'])

                self.grid_box.addWidget(QLabel(self.tr("n_estimators")), 0, 0)
                self.grid_box.addWidget(self.cb_estimators, 0, 1)

                self.grid_box.addWidget(QLabel(self.tr("max_depth")), 1, 0)
                self.grid_box.addWidget(self.cb_max_depth, 1, 1)

                self.grid_box.addWidget(QLabel(self.tr("max_features")), 2, 0)
                self.grid_box.addWidget(self.le_max_features, 2, 1)
                self.grid_box.addWidget(QLabel(self.tr("bootstrap")), 3, 0)
                self.grid_box.addWidget(self.cb_bootstrap, 3, 1)
                self.gb.setLayout(self.grid_box)

                self.update()
            else:
                self.clearLayout(self.grid_box)
                self.update()

    def knnClicked(self):
        """
        K-NN Radio Button 을 클릭시 나오는 UI
        """
        if self.knnButton.text() == "K-NN":
            if self.knnButton.isChecked():
                # self.gb = QGroupBox(self.tr("Serial"))

                # self.grid_box = QGridLayout()
                self.le_n_neighbors = QLineEdit()
                self.le_n_neighbors.setText("3, 5")
                self.grid_box.addWidget(QLabel(self.tr("n_neighbors")), 0, 0)
                self.grid_box.addWidget(self.le_n_neighbors, 0, 1)

                self.gb.setLayout(self.grid_box)
                self.update()
            else:
                self.clearLayout(self.grid_box)
                self.update()

    def rnnClicked(self):
        """
        Random Forest Radio Button 을 클릭시 나오는 UI
        """
        if self.rnnButton.text() == "RNN":
            if self.rnnButton.isChecked():
                # self.gb = QGroupBox(self.tr("Serial"))

                self.le_layer = LineEdit()
                self.cb_in_activ = QComboBox()
                self.cb_in_activ.addItems(['relu', 'elu', 'selu', 'softplus', 'softsign'])
                #self.cb_in_activ.setCurrentIndex(3)
                self.cb_out_activ = QComboBox()
                self.cb_out_activ.addItems(['softmax', 'linear', 'sigmoid'])
                self.cb_epoch = QComboBox()
                self.cb_epoch.addItems(['100', '200', '300', '400', '500'])
                self.le_tr_size = LineEdit()
                self.le_normal = LineEdit()

                self.grid_box.addWidget(QLabel(self.tr("Layer Size")), 0, 0)
                self.grid_box.addWidget(self.le_layer, 0, 1)

                self.grid_box.addWidget(QLabel(self.tr("input Activation Function")), 1, 0)
                self.grid_box.addWidget(self.cb_in_activ, 1, 1)

                self.grid_box.addWidget(QLabel(self.tr("Output Activation Function")), 2, 0)
                self.grid_box.addWidget(self.cb_out_activ, 2, 1)
                self.grid_box.addWidget(QLabel(self.tr("Epoch")), 3, 0)
                self.grid_box.addWidget(self.cb_epoch, 3, 1)
                self.grid_box.addWidget(QLabel(self.tr("Training Size")), 4, 0)
                self.grid_box.addWidget(self.le_tr_size, 4, 1)
                self.grid_box.addWidget(QLabel(self.tr("normalization")), 5, 0)
                self.grid_box.addWidget(self.le_normal, 5, 1)
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
        condition_list = [col.strip() for col in self.condition_list.text().split(',')]
        save_path = set_save_folder(os.curdir, 'modeling')
        dependent_file_path = self.dependent_file_path.text().split('file://')[1]
        independent_file_path = self.independent_file_path.text().split('file://')[1]
        # =============================================================================
        #     KNN
        # =============================================================================
        if self.knnButton.isChecked():
            n_neighbors_list = [int(col.strip()) for col in self.le_n_neighbors.text().split(',')]
            if self.bt_subset.isChecked():
                column_list = [col.strip() for col in self.le_column_list.text().split(',')]
                start_setting = \
                    {
                        'setting':
                            [
                                {
                                    'classifier': 'KNN',
                                    'type_option_list': {'n_neighbors_list': n_neighbors_list},
                                    'column_option_list': \
                                        {'option': 'subset', 'column_list': [column_list]},
                                    'condition_list': condition_list.text(),
                                    'dependent_file_path': dependent_file_path,
                                    'independent_path': independent_file_path,
                                    'save_path': save_path,
                                    'start_date': self.de_train_start.text(),
                                    'seperate_date': self.de_train_end.text(),
                                    'end_date': self.de_test_end.text()
                                }
                            ]
                    }
                print(start_setting)
            elif self.bt_all.isChecked():
                range_of_column_no = [int(self.startNum.currentText()), int(self.endNum.currentText())]

                start_setting = \
                    {
                        'setting':
                            [
                                {
                                    'classifier': 'KNN',
                                    'type_option_list': {'n_neighbors_list': n_neighbors_list},
                                    'column_option_list': \
                                        {'option': 'all', 'range_of_column_no': range_of_column_no},
                                    'condition_list': condition_list,
                                    'dependent_file_path': dependent_file_path,
                                    'independent_path': independent_file_path,
                                    'save_path': save_path,
                                    'start_date': self.de_train_start.text(),
                                    'seperate_date': self.de_train_end.text(),
                                    'end_date': self.de_test_end.text()
                                }
                            ]
                    }
                print(start_setting)
        # =============================================================================
        #     RANDOM FOREST
        # =============================================================================
        elif self.rfButton.isChecked():
            if self.bt_subset.isChecked():
                column_list = [col.strip() for col in self.le_column_list.text().split(',')]
                start_setting = \
                    {'setting':
                        [
                            {
                                'classifier': 'RF',
                                'type_option_list': {'n_estimators': int(self.cb_estimators.currentText()),
                                                     'max_depth': int(self.cb_max_depth.currentText()),
                                                     'random_state': 0,
                                                     'max_features': self.le_max_features.text(),
                                                     'bootstrap': bool(self.cb_bootstrap.currentText())},
                                'column_option_list': \
                                    {'option': 'subset', 'column_list': [column_list]},
                                'condition_list': condition_list,
                                'dependent_file_path': dependent_file_path,
                                'independent_path': independent_file_path,
                                'save_path': save_path,
                                'start_date': self.de_train_start.text(),
                                'seperate_date': self.de_train_end.text(),
                                'end_date': self.de_test_end.text()
                            }
                        ]
                    }
                print(start_setting)
            elif self.bt_all.isChecked():
                range_of_column_no = [int(self.startNum.currentText()), int(self.endNum.currentText())]
                start_setting = \
                    {
                        'setting':
                            [
                                {
                                    'classifier': 'RF',
                                    'type_option_list': {'n_estimators': int(self.cb_estimators.currentText()),
                                                         'max_depth': int(self.cb_max_depth.currentText()),
                                                         'random_state': 0,
                                                         'max_features': self.le_max_features.text(),
                                                         'bootstrap': bool(self.cb_bootstrap.currentText())},
                                    'column_option_list': \
                                        {'option': 'all', 'range_of_column_no': range_of_column_no},
                                    'condition_list': condition_list,
                                    'dependent_file_path': dependent_file_path,
                                    'independent_path': independent_file_path,
                                    'save_path': save_path,
                                    'start_date': self.de_train_start.text(),
                                    'seperate_date': self.de_train_end.text(),
                                    'end_date': self.de_test_end.text()
                                }
                            ]
                    }
                print(start_setting)
        # =============================================================================
        #     RMM
        # =============================================================================
        elif self.rnnButton.isChecked():
            if self.bt_subset.isChecked():
                column_list = [col.strip() for col in self.le_column_list.text().split(',')]
                mod = RNN_modeling()
                data = pd.read_csv(dependent_file_path)
                mod.set_option(column_list, condition_list,
                               int(len(data)*0.7))
                mod.set_model_option(int(self.le_layer.text()), self.cb_in_activ.currentText(),
                                     self.cb_out_activ.currentText(), int(self.cb_epoch.currentText()))
                mod.merge_data(data, independent_file_path, self.le_normal.text(), 3)
                predict, scoring = mod.modeling()
                res = data[:-3][-35:]
                res['predicted'] = predict
                res.to_csv(save_path + str(scoring) + '.csv', header=True, index=False)

                sig = False
            else:
                print("미구현\n")
                sig = False
        if sig == True:
            run_modeling(start_setting)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ModelingOption()
    form.show()
    app.exec_()
