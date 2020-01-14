#!interpreter [project-doozy]
# -*- coding: utf-8 -*-

"""
gui runcher
{License_info} 라이센스 정해야함
"""

# Built-in/Generic Imports
import os
import sys

from PySide2.QtCore import QDate
from PySide2.QtCore import Slot
# Libs
from PySide2.QtWidgets import (QApplication, QWidget, QPushButton,
                               QRadioButton, QVBoxLayout, QLineEdit,
                               QHBoxLayout, QGroupBox, QGridLayout,
                               QLabel, QComboBox, QFormLayout, QDateEdit)

from src.gui.markingwidget import LineEdit
from src.module.classifier import run_modeling


class ModelingOption(QWidget):
    def __init__(self, path):
        QWidget.__init__(self)
        self.path = path
        self.setWindowTitle('Button Demo')

        predBox = QGroupBox("예측", self)

        self.okButton = QPushButton("ok", self)
        self.okButton.clicked.connect(self.slot_clicked_ok_button)

        self.button1 = QRadioButton("일간 예측", predBox)
        self.button2 = QRadioButton("월간 예측", predBox)
        self.button2.setChecked(True)

        algorithmBox = QGroupBox("사용할 알고리즘", self)
        self.rfButton = QRadioButton("Random Forest", algorithmBox)
        self.knnButton = QRadioButton("K-NN", algorithmBox)
        self.lrButton = QRadioButton("Linear Regression", algorithmBox)
        self.xgbButton = QRadioButton("XGBoost", algorithmBox)

        groupBoxLayout1 = QHBoxLayout(predBox)
        groupBoxLayout1.addWidget(self.button1)
        groupBoxLayout1.addWidget(self.button2)

        groupBoxLayout2 = QHBoxLayout(algorithmBox)
        groupBoxLayout2.addWidget(self.rfButton)
        groupBoxLayout2.addWidget(self.knnButton)
        groupBoxLayout2.addWidget(self.lrButton)
        groupBoxLayout2.addWidget(self.xgbButton)
        self.rfButton.toggled.connect(self.rfClicked)
        self.knnButton.toggled.connect(self.knnClicked)

        gb_independent_opt = QGroupBox("독립변수 설정", self)
        self.bt_all = QRadioButton("all", gb_independent_opt)
        self.bt_all.toggled.connect(self.clicked_all)
        self.bt_subset = QRadioButton("subset", gb_independent_opt)
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
        # self.dateed_start.setDate(QDate(2017, 1, 3))
        self.de_train_start.setDate(QDate.currentDate())
        self.de_train_start.setCalendarPopup(True)

        self.de_train_end = QDateEdit(self)
        # self.de_train_end.setDate(QDate(2017, 1, 3))
        self.de_train_end.setDate(QDate.currentDate())
        self.de_train_end.setCalendarPopup(True)

        self.lb_test = QLabel("test date: ", self)
        self.de_test_start = QDateEdit(self)
        # self.de_test_start.setDate(QDate(2017, 1, 3))
        self.de_test_start.setDate(QDate.currentDate())
        self.de_test_start.setCalendarPopup(True)

        self.de_test_end = QDateEdit(self)
        # self.de_test_end.setDate(QDate(2017, 1, 3))
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
        self.mainlayout.addWidget(gb_independent_opt)
        # self.mainlayout.addWidget(numberOfCombinationBox)
        self.mainlayout.addWidget(gb_3)
        self.mainlayout.addLayout(hb_2)
        self.mainlayout.addLayout(hb_3)
        self.mainlayout.addStretch()
        self.mainlayout.addWidget(self.okButton)

        self.setLayout(self.mainlayout)

    def rfClicked(self):
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

    def clicked_all(self):
        if self.bt_all.isChecked():
            self.startNum = QComboBox()
            self.startNum.insertItems(0, [str(x) for x in range(10)])
            self.endNum = QComboBox()
            self.endNum.insertItems(0, [str(x) for x in range(10)])
            self.groupBoxLayout3 = QHBoxLayout()
            self.groupBoxLayout3.addWidget(self.startNum)
            self.groupBoxLayout3.addWidget(QLabel(self.tr("~")))
            self.groupBoxLayout3.addWidget(self.endNum)
            self.gb_layout3.addLayout(self.groupBoxLayout3)
        else:
            self.clearLayout(self.groupBoxLayout3)

    def clicked_subset(self):
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
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    @Slot(name="clickedOkButton")
    def slot_clicked_ok_button(self):
        sig = True
        if not os.path.exists(os.path.join(self.path, 'save')):
            os.mkdir(os.path.join(self.path, 'save'))
        save_path = os.path.join(self.path, 'save')
        dependent_file_path = self.dependent_file_path.text().split('file:///')[1]
        independent_file_path = self.independent_file_path.text().split('file:///')[1]
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
                                    'condition_list': self.condition_list.text().split(','),
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
                                    'condition_list': self.condition_list.text().split(','),
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
                                'condition_list': self.condition_list.text().split(','),
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
                                    'condition_list': self.condition_list.text().split(','),
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
            else:
                print("미구현\n")
                sig = False
        if sig == True:
            run_modeling(start_setting, self.path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ModelingOption("")
    form.show()
    app.exec_()
