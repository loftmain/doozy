# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 16:02:42 2020

@author: giho9
"""

import pandas as pd
import numpy as np
import os

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.feature_selection import RFECV, RFE, SelectKBest, f_classif, chi2
from sklearn.pipeline import Pipeline, make_pipeline

from sklearn.metrics import classification_report, precision_recall_fscore_support
from sklearn.decomposition import PCA
from xgboost import XGBClassifier
from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D
import random

import matplotlib.pyplot as plt
import warnings
from sklearn.exceptions import UndefinedMetricWarning

warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def SearchCV(n_estimators=None, n_features=None, model=None, param=None,
             data=None, features=None, target=None, train_size=None):
    temp = defaultdict()

    for i in range(n_estimators):
        feature = random.sample(list(features), n_features)

        X, y = \
            pd.DataFrame(data, columns=feature), \
            pd.DataFrame(data, columns=[target])

        train_x, train_y, test_x, test_y = \
            X[:train_size], y[:train_size], X[train_size:], y[train_size:]

        gcv=GridSearchCV(model, param_grid=param, scoring='f1')
        
        gcv.fit(train_x, train_y)
        
        pred_y = gcv.predict(test_x)
        report = precision_recall_fscore_support \
        (test_y, pred_y, average='binary', warn_for=tuple())
        # report = score(test_y, pred_y)
        temp[tuple(feature)] = report, gcv.best_params_
    inven = sorted(temp.items(), key=lambda x: x[1][0], reverse=True)

    return inven

def setup(df, path):
    folder = os.listdir(path)

    economy = [pd.read_csv(path + '/' + file) for file in folder]

    for index in economy: df = pd.merge(df, index[index.columns[0::2]], on='Date')

    date = df['Date']

    origin = df[df.columns[:21]]
    index = df[df.columns[21:]].shift(3).dropna(axis=0)

    index['Date'] = date

    dataset = pd.merge(origin, index, on='Date')

    features = df.columns[31:]

    return dataset, features

def STT(dataset=None, 
        train_window_size=None, invest_window_size=None, window_size=None,
        test_size=None, eco_index_sample=None, param_grid=None, target=None):
    
    start = 0

    decision = list()

    for end in range(window_size, len(dataset) - invest_window_size):
        

        train_size = int(len(dataset[start:end]) * test_size)

        clf = KNeighborsClassifier()
        
        best_result = \
            SearchCV(n_estimators=random_sample, n_features=eco_index_sample, model=clf, param=param_grid,
                     data=dataset[start:end], features=features, target=target,
                     train_size=train_size)

        feature = best_result[0][0]
        best_param = best_result[0][1][1]

        X, y = \
            pd.DataFrame(dataset[start:end], columns=feature), \
            pd.DataFrame(dataset[start:end], columns=[target])

        test_x, test_y = \
            pd.DataFrame(dataset[end:end + invest_window_size], columns=feature), \
            pd.DataFrame(dataset[end:end + invest_window_size], columns=[target])

        train_x, train_y = X[:train_size], y[:train_size]

        clf = KNeighborsClassifier(n_neighbors=best_param['n_neighbors'])

        clf.fit(train_x, train_y)
        pred_y = clf.predict(test_x)

        start += 1
        score = precision_recall_fscore_support \
        (test_y, pred_y, average='binary', warn_for=tuple())
        pre, rec, fs, xxx = score
        
        decision.append((feature, score, pred_y, list(test_y.index)))
        print('###[', start, ']###')
        print('테스트 결과')
        print(feature)
        print('precision :', best_result[0][1][0][0])
        print('recall :', best_result[0][1][0][1])
        print('f1 score :', best_result[0][1][0][2])
        print('투자예측 결과')
        print('precision :', pre)
        print('recall :', rec)
        print('f1 score :', fs)
        print('')
        
    q = list(np.array(decision).T[2])
    w = list(np.array(decision).T[3])

    emp = np.full((len(dataset), len(decision)), np.nan)

    count = 0

    for a, s in zip(q, w):
        
        for index in range(invest_window_size):
            emp[s[index]][count] = a[index]
        
        count += 1

    result = list()

    count = 0

    for ele in emp:
        if (ele == 0).sum() >= int(invest_window_size/2) + 1:
            result.append(0)
        elif (ele == 1).sum() >= int(invest_window_size/2) + 1:
            result.append(1)
        else:
            result.append(0)

    dataset['predict'] = result
    
    dataset = dataset[window_size+invest_window_size:]
    dataset['vote'] = np.array(decision).T[2]
    dataset['score'] = np.array(decision).T[1]
    dataset['feature'] = np.array(decision).T[0]
    
    report = precision_recall_fscore_support \
    (dataset[target], dataset['predict'], average='binary', warn_for=tuple())
    
    print('###[실전투자예측]###')
    print('precision :', report[0])
    print('recall :', report[1])
    print('f1 score :', report[2])
    
    return dataset, report

if __name__ == '__main__':
    # 지수파일 경로
    
    targets = ['LM4DN']
    
    for target in targets:
        
        df = pd.read_csv('save/marking/^DJI.csv')
    
        # 경제지표가 들어있는 폴더 이름
        folder = 'independent'
    
        # target column name
    
        dataset, features = setup(df, folder)
    
        train_window_size = 60
        invest_window_size = 12
        window_size = train_window_size + invest_window_size
        
        test_size = 0.8
    
        # 경제지표 갯수
        eco_index_sample = 87
        
        # 랜덤 샘플 개수
        random_sample = 1
    
        model = 'KNN'
        param_grid = {'n_neighbors' : [3,5,7]}


        dataset, report = STT(dataset, train_window_size, invest_window_size, window_size,
                      test_size, eco_index_sample, param_grid, target)
        
        dataset.to_csv(model + '_' + target + str(report) + '.csv', index=False)