from PyQt5.QtCore import pyqtSlot, QDate, QTime
from PyQt5.QtWidgets import *


class MainGUI(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        self.label_start = QLabel("시작일", self)
        self.label_start.setStyleSheet("background-color: yellow")
        self.dateed_start = QDateEdit(self)
        # self.dateed_start.setDate(QDate(2017, 1, 3))
        self.dateed_start.setDate(QDate.currentDate())
        self.dateed_start.setCalendarPopup(True)

        self.label_end = QLabel("종료일", self)
        self.label_end.setStyleSheet("background-color: yellow")
        self.dateed_end = QDateEdit(self)
        # self.dateed_end.setDate(QDate(2017, 1, 3))
        self.dateed_end.setDate(QDate.currentDate())
        self.dateed_end.setCalendarPopup(True)

        self.label3 = QLabel("QDateTimeEdit")
        self.datetimeed = QDateTimeEdit(self)
        self.datetimeed.setCalendarPopup(True)
        self.timeed = QTimeEdit(self)
        self.timeed.setDisplayFormat("hh:mm")  # 24 시간으로 표시
        self.timeed.setTime(QTime(15, 30))

        self._btn_getdate = QPushButton("날짜,시간 구하기", self)

        hbox1.addWidget(self.label_start)
        hbox1.addWidget(self.dateed_start)
        hbox1.addSpacing(50)
        hbox1.addWidget(self.label_end)
        hbox1.addWidget(self.dateed_end)
        hbox1.addStretch()

        vbox.addLayout(hbox1)
        vbox.addSpacing(10)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.label3)
        hbox2.addWidget(self.datetimeed)
        hbox2.addStretch()

        vbox.addLayout(hbox2)
        vbox.addSpacing(20)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(8)
        hbox3.addWidget(QLabel("QTimeEdit"))
        hbox3.addWidget(self.timeed)
        hbox3.addStretch(1)
        hbox3.addWidget(self._btn_getdate)

        vbox.addLayout(hbox3)

        hbox4 = QHBoxLayout()
        self.cal = QCalendarWidget(self)  # 달력
        self.cal.setVerticalHeaderFormat(0)  # vertical header 숨기기
        # print(self.cal.sizeHint())
        # self.cal.resize(self.cal.sizeHint())
        # self.cal.setFixedSize(200, 200)  # w, h
        self.cal.setFixedSize(self.cal.sizeHint())  # w, h
        hbox4.addWidget(self.cal)
        hbox4.addStretch()

        vbox.addLayout(hbox4)

        self.qtxt = QTextEdit(self)
        vbox.addWidget(self.qtxt)

        self.setLayout(vbox)
        self.setGeometry(100, 100, 800, 650)


class MyMain(MainGUI):
    def __init__(self):
        super().__init__()

        self._btn_getdate.clicked.connect(self.__btn_getdate_clicked)
        self.cal.clicked.connect(self.__cal_clicked)
        self.cal.selectionChanged.connect(self.__cal_selectionchanged)

    @pyqtSlot()
    def __btn_getdate_clicked(self):
        self.qtxt.append("\n\n======== 시작일 =============")
        self.qtxt.append(str(self.dateed_start.date()))
        self.qtxt.append(self.dateed_start.date().toString())

        ddate = str(self.dateed_start.date().toPyDate())
        ddate_tmp = ddate.split("-")
        ddate2 = "".join(ddate_tmp)
        self.qtxt.append(ddate)
        self.qtxt.append(ddate2)

        self.qtxt.append("\n======== 종료일 =============")
        self.qtxt.append(str(self.dateed_end.date()))
        self.qtxt.append(self.dateed_end.date().toString())
        self.qtxt.append(str(self.dateed_end.date().toPyDate()))

        self.qtxt.append("\n====== QDateTimeEdit ==========")
        self.qtxt.append(str(self.datetimeed.dateTime()))
        self.qtxt.append(self.datetimeed.dateTime().toString())
        self.qtxt.append(str(self.datetimeed.dateTime().toPyDateTime()))

        self.qtxt.append("\n ====== QTimeEdit ==========")
        self.qtxt.append(str(self.timeed.time()))

        ttime = self.timeed.time().toString()
        self.qtxt.append(ttime)
        self.qtxt.append(str(self.timeed.time().toPyTime()))

        ttime_tmp = ttime.split(":")
        ttime2 = "".join(ttime_tmp[:-1])
        self.qtxt.append("초 제거후 ==>" + ttime2)

        self.qtxt.append("")
        self.qtxt.append("minimumTime ==> " + str(self.timeed.minimumTime()))
        self.qtxt.append("maximumTime ==> " + str(self.timeed.maximumTime()))
        self.qtxt.append("displayFormat ==> " + str(self.timeed.displayFormat()))

    @pyqtSlot(QDate)
    def __cal_clicked(self, ddate):
        self.qtxt.append("----- calendar clicked.....")
        self.qtxt.append(ddate.toString())
        tmp_date = str(ddate.toPyDate())
        tmp2 = tmp_date.split("-")
        ddate2 = "".join(tmp2)

        self.qtxt.append(tmp_date)
        self.qtxt.append(ddate2)

        self.qtxt.append("월 = " + str(self.cal.monthShown()))
        self.qtxt.append("년 = " + str(self.cal.yearShown()))

        self.cal.showToday()  # 달력에서 오늘 날짜 보이는 년월로 돌아온다.

    @pyqtSlot()
    def __cal_selectionchanged(self):  # 화살표버튼눌러 이동시에도 작동한다...
        self.qtxt.append("------ calendar selection changed.....")
        ddate = self.cal.selectedDate()
        # print(ddate)
        self.qtxt.append(ddate.toString())
        self.qtxt.append(str(ddate.toPyDate()))
        # print(ddate.toJulianDay())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    myWindow = MyMain()

    myWindow.show()
    app.exec_()
