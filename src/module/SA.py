import glob

import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)


# pd.set_option('display.max_rows', None)

class PeriodError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MissingValueError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class SA(object):
    def __init__(self,
                 condition_list,
                 dependent_path,
                 independent_path,
                 saved_path,
                 start_date,
                 seperate_date,
                 end_date,
                 column_list=None):
        self.dataframe = pd.read_csv(dependent_path, encoding='CP949')

        self.column_list = column_list
        self.condition_list = condition_list
        self.dependent_path = dependent_path
        self.independent_path = independent_path
        self.saved_path = saved_path
        self.start_date = start_date
        self.seperate_date = seperate_date
        self.end_date = end_date
        self.y_prediction = None
        # if 'Date' in self.dataframe:
        #    self.dataframe.rename(columns={'Date': 'DATE'}, inplace=True)
        self.dependent_columns = list(self.dataframe)
        self.dependent_columns.remove("Date")

    def check_error(self, dataframe):
        """
        dataframe에 대해서 오류가 있는지 check를 해야함.
        1. 데이터 무결성
            - None값이 있는지
            - None값에 0을 넣어놓은 경우
            - 매월 데이터가 있는가
        2. 원하는 분석 기간까지 데이터가 있는가

        """
        dataframe = dataframe.replace('', np.nan)
        dataframe_na_sum = dataframe.isnull().sum().sum()
        if int(dataframe_na_sum) is not 0:
            raise MissingValueError("읽어들인 파일의 값이 잘못되었습니다.")
        # https://cleancode-ws.tistory.com/63 참고 - 결측치 처리

    def check_independent_data_period(self):
        # TODO: linux에서 날짜 xx. x. x로 받아와서 오류 발생 (수정해야함)
        date_index_list = list(self.dataframe.index.strftime("%Y-%m-%d"))
        #print(self.merged_independent.loc[self.start_date:self.end_date, :])
        if str(self.start_date) not in date_index_list:
            #error 발생
            #데이터 양 부족
            raise PeriodError(str(self.start_date) +" is not in dataframe")
        elif str(self.end_date) not in date_index_list:
            # error 발생
            # 데이터 양 부족
            raise PeriodError(str(self.end_date) +" is not in dataframe")
        else:
            print("data OK!")

    def read_excel_files(self): # dataframe(지수)이 필요한가?
        """Read all independent excel files in the independent_path.

        :return:
        self.merged_independent : dataframe, merged all independent excel
                                  files in the independent_path.
        """

        all_csv_files = glob.glob(self.independent_path + '/*.csv')
        for index_, csv_file in enumerate(all_csv_files):
            print("read " + csv_file)
            new_df = pd.read_csv(csv_file, encoding='CP949')
            new_df.iloc[:, 1:] = new_df.iloc[:, 1:].shift(+3)
            new_df = new_df.drop(index=[0, 1, 2, 3])
            # shifting 3-month
            self.check_error(new_df)

            # if index_ is not 0:
            self.dataframe = pd.merge(self.dataframe, new_df, on='Date')

        self.dataframe.set_index('Date', inplace=True)
        self.dataframe = self.dataframe.set_index(pd.to_datetime(self.dataframe.index))
        self.check_independent_data_period()
        # data period check (start_date ~ end_date)

   # def merge_dataframe(self, new_df):
    # 기존 종속변수에 추가하는 방식으로 변경


    def seperate_data(self, columns, condition):
        print(type(self.dataframe.index))
        X_train = self.dataframe.loc[self.start_date:self.seperate_date, :]\
                                [columns]
        y_train = self.dataframe.loc[self.start_date:self.seperate_date, :] \
                                [condition]  # LM4DN   HM4UP
        X_test = self.dataframe.loc[self.seperate_date: ,:] \
                            [columns]# 시작일 +1 해야함
        X_test = X_test.drop(X_test.index[0])
        y_test = self.dataframe.loc[self.seperate_date: ,:]\
                            [condition]
        y_test = y_test.drop(y_test.index[0])

        return X_train, y_train, X_test, y_test

    def calculate_margin(self, condition):

        pre_dataframe = self.dataframe.loc[self.seperate_date:, :]
        pre_dataframe = pre_dataframe.drop(pre_dataframe.index[0])
        pre_dataframe[condition + '_predict'] = self.y_prediction
        if condition == "HM4UP":
            pre_dataframe[condition + '_margin'] = \
                np.where((pre_dataframe[condition + '_predict'] == 1),
                        np.where(pre_dataframe['High'] >= pre_dataframe['Open'] * 1.04,
                        pre_dataframe['Open'] * 0.04,
                        pre_dataframe['Adj Close'] - pre_dataframe['Open']), 0)

        elif condition == "LM4DN":
            pre_dataframe[condition + '_margin'] = \
                np.where((pre_dataframe[condition + '_predict'] == 1),
                         np.where(pre_dataframe['Low'] <= pre_dataframe['Open'] * 0.96,
                                  pre_dataframe['Open'] * 0.04,
                                  -(pre_dataframe['Adj Close'] - pre_dataframe['Open'])), 0)

        closeIncreaseRate = pre_dataframe['Close'].iloc[-2] / pre_dataframe['Close'].iloc[0] - 1
        Margin = float(pre_dataframe[condition + '_margin'].sum() / pre_dataframe['Close'].iloc[0:1])

        pre_dataframe.loc[pre_dataframe.index[-1] + pd.Timedelta(seconds=1), condition + '_predict'] = closeIncreaseRate
        pre_dataframe.loc[pre_dataframe.index[-1] + pd.Timedelta(seconds=1), condition + '_margin'] = Margin
        return pre_dataframe, Margin, closeIncreaseRate

    def save_excel_file(self, dataframe, Classifier, condition, columns):
        dependent_name = self.dependent_path.split("/")
        if Classifier == "KNN":

            dataframe.to_excel(
            self.saved_path + '/' + str(self.n_neighbors) + Classifier + '_'+ dependent_name[-1] + "_" + str(condition) + str(
                columns) + str(self.start_date) + "_" + str(self.seperate_date) + '.xlsx')
        else:
            dataframe.to_excel(
            self.saved_path + '/' + Classifier + '_' + dependent_name[-1] + "_" + str(condition) + str(
                columns) + str(self.start_date) + "_" + str(self.seperate_date) + '.xlsx')

    def get_independent_columns(self):
        independent_columns = list(self.dataframe)
        for i in self.dependent_columns:
            independent_columns.remove(i)
        return independent_columns
