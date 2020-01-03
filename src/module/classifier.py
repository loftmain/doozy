from SA import SA
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

import statsmodels.formula.api as sm
from xgboost import XGBClassifier
from itertools import combinations
import warnings

warnings.filterwarnings('ignore')


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

                copy_dataframe, margin, close_increase_rate = self.calculate_margin(condition)
                result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%} ' \
                              f' margin:{margin: .2%}  close_increase_rate:{close_increase_rate: .2%}\n' \
                              f' {condition}  "RF" {columns}\n'
                print(result_data)
                log.loc[len(log)] = ["RF", condition, columns, accuracy, precision, recall, margin,
                                     close_increase_rate, f'n_estimators={n_estimators} max_depth='
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

                    copy_dataframe, margin, close_increase_rate = self.calculate_margin(condition)
                    result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%} ' \
                                  f' margin:{margin: .2%}  close_increase_rate:{close_increase_rate: .2%}\n' \
                                  f' {condition}  "RF" {columns}\n'
                    print(result_data)
                    log.loc[len(log)] = ["RF", condition, columns, accuracy, precision, recall, margin,
                                         close_increase_rate, f'n_estimators={n_estimators} max_depth='
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

                    pre_dataframe, margin, close_increase_rate = self.calculate_margin(condition)
                    result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%} ' \
                                  f' margin:{margin: .2%}  close_increase_rate:{close_increase_rate: .2%}\n' \
                                  f' {condition}  "n_neighbors" {self.n_neighbors}  "KNN" {columns}\n'
                    print(result_data)
                    log.loc[len(log)] = ["KNN", condition, columns, accuracy, precision, recall, margin,
                                         close_increase_rate, f'n_neighbors={self.n_neighbors}']

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

                        pre_dataframe, margin, close_increase_rate = self.calculate_margin(condition)
                        result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%} ' \
                                      f' margin:{margin: .2%}  close_increase_rate:{close_increase_rate: .2%}\n' \
                                      f' {condition}  "n_neighbors" {self.n_neighbors}  "KNN" {columns}\n'
                        print(result_data)
                        log.loc[len(log)] = ["KNN", condition, columns, accuracy, precision, recall, margin,
                                             close_increase_rate, f'n_neighbors={self.n_neighbors}']


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

                pre_dataframe, margin, close_increase_rate = self.calculate_margin(condition)
                result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%} ' \
                              f' margin:{margin: .2%}  close_increase_rate:{close_increase_rate: .2%}\n' \
                              f' {condition}  "XGboost" {columns}\n'
                print(result_data)
                log.loc[len(log)] = ["XGBOOST", condition, columns, accuracy, precision, recall, margin,
                                     close_increase_rate, f'n_estimators={n_estimators} '
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
                    pre_dataframe, margin, close_increase_rate = self.calculate_margin(condition)
                    result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%} ' \
                                  f' margin:{margin: .2%}  close_increase_rate:{close_increase_rate: .2%}\n' \
                                  f' {condition}  "XGboost" {columns}\n'
                    print(result_data)
                    log.loc[len(log)] = ["XGBOOST", condition, columns, accuracy, precision, recall, margin,
                                         close_increase_rate, f'n_estimators={n_estimators} '
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

                pre_dataframe, margin, close_increase_rate = self.calculate_margin(condition)
                result_data = f'accuracy: {accuracy: .2%} precision: {precision:.2%}  recall:{recall:.2%} ' \
                              f' margin:{margin: .2%}  close_increase_rate:{close_increase_rate: .2%}\n' \
                              f' {condition}  "LR" {columns}\n'
                print(result_data)
                log.loc[len(log)] = ["LR", condition, columns, accuracy, precision, recall, margin,
                                     close_increase_rate, f'None']
                self.save_excel_file(pre_dataframe, "LR", condition, columns)
                """


                    print(result_data)
                    log.loc[len(log)] = ["KNN", condition, columns, accuracy, precision, recall, margin, close_increase_rate]

                    self.save_excel_file(pre_dataframe, "KNN", condition, columns)"""
