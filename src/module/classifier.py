from src.module.SA import SA
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import os
import statsmodels.formula.api as sm
from xgboost import XGBClassifier
from itertools import combinations
import warnings
import datetime
import pandas as pd
warnings.filterwarnings('ignore')

def check_column_option(setting):
    if 'column_list' in setting["column_option_list"]:
        column_list = setting["column_option_list"]['column_list']
    else:
        column_list = None
    return column_list

def check_setting_file(setting):
    if not os.path.exists(setting["independent_path"]):
        raise FileNotFoundError(setting["independent_path"])
    if not os.path.exists(setting["dependent_file_path"]):
        raise FileNotFoundError(setting["dependent_file_path"])
    if not os.path.exists(setting["save_path"]):
        raise FileNotFoundError(setting["save_path"])


def check_classifier(setting, log_data):
    column_list = check_column_option(setting)

    if setting["classifier"] == "RF":
        # check option : HM4UP 과 같은 옵션 구별
        # coulums check : 컬럼설정한것 구별할 함수 있어야함
        # independent path 만 주고서 dataframe 파라미터를 빼도 될거 같음
        # type에 kospi 와 같은 것 넣는 이유 = save 시에 이름에 넣기 위해서
        #
        rf = SA_Randomforest(
            column_list=column_list,
            condition_list=setting["condition_list"],
            dependent_path=setting["dependent_file_path"],
            independent_path=setting["independent_path"],
            saved_path=setting["save_path"],
            start_date=setting["start_date"],
            seperate_date=setting["seperate_date"],
            end_date=setting["end_date"])

        if setting["column_option_list"]['option'] == "subset":
            rf.analyze(log=log_data,
                       n_estimators=setting["type_option_list"]["n_estimators"],
                       max_depth=int(setting["type_option_list"]["max_depth"]),
                       random_state=int(setting["type_option_list"]["random_state"])
                       )

        elif setting["column_option_list"]['option'] == "all":
            rf.analyze_auto(log=log_data,
                            range_of_column_no=setting["column_option_list"]["range_of_column_no"],
                            n_estimators=setting["type_option_list"]["n_estimators"],
                            max_depth=setting["type_option_list"]["max_depth"],
                            random_state=setting["type_option_list"]["random_state"])
        else:
            print("columns list option ERROR!!!")

    elif setting["classifier"] == "KNN":
        knn = SA_Knn(
            column_list=column_list,
            condition_list=setting["condition_list"],
            dependent_path=setting["dependent_file_path"],
            independent_path=setting["independent_path"],
            saved_path=setting["save_path"],
            start_date=setting["start_date"],
            seperate_date=setting["seperate_date"],
            end_date=setting["end_date"])

        if setting["column_option_list"]['option'] == "subset":
            knn.analyze(n_neighbors_list=setting["type_option_list"]["n_neighbors_list"],
                        log=log_data)

        elif setting["column_option_list"]['option'] == "all":
            knn.analyze_auto(log=log_data,
                             n_neighbors_list=setting["type_option_list"]["n_neighbors_list"],
                             range_of_column_no=setting["column_option_list"]["range_of_column_no"])
        else:
            print("columns list option ERROR!!!")

    elif setting["classifier"] == "LR":
        print("LR")
        lr = SA_LinearRegression(
            column_list=column_list,
            condition_list=setting["condition_list"],
            dependent_path=setting["dependent_file_path"],
            independent_path=setting["independent_path"],
            saved_path=setting["save_path"],
            start_date=setting["start_date"],
            seperate_date=setting["seperate_date"],
            end_date=setting["end_date"])

        if setting["column_option_list"]['option'] == "subset":
            lr.analyze(log=log_data)
        elif setting["column_option_list"]['option'] == "all":
            print("구현예정")

    elif setting["classifier"] == "xgboost":
        print("XGBoost")
        xgb = SA_xgboost(
            column_list=column_list,
            condition_list=setting["condition_list"],
            dependent_path=setting["dependent_file_path"],
            independent_path=setting["independent_path"],
            saved_path=setting["save_path"],
            start_date=setting["start_date"],
            seperate_date=setting["seperate_date"],
            end_date=setting["end_date"])

        if setting["column_option_list"]['option'] == "subset":
            xgb.analyze(log=log_data, n_estimators=100, min_child_weight=1, max_depth=8, gamma=0)

        elif setting["column_option_list"]['option'] == "all":
            xgb.analyze_auto(log=log_data,
                             range_of_column_no=setting["column_option_list"]["range_of_column_no"],
                             n_estimators=100, min_child_weight=1, max_depth=8, gamma=0)
        else:
            print("columns list option ERROR!!!")
    else:
        print("not right type!!")

class SA_Randomforest(SA):
    def __init__(self,
                 condition_list,
                 dependent_path,
                 independent_path,
                 saved_path,
                 start_date,
                 seperate_date,
                 end_date,
                 column_list=None):
        super().__init__(
            condition_list,
            dependent_path,
            independent_path,
            saved_path,
            start_date,
            seperate_date,
            end_date,
            column_list)

    def analyze(self, log, n_estimators=100, max_depth=8, random_state=0):
        super().read_excel_files()
        for columns in self.column_list:
            for condition in self.condition_list:
                X_train, y_train, X_test, y_test = super().seperate_data(columns, condition)

                random_clf = RandomForestClassifier(n_estimators=n_estimators,
                                                    n_jobs=-1, max_depth=max_depth,
                                                    random_state=random_state)

                random_clf.fit(X_train, np.ravel(y_train))
                self.y_prediction = random_clf.predict(X_test)
                accuracy = accuracy_score(y_test, self.y_prediction)
                precision = precision_score(y_test, self.y_prediction)
                recall = recall_score(y_test, self.y_prediction)

                copy_dataframe = self.dataframe.loc[self.seperate_date:, :]
                copy_dataframe = copy_dataframe.drop(copy_dataframe.index[0])
                copy_dataframe[condition + '_predict'] = self.y_prediction
                result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%}\n ' \
                              f' {condition}  "RF" {columns}\n'
                print(result_data)
                log.loc[len(log)] = ["RF", condition, columns, accuracy, precision, recall,
                                      f'n_estimators={n_estimators} max_depth='
                                                          f'{max_depth} random_state={random_state}']
                self.save_excel_file(copy_dataframe, "RF", condition, columns)

    def analyze_auto(self, log, range_of_column_no, n_estimators=100, max_depth=None, random_state=0):
        super().read_excel_files()
        number_of_case_columns = self.get_independent_columns()
        X_train, y_train, X_test, y_test = super().seperate_data(number_of_case_columns, self.condition_list)
        print(range_of_column_no)
        for column_count in range(range_of_column_no[0], range_of_column_no[1]):
            print(column_count, end=' ')
            column_list_index = list(combinations(number_of_case_columns, column_count))

            for condition in self.condition_list:

                for columns in column_list_index:
                    random_clf = RandomForestClassifier(n_estimators=n_estimators,
                                                        n_jobs=-1, max_depth=max_depth,
                                                        random_state=random_state)
                    random_clf.fit(X_train[list(columns)], y_train[condition])
                    self.y_prediction = random_clf.predict(X_test[list(columns)])
                    accuracy = accuracy_score(y_test[condition], self.y_prediction)
                    precision = precision_score(y_test[condition], self.y_prediction)
                    recall = recall_score(y_test[condition], self.y_prediction)

                    copy_dataframe = self.dataframe.loc[self.seperate_date:, :]
                    copy_dataframe = copy_dataframe.drop(copy_dataframe.index[0])
                    copy_dataframe[condition + '_predict'] = self.y_prediction
                    result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%}\n ' \
                                  f' {condition}  "RF" {columns}\n'
                    print(result_data)
                    log.loc[len(log)] = ["RF", condition, columns, accuracy, precision, recall,
                                          f'n_estimators={n_estimators} max_depth='
                                                              f'{max_depth} random_state={random_state}']

                    # self.save_excel_file(copy_dataframe, "RF", condition, columns)


"""
                    if (precision >= 0.4) & (recall >= 0.3):
                        copyFrame = frame[frame['DATE'] > turnoutDay]
                        margin, closeIncreaseRate, copyFrame = cal_margin(cm, copyFrame, y_pred)
                        if margin >= 0.2:
                            save_excel(copyFrame, margin, precision, recall, cm, column, startDay, turnoutDay, 'good')
                        elif margin >= 0.15:
                            save_excel(copyFrame, margin, precision, recall, cm, column, startDay, turnoutDay, 'normal')
"""


class SA_Knn(SA):
    def __init__(self,
                 condition_list,
                 dependent_path,
                 independent_path,
                 saved_path,
                 start_date,
                 seperate_date,
                 end_date,
                 column_list=None):
        super().__init__(
            condition_list,
            dependent_path,
            independent_path,
            saved_path,
            start_date,
            seperate_date,
            end_date,
            column_list)

    def analyze(self, n_neighbors_list, log):
        super().read_excel_files()
        for columns in self.column_list:
            for condition in self.condition_list:
                X_train, y_train, X_test, y_test = super().seperate_data(columns, condition)
                for self.n_neighbors in n_neighbors_list:
                    clf = neighbors.KNeighborsClassifier(self.n_neighbors)
                    clf.fit(X_train, np.ravel(y_train))
                    y_prediction = clf.predict(X_test)
                    self.y_prediction = y_prediction
                    # classification, fiting, output the predicted value
                    accuracy = accuracy_score(y_test, self.y_prediction)
                    precision = precision_score(y_test, self.y_prediction)
                    recall = recall_score(y_test, self.y_prediction)

                    pre_dataframe = self.dataframe.loc[self.seperate_date:, :]
                    pre_dataframe = pre_dataframe.drop(pre_dataframe.index[0])
                    pre_dataframe[condition + '_predict'] = self.y_prediction
                    result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%} ' \
                                  f'\n' \
                                  f' {condition}  "n_neighbors" {self.n_neighbors}  "KNN" {columns}\n'
                    print(result_data)
                    log.loc[len(log)] = ["KNN", condition, columns, accuracy, precision, recall,
                                          f'n_neighbors={self.n_neighbors}']

                    self.save_excel_file(pre_dataframe, "KNN", condition, columns)

    def analyze_auto(self, log, range_of_column_no, n_neighbors_list):
        super().read_excel_files()
        number_of_case_columns = self.get_independent_columns()
        X_train, y_train, X_test, y_test = super().seperate_data(number_of_case_columns, self.condition_list)
        for column_count in range(range_of_column_no[0], range_of_column_no[1]):
            print(column_count, end=' ')
            column_list_index = list(combinations(number_of_case_columns, column_count))

            for condition in self.condition_list:
                for self.n_neighbors in n_neighbors_list:
                    for columns in column_list_index:
                        clf = neighbors.KNeighborsClassifier(self.n_neighbors)
                        clf.fit(X_train[list(columns)], np.ravel(y_train[condition]))
                        y_prediction = clf.predict(X_test[list(columns)])
                        self.y_prediction = y_prediction
                        # classification, fiting, output the predicted value
                        accuracy = accuracy_score(y_test[condition], self.y_prediction)
                        precision = precision_score(y_test[condition], self.y_prediction)
                        recall = recall_score(y_test[condition], self.y_prediction)

                        pre_dataframe = self.dataframe.loc[self.seperate_date:, :]
                        pre_dataframe = pre_dataframe.drop(pre_dataframe.index[0])
                        pre_dataframe[condition + '_predict'] = self.y_prediction
                        result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%} ' \
                                      f' \n' \
                                      f' {condition}  "n_neighbors" {self.n_neighbors}  "KNN" {columns}\n'
                        print(result_data)
                        log.loc[len(log)] = ["KNN", condition, columns, accuracy, precision, recall,
                                             f'n_neighbors={self.n_neighbors}']


class SA_xgboost(SA):
    def __init__(self,
                 condition_list,
                 dependent_path,
                 independent_path,
                 saved_path,
                 start_date,
                 seperate_date,
                 end_date,
                 column_list=None):
        super().__init__(
            condition_list,
            dependent_path,
            independent_path,
            saved_path,
            start_date,
            seperate_date,
            end_date,
            column_list)

    def analyze(self, log, n_estimators=100, min_child_weight=1, max_depth=8, gamma=0):
        super().read_excel_files()
        for columns in self.column_list:
            for condition in self.condition_list:
                X_train, y_train, X_test, y_test = super().seperate_data(columns, condition)
                sc = StandardScaler()
                sc.fit(X_train)
                X_train_std = sc.transform(X_train)
                X_test_std = sc.transform(X_test)

                ml = XGBClassifier(n_estimators=n_estimators,
                                   min_child_weight=min_child_weight,
                                   max_depth=max_depth,
                                   gamma=gamma)
                ml.fit(X_train_std, y_train)
                self.y_prediction = ml.predict(X_test_std)

                accuracy = accuracy_score(y_test, self.y_prediction)
                recall = recall_score(y_test, self.y_prediction)
                precision = precision_score(y_test, self.y_prediction)

                pre_dataframe = self.dataframe.loc[self.seperate_date:, :]
                pre_dataframe = pre_dataframe.drop(pre_dataframe.index[0])
                pre_dataframe[condition + '_predict'] = self.y_prediction
                result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%}\n ' \
                              f' {condition}  "XGboost" {columns}\n'
                print(result_data)
                log.loc[len(log)] = ["XGBOOST", condition, columns, accuracy, precision, recall,
                                      f'n_estimators={n_estimators} '
                                                          f'min_child_weight={min_child_weight} '
                                                          f'max_depth={max_depth} gamma={gamma}']

                self.save_excel_file(pre_dataframe, "xgboost", condition, columns)

    def analyze_auto(self, log, range_of_column_no, n_estimators=100, min_child_weight=1, max_depth=8, gamma=0):
        super().read_excel_files()
        number_of_case_columns = self.get_independent_columns()
        X_train, y_train, X_test, y_test = super().seperate_data(number_of_case_columns, self.condition_list)
        print(range_of_column_no)
        for column_count in range(range_of_column_no[0], range_of_column_no[1]):
            print(column_count, end=' ')
            column_list_index = list(combinations(number_of_case_columns, column_count))

            for condition in self.condition_list:

                for columns in column_list_index:
                    sc = StandardScaler()
                    sc.fit(X_train[list(columns)])
                    X_train_std = sc.transform(X_train[list(columns)])
                    X_test_std = sc.transform(X_test[list(columns)])

                    ml = XGBClassifier(n_estimators=n_estimators,
                                       min_child_weight=min_child_weight,
                                       max_depth=max_depth,
                                       gamma=gamma)
                    ml.fit(X_train_std, y_train[condition])
                    self.y_prediction = ml.predict(X_test_std)

                    accuracy = accuracy_score(y_test[condition], self.y_prediction)
                    recall = recall_score(y_test[condition], self.y_prediction)
                    precision = precision_score(y_test[condition], self.y_prediction)
                    pre_dataframe = self.dataframe.loc[self.seperate_date:, :]
                    pre_dataframe = pre_dataframe.drop(pre_dataframe.index[0])
                    pre_dataframe[condition + '_predict'] = self.y_prediction
                    result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%}\n ' \
                                  f' {condition}  "XGboost" {columns}\n'
                    print(result_data)
                    log.loc[len(log)] = ["XGBOOST", condition, columns, accuracy, precision, recall,
                                          f'n_estimators={n_estimators} '
                                                              f'min_child_weight={min_child_weight} '
                                                              f'max_depth={max_depth} gamma={gamma}']

                    # self.save_excel_file(pre_dataframe, "xgboost", condition, columns)
                    """

"""


class SA_LinearRegression(SA):
    def __init__(self,
                 condition_list,
                 dependent_path,
                 independent_path,
                 saved_path,
                 start_date,
                 seperate_date,
                 end_date,
                 column_list=None):
        super().__init__(
            condition_list,
            dependent_path,
            independent_path,
            saved_path,
            start_date,
            seperate_date,
            end_date,
            column_list)

    def analyze(self, log):
        super().read_excel_files()
        for columns in self.column_list:
            for condition in self.condition_list:
                columns.append(condition)
                X_train, y_train, X_test, y_test = super().seperate_data(columns, condition)

                columns.remove(condition)
                print(condition + ' ~' + '+'.join(columns))
                model = sm.ols(formula=condition + ' ~' + '+'.join(columns),
                               data=X_train).fit()
                y_predict = model.predict(X_test)
                r_square = model.rsquared
                print('R-SQUARE:', r_square)
                print('Pvalue :', model.pvalues)
                self.y_prediction = y_predict.apply(lambda x: 0 if x < 0.5 else 1)
                accuracy = accuracy_score(y_test, self.y_prediction)
                precision = precision_score(y_test, self.y_prediction)
                recall = recall_score(y_test, self.y_prediction)

                pre_dataframe = self.dataframe.loc[self.seperate_date:, :]
                pre_dataframe = pre_dataframe.drop(pre_dataframe.index[0])
                pre_dataframe[condition + '_predict'] = self.y_prediction
                result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%}\n ' \
                              f' {condition}  "LR" {columns}\n'
                print(result_data)
                log.loc[len(log)] = ["LR", condition, columns, accuracy, precision, recall,
                                      f'None']
                self.save_excel_file(pre_dataframe, "LR", condition, columns)
                """


                    print(result_data)
                    log.loc[len(log)] = ["KNN", condition, columns, accuracy, precision, recall, margin, close_increase_rate]

                    self.save_excel_file(pre_dataframe, "KNN", condition, columns)"""


if __name__ == '__main__':
    opt0 = 'KNN'
    opt1 = [3, 5, 7]
    opt2 = 'subset'
    opt3 = [['BAArate', 'HOUSTrate', 'DGORDERrate']]
    opt4 = ['HM3UP']
    opt5 = 'dependent/^DJI.xlsx'
    opt6 = 'independent'
    opt7 = 'save'
    opt8 = [2015, 1, 1]
    opt9 = [2018, 1, 1]
    opt10 = [2019, 4, 1]
    # =============================================================================
    #     KNN
    # =============================================================================
    if opt0 == 'KNN':
        if opt2 == 'subset':
            start_setting = \
                {'setting':
                    [
                        {
                            'classifier': opt0,
                            'type_option_list': {'n_neighbors_list': opt1},
                            'column_option_list': {'option': opt2, 'column_list': opt3},
                            'condition_list': opt4,
                            'dependent_file_path': opt5,
                            'independent_path': opt6,
                            'save_path': opt7,
                            'start_date': datetime.date(opt8[0], opt8[1], opt8[2]),
                            'seperate_date': datetime.date(opt9[0], opt9[1], opt9[2]),
                            'end_date': datetime.date(opt10[0], opt10[1], opt10[2])
                        }
                    ]
                }
        if opt2 == 'all':
            start_setting = \
                {'setting':
                    [
                        {
                            'classifier': opt0,
                            'type_option_list': {'n_neighbors_list': opt1},
                            'column_option_list': {'option': opt2, 'range_of_column_no': opt3},
                            'condition_list': opt4,
                            'dependent_file_path': opt5,
                            'independent_path': opt6,
                            'save_path': opt7,
                            'start_date': datetime.date(opt8[0], opt8[1], opt8[2]),
                            'seperate_date': datetime.date(opt9[0], opt9[1], opt9[2]),
                            'end_date': datetime.date(opt10[0], opt10[1], opt10[2])
                        }
                    ]
                }
    # =============================================================================
    #     RANDOM FOREST
    # =============================================================================
    if opt0 == 'RF':
        if opt2 == 'subset':
            start_setting = \
                {'setting':
                    [
                        {
                            'classifier': opt0,
                            'type_option_list': {'n_estimators': opt1[0],
                                                 'max_depth': opt1[1],
                                                 'random_state': opt1[2]},
                            'column_option_list': {'option': opt2, 'column_list': opt3},
                            'condition_list': opt4,
                            'dependent_file_path': opt5,
                            'independent_path': opt6,
                            'save_path': opt7,
                            'start_date': datetime.date(opt8[0], opt8[1], opt8[2]),
                            'seperate_date': datetime.date(opt9[0], opt9[1], opt9[2]),
                            'end_date': datetime.date(opt10[0], opt10[1], opt10[2])
                        }
                    ]
                }
        if opt2 == 'all':
            start_setting = \
                {'setting':
                    [
                        {
                            'classifier': opt0,
                            'type_option_list': {'n_estimators': opt1[0],
                                                 'max_depth': opt1[1],
                                                 'random_state': opt1[2]},
                            'column_option_list': {'option': opt2, 'range_of_column_no': opt3},
                            'condition_list': opt4,
                            'dependent_file_path': opt5,
                            'independent_path': opt6,
                            'save_path': opt7,
                            'start_date': datetime.date(opt8[0], opt8[1], opt8[2]),
                            'seperate_date': datetime.date(opt9[0], opt9[1], opt9[2]),
                            'end_date': datetime.date(opt10[0], opt10[1], opt10[2])
                        }
                    ]
                }
    # =============================================================================
    #     XGBOOST
    # =============================================================================
    if opt0 == 'xgboost':
        if opt2 == 'subset':
            start_setting = \
                {'setting':
                    [
                        {
                            'classifier': opt0,
                            'type_option_list': {'n_estimators': opt1[0],
                                                 'min_child_weight': opt1[1],
                                                 'max_depth': opt1[2],
                                                 'gamma': opt1[3]},
                            'column_option_list': {'option': opt2, 'column_list': opt3},
                            'condition_list': opt4,
                            'dependent_file_path': opt5,
                            'independent_path': opt6,
                            'save_path': opt7,
                            'start_date': datetime.date(opt8[0], opt8[1], opt8[2]),
                            'seperate_date': datetime.date(opt9[0], opt9[1], opt9[2]),
                            'end_date': datetime.date(opt10[0], opt10[1], opt10[2])
                        }
                    ]
                }
        if opt2 == 'all':
            start_setting = \
                {'setting':
                    [
                        {
                            'classifier': opt0,
                            'type_option_list': {'n_estimators': opt1[0],
                                                 'min_child_weight': opt1[1],
                                                 'max_depth': opt1[2],
                                                 'gamma': opt1[3]},
                            'column_option_list': {'option': opt2, 'range_of_column_no': opt3},
                            'condition_list': opt4,
                            'dependent_file_path': opt5,
                            'independent_path': opt6,
                            'save_path': opt7,
                            'start_date': datetime.date(opt8[0], opt8[1], opt8[2]),
                            'seperate_date': datetime.date(opt9[0], opt9[1], opt9[2]),
                            'end_date': datetime.date(opt10[0], opt10[1], opt10[2])
                        }
                    ]
                }

    log_data = pd.DataFrame(columns=['classifier', 'condition', 'columns', 'accuracy',
                                     'precision', 'recall', 'option'])
    for setting in start_setting['setting']:
        check_setting_file(setting)
        check_classifier(setting, log_data)
        print('-----------------------------------------------------------------')
    log_data.to_excel('log_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx')
