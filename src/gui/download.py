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
from datetime import datetime

# Libs
import pandas as pd
from PySide2.QtWidgets import QDialog, QLabel, QProgressBar, QPushButton, QVBoxLayout \
    , QApplication
from dateutil.relativedelta import relativedelta
from fredapi import Fred

# 임시로 개인 key 사용
fred = Fred(api_key='3b2795f81c94f1a105d1e4fc3661a45e')


class DlIndependentDialog(QDialog):
    """
    경제지표 다운로드 Dialog입니다.
    """

    def __init__(self, path):
        super().__init__()
        self.setupUI()
        self.path = path

    def setupUI(self):
        """
        UI의 화면 설정
        """
        self.setWindowTitle("independent download")

        label1 = QLabel("70개의 경제 지표를 다운로드", self)
        self.progress = QProgressBar(self)

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
        """
        다운로드 경로 설정
        """
        if not os.path.exists(os.path.join(self.path, 'independent')):
            os.mkdir(os.path.join(self.path, 'independent'))
        folderpath = os.path.join(self.path, 'independent')
        return folderpath


    def inspect_column_file(self):
        """
        경제지표 리스트 지정
        """
        line = 'AAA,AHETPI,ALTSALES,AMBNS,AMBSL,BAA,BAA10YM,BOGMBASE,BUSLOANS,BUSLOANSNSA,CES0500000003,' \
               'CEU0500000003,CIVPART,CPALTT01USM657N,CPALTT01USM659N,CPALTT01USM661S,CPIAUCNS,CPIAUCSL,' \
               'CPILFENS,CPILFESL,CSUSHPINSA,CSUSHPISA,DGORDER,DPCERAM1M225NBEA,DSPIC96,EXCHUS,EXCSRESNS,' \
               'EXJPUS,EXUSEU,FEDFUNDS,FII10,GS1,GS10,GS2,GS20,GS30,GS3M,GS5,H8B1023NCBCMG,HOUST,HOUSTNSA,' \
               'HTRUCKSNSA,HTRUCKSSA,HTRUCKSSAAR,INDPRO,INTDSRUSM193N,LFWA64TTUSM647N,LFWA64TTUSM647S,LNS14000024,' \
               'LNS14000031,LNU04000024,LNU04000031,M1NS,M1SL,M2NS,M2SL,MANEMP,MCOILBRENTEU,MCOILWTICO,MPRIME,MSACSR,' \
               'MSACSRNSA,MTSDS133FMS,PAYEMS,PAYNSA,PCE,PCEC96,PCEPI,PCEPILFE,PERMIT,PERMITNSA,PPIACO,PSAVERT,' \
               'RECPROUSM156N,SFXRNSA,SFXRSA,SPCS20RNSA,SPCS20RSA,T10Y2YM,T10Y3MM,T10YFFM,T10YIEM,T5YIEM,T5YIFRM,' \
               'TB3MS,TOTALNSA,TOTALSA,TWEXBMTH,TWEXMMTH,UMCSENT,UNRATE,UNRATENSA,USSLIND,WPU0911,WPU091105,WPU09110501'
        index_list = list(map(str, (line.split(','))))
        return index_list


    def gathering(self):
        """
        경제지표 다운로드 프로그램
        default start date: 2000-01-01
        3개월 shift하여 저장
        """
        folderpath = self.inspect_index_folder()
        index_list = self.inspect_column_file()
        if index_list == False: return False

        time_point = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
        self.progress.setMaximum(len(index_list))
        # for index in index_list:
        for index in index_list:
            # Get data from fred
            df = fred.get_series_all_releases(index)
            # df_info = fred.search(index)

            # Drop column(realtime_start column)
            df.drop_duplicates(["date"], keep="last", inplace=True)

            # Change column name
            df['Date'] = df['date'].dt.date
            df.rename(columns={'value': index}, inplace=True)

            # Column sort
            df = df[['Date', index]]

            # Drop column(realtime_start column)
            df.drop(df[df.Date < time_point].index, inplace=True)
            df.index = pd.RangeIndex(len(df.index))

            # Add empty row, Because we use shifted data and use it Machine-Learning
            df.loc[len(df), 'Date'] = df['Date'][len(df) - 1] + relativedelta(months=1)
            df.loc[len(df), 'Date'] = df['Date'][len(df) - 2] + relativedelta(months=2)
            df.loc[len(df), 'Date'] = df['Date'][len(df) - 3] + relativedelta(months=3)

            # Check for bad data
            try:
                df[index + 'rate'] = (df[index] / df[index].shift(+1)) - 1
                print(index, ": success")
            except ZeroDivisionError:
                print(index, ": error(data contained zero)")
                continue

            # Write to excel file
            df.to_csv(os.path.join(folderpath, index) + '.csv', index=False)
            # df_info.to_excel(writer, sheet_name='Sheet2', index=False)
            self.completed += 1
            self.progress.setValue(self.completed)
        return True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DlIndependentDialog(os.curdir)
    window.show()
    app.exec_()