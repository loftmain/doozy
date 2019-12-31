from PySide2.QtWidgets import (QApplication, QWidget, QPushButton,
                               QCheckBox, QRadioButton, QVBoxLayout,
                               QHBoxLayout, QGroupBox, QGridLayout,
                               QLabel, QComboBox, QBoxLayout)
import sys

class ModelingOption(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setWindowTitle('Button Demo')

        predBox = QGroupBox("예측",self)

        self.okButton = QPushButton("ok", self)



        self.button1 = QRadioButton("일간 예측",predBox)
        self.button2 = QRadioButton("월간 예측",predBox)
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

        numberOfCombinationBox = QGroupBox("사용할 조합의 개수", self)
        self.startNum = QComboBox()
        self.startNum.insertItems(0, [str(x) for x in range(10)])
        self.endNum = QComboBox()
        self.endNum.insertItems(0, [str(x) for x in range(10)])
        groupBoxLayout3 = QHBoxLayout(numberOfCombinationBox)
        groupBoxLayout3.addWidget(self.startNum)
        groupBoxLayout3.addWidget(QLabel(self.tr("~")))
        groupBoxLayout3.addWidget(self.endNum)

        self.gb = QGroupBox(self.tr("Serial"))
        self.grid_box = QGridLayout()

        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(predBox)
        self.mainlayout.addWidget(algorithmBox)
        self.mainlayout.addWidget(self.gb)
        self.mainlayout.addWidget(numberOfCombinationBox)
        self.mainlayout.addStretch()
        self.mainlayout.addWidget(self.okButton)

        self.setLayout(self.mainlayout)

    def rfClicked(self):
        if self.rfButton.text() == "Random Forest":
            if self.rfButton.isChecked():
                #self.gb = QGroupBox(self.tr("Serial"))

                self.cb_port = QComboBox()
                self.cb_baud_rate = QComboBox()
                self.grid_box.addWidget(QLabel(self.tr("RF")), 0, 0)
                self.grid_box.addWidget(self.cb_port, 0, 1)

                self.grid_box.addWidget(QLabel(self.tr("RF")), 1, 0)
                self.grid_box.addWidget(self.cb_baud_rate, 1, 1)

                self.gb.setLayout(self.grid_box)
                #self.mainlayout.addWidget(self.gb)

                self.update()
            else:
                self.clearLayout(self.grid_box)
                self.update()


    def knnClicked(self):
        if self.knnButton.text() == "K-NN":
            if self.knnButton.isChecked():
                #self.gb = QGroupBox(self.tr("Serial"))

                #self.grid_box = QGridLayout()
                self.cb_port = QComboBox()
                self.cb_baud_rate = QComboBox()
                self.grid_box.addWidget(QLabel(self.tr("KNN")), 0, 0)
                self.grid_box.addWidget(self.cb_port, 0, 1)

                self.grid_box.addWidget(QLabel(self.tr("KNN")), 1, 0)
                self.grid_box.addWidget(self.cb_baud_rate, 1, 1)

                self.gb.setLayout(self.grid_box)
                #self.mainlayout.addWidget(self.gb)

                self.update()
            else:
                #self.mainlayout.removeWidget(self.gb)
                self.clearLayout(self.grid_box)

                self.update()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ModelingOption()
    form.show()
    app.exec_()