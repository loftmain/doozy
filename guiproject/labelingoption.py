from PySide2.QtWidgets import (QApplication, QWidget, QPushButton,
                               QVBoxLayout, QHBoxLayout, QGroupBox,
                               QGridLayout, QLabel, QComboBox, QSpinBox,
                               QLineEdit, QFormLayout)
import sys
from PySide2.QtCore import Slot, Qt

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

class labeling(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setWindowTitle('create Label')

        self.okButton = QPushButton("ok", self)
        self.okButton.clicked.connect(self.slot_clicked_ok_button)

        gb_1 = QGroupBox("label 범위",self)
        firstIndexLabel = QLabel("first index", self)
        secondIndexLabel = QLabel("second index", self)
        firstColumnLabel = QLabel("first column", self)
        secondColumnLabel = QLabel("second column", self)

        gb_Layout_1 = QGridLayout(gb_1)

        self. firstIndexSpinBox = QSpinBox(self)
        self.firstIndexSpinBox.setValue(0)
        #self.spinBox.setSingleStep(10)
        self.firstIndexSpinBox.setMinimum(0)
        self.firstIndexSpinBox.setMaximum(5)
        #self.firstIndexSpinBox.valueChanged.connect(self.spinBoxChanged)

        self.secondIndexSpinBox = QSpinBox(self)
        self.secondIndexSpinBox.setValue(0)
        #self.spinBox.setSingleStep(10)
        self.secondIndexSpinBox.setMinimum(0)
        self.secondIndexSpinBox.setMaximum(5)
        #self.firstIndexSpinBox.valueChanged.connect(self.spinBoxChanged)

        self.firstColumnComboBox = QComboBox(self)
        self.secondColumnComboBox = QComboBox(self)
        self._fill_columns_info()

        gb_Layout_1.addWidget(firstIndexLabel, 0, 0)
        gb_Layout_1.addWidget(self.firstIndexSpinBox, 0, 1)
        gb_Layout_1.addWidget(firstColumnLabel, 0, 2)
        gb_Layout_1.addWidget(self.firstColumnComboBox, 0, 3)
        gb_Layout_1.addWidget(secondIndexLabel, 1, 0)
        gb_Layout_1.addWidget(self.secondIndexSpinBox, 1, 1)
        gb_Layout_1.addWidget(secondColumnLabel, 1, 2)
        gb_Layout_1.addWidget(self.secondColumnComboBox, 1, 3)

        gb_2 = QGroupBox("퍼센트", self)
        self.sb_per = QSpinBox(self)
        self.sb_per.setMinimum(-10)
        gb_Layout_2 = QHBoxLayout(gb_2)
        gb_Layout_2.addWidget(self.sb_per)
        gb_Layout_2.addWidget(QLabel("%", self))


        gb_3 = QGroupBox("업다운", self)
        self.cb_updown = QComboBox(self)
        self.cb_updown.addItems(["up", "down"])  # 다수 아이템 추가시
        gb_Layout_3 = QHBoxLayout(gb_3)
        gb_Layout_3.addWidget(self.cb_updown)

        hbox = QVBoxLayout()
        self.te_label_name = QLineEdit()
        hbox.addWidget(self.te_label_name)
        hbox.addStretch()

        self.file_name = LineEdit()
        self.mainlayout = QFormLayout()
        self.mainlayout.addRow(QLabel("file name(Drag in file view): "), self.file_name)
        self.mainlayout.addRow(gb_1)
        self.mainlayout.addRow(gb_2)
        self.mainlayout.addRow(gb_3)
        self.mainlayout.addRow(QLabel("label name: "), hbox)
        self.mainlayout.addRow( self.okButton)
        self.setLayout(self.mainlayout)

    def spinBoxChanged(self):
        val = self.spinBox.value()
        msg = '%d 인덱스부터 labeling계산을 합니다.' % (val)
        #self.statusBar.showMessage(msg)

    def _fill_columns_info(self):
        cloumn_name = ["open", "high", "low", "close"]
        self.firstColumnComboBox.insertItems(0, [x for x in cloumn_name])
        self.secondColumnComboBox.insertItems(0, [x for x in cloumn_name])

    @Slot(name="clickedOkButton")
    def slot_clicked_ok_button(self):
        serial_info = {
            "file_root": self.file_name.text(),
            "first_index": self.firstIndexSpinBox.value(),
            "first_column": self.firstColumnComboBox.currentText(),
            "second_index": self.secondIndexSpinBox.value(),
            "second_column": self.secondColumnComboBox.currentText(),
            "per": self.sb_per.value(),
            "updown": self.cb_updown.currentText(),
            "name": self.te_label_name.text(),
        }
        print(serial_info)
        #.currentText()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = labeling()
    form.show()
    app.exec_()