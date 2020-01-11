import sys

from PySide2.QtWidgets import (QApplication, QWidget, QPushButton,
                                QVBoxLayout, QGroupBox, QLabel,
                               QFormLayout,QRadioButton, QSpinBox, QHBoxLayout)
from PySide2.QtCore import Slot, Qt
from src.gui.markingwidget import LineEdit

class OrderRunWidget(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setWindowTitle('orderexcute')


        self.run_button = QPushButton("run", self)
        self.run_button.clicked.connect(self.slot_clicked_run_button)


        gb_1 = QGroupBox("create order", self)
        formLayout = QFormLayout(gb_1)
        self.dependent_file_path = LineEdit()
        self.independent_file_path = LineEdit()
        self.lb_info = QLabel("*drag in file view*")
        self.lb_info.setAlignment(Qt.AlignRight)
        formLayout.addRow(self.lb_info)
        formLayout.addRow(QLabel("order file path: "), self.dependent_file_path)
        formLayout.addRow(QLabel("column name: "), self.independent_file_path)

        gb_2 = QGroupBox("전략선택", self)
        self.rb_1 = QRadioButton('HLBS')
        self.rb_2 = QRadioButton('HLBLS')
        self.rb_3 = QRadioButton('LMBS')
        self.rb_4 = QRadioButton('LMBLS')
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


        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(gb_1)
        self.mainlayout.addWidget(gb_2)
        self.mainlayout.addWidget(gb_3)
        self.mainlayout.addStretch()
        self.mainlayout.addWidget(self.run_button)
        self.setLayout(self.mainlayout)

    def rb_clicked(self):
        if self.rb_1.isChecked():
            return self.rb_1.text()
        elif self.rb_2.isChecked():
            return self.rb_2.text()
        elif self.rb_3.isChecked():
            return self.rb_3.text()
        elif self.rb_4.isChecked():
            return self.rb_4.text()
        else:
            print("ERROR: radio button is unchecked")


    @Slot(name="clickedRunButton")
    def slot_clicked_run_button(self):
        setting_info = {
            "order_file_path": self.dependent_file_path.text(),
            "column_name": self.independent_file_path.text(),
            "strategy": self.rb_clicked(),
            "per": self.sb_per.text()
        }
        print(setting_info)
        #.currentText()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = OrderRunWidget()
    form.show()
    app.exec_()