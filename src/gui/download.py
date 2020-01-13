#!interpreter [project-doozy]
# -*- coding: utf-8 -*-

"""
gui runcher
{License_info} 라이센스 정해야함
"""

# Built-in/Generic Imports
import sys
import os

# Libs
import pandas as pd
from fredapi import Fred
from datetime import datetime
from dateutil.relativedelta import relativedelta
from PySide2.QtWidgets import QDialog, QLabel, QProgressBar, QPushButton, QVBoxLayout\
                        , QApplication


fred = Fred(api_key='3b2795f81c94f1a105d1e4fc3661a45e')

class DlIndependentDialog(QDialog):
    def __init__(self, path):
        super().__init__()
        self.setupUI()
        self.path = path

    def setupUI(self):
        self.setWindowTitle("independent download")

        label1 = QLabel("30개의 경제 지표를 다운로드", self)
        self.progress = QProgressBar(self)
        self.progress.setMaximum(30)
        self.btn = QPushButton("Download", self)
        self.btn.clicked.connect(self.download)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.progress)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def download(self):
        self.completed = 0
        self.gathering()
        #while self.completed < 100:


    def inspect_index_folder(self):
        if not os.path.exists(os.path.join(self.path, 'independent')):
            os.mkdir(os.path.join(self.path, 'independent'))
        folderpath = os.path.join(self.path, 'independent')
        return folderpath


    def inspect_column_file(self):
        line = 'BAA,CSUSHPINSA,PCE,LREMTTTTUSM156S,DGORDER,TWEXBMTH,UNRATENSA,TCU,INDPRO,PPIACO,CPIAUCSL,HOUST,HSN1F,FEDFUNDS,USSLIND,TOTALSA,NEWORDER,UMCSENT,AMBNS,EXJPUS,EXKOUS,EXCHUS,T10Y2YM,XTEXVA01CNM667S,GACDFSA066MSFRBPHI,XTIMVA01KRM667S,KORPROINDMISMEI,KORCPIALLMINMEI,LRUNTTTTKRM156S,IR3TCD01KRM156N'
        index_list = list(map(str, (line.split(','))))
        return index_list


    def gathering(self):
        folderpath = self.inspect_index_folder()
        index_list = self.inspect_column_file()
        if index_list == False: return False

        time_point = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

        # for index in index_list:
        for index in index_list:
            # Get data from fred
            df = fred.get_series_all_releases(index)
            # df_info = fred.search(index)

            # Drop column(realtime_start column)
            df.drop_duplicates(["date"], keep="last", inplace=True)

            # Change column name
            df['DATE'] = df['date'].dt.date
            df.rename(columns={'value': index}, inplace=True)

            # Column sort
            df = df[['DATE', index]]

            # Drop column(realtime_start column)
            df.drop(df[df.DATE < time_point].index, inplace=True)
            df.index = pd.RangeIndex(len(df.index))

            # Add empty row, Because we use shifted data and use it Machine-Learning
            df.loc[len(df), 'DATE'] = df['DATE'][len(df) - 1] + relativedelta(months=1)
            df.loc[len(df), 'DATE'] = df['DATE'][len(df) - 2] + relativedelta(months=2)
            df.loc[len(df), 'DATE'] = df['DATE'][len(df) - 3] + relativedelta(months=3)

            # Check for bad data
            try:
                df[index + 'rate'] = (df[index] / df[index].shift(+1)) - 1
                print(index, ": success")
            except ZeroDivisionError:
                print(index, ": error(data contained zero)")
                continue

            # Write to excel file
            df.to_excel(os.path.join(folderpath, index) + '.xlsx', sheet_name='Sheet1', index=False)
            # df_info.to_excel(writer, sheet_name='Sheet2', index=False)
            self.completed += 1
            self.progress.setValue(self.completed)
        return True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DlIndependentDialog()
    window.show()
    app.exec_()