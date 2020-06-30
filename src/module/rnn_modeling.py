# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 22:02:27 2020

@author: shyoo
"""


class RNN_modeling:
    '''

    deep learning의 rnn기반 LSTM 알고리즘으로 이진 분류 모델을 생성하고 예측값을 생성한다.

    사용 예시
    ----------

    >>> import pandas as pd

    >>> folder = 'independent'
    # 경제지표들이 들어있는 폴더 경로

    >>> feature_list = ['BAArate', 'NEWORDERrate', 'T10Y2YMrate']
    # 예측에 사용할 경제지표 목록

    >>> target_list = ['HM4UP']
    # 예측할 레이블 타겟

    >>> data = pd.read_csv('dependent/^DJI.csv')
    # 지수파일 읽어오기

    >>> train_size = int(len(data) * 0.7)
    # 트레이닝 사이즈

    >>> mod = RNN_modeling()
    # 클래스 선언

    >>> mod.set_option(feature_list, target_list, train_size)
    # 옵션 설정
    # 경제지표 목록, 레이블 타겟, 트레이닝 사이즈

    >>> mod.set_model_option(40, 'relu', 'sigmoid', 200)
    # LSTM 모델 옵션 설정
    # 입력층과 은닉층 레이어 사이즈, 입력층과 은닉층 활성화 함수
    # 출력층 활성화 함수, 에포크 사이즈

    >>> mod.merge_data(data, folder, 'rate', 3)
    #     # 지수데이터와 경제지표 데이터가 모두 들어있는 데이터셋(데이터프레임)을 만듬
    #     # 지수데이터 데이터프레임, 경제지표가 들어있는 폴더 경로
    #     # 경제지표에서 어떤 정규화 데이터를 쓸것인지
    #     # data shifting value는 얼마인지
    #
    #     >>> predict, scoring = mod.modeling()
    #     # 모델링 진행, 예측값과 스코어 리턴

    >>> res = data[:-3][-35:]
    >>> res['predicted'] = predict
    # 지수 데이터프레임에 예측값 추가

    >>> res.to_csv('save/modeling/RNN'+str(scoring)+'.csv', header=True, index=False)
    # csv파일 생성
    '''

    def set_option(self, feature, target, tsize):
        '''
        클래스 멤버변수를 설정하는 함수이다.

        Parameters
        ----------
        feature : list

            사용할 경제지표

            예 : ['BAA', 'HOUST', 'NEWORDER']

        target : list

            타겟이 될 레이블

            예 : ['HM4UP']
                 ['LM4DN']

        Returns
        -------
        None

        '''
        self._feature = feature
        self._target = target
        self._tsize = tsize

    def set_model_option(self, layer, ihfx, ofx, epo):
        '''
        LSTM RNN 모델의 옵션을 설정하는 함수이다.

        Parameters
        ----------
        feature : int

            입력층과 은닉층의 레이어 사이즈이다.

            예 : 64

        feature : str


            입력층과 은닉층의 활성화 함수이다.

            예 : relu, elu, selu, softplus, softsign

        feature : str

            출력층의 활성화 함수이다.

            예 : softmax, linear, sigmoid


        feature : int

            에포크(학습 횟수)이다.
            적절한 epoch 값 설정을 해야 언더피팅과 오버피팅을 방지할 수 있다.

            예 : 200,300,500

        Returns
        -------
        None

        '''

        self._layer = layer
        self._ihfx = ihfx
        self._ofx = ofx
        self._epo = epo

    def score(self, ty, py):
        '''
        예측값과 실제값으로 정확도, 정밀도, 재현율을 계산한다.

        LSTM RNN 모델의 옵션을 설정하는 함수이다.

        Parameters
        ----------
        ty : list

            실제값인 test_y이다.

            예 : 1,0,1,0,1,1,1,0,0

        feature : list

            예측값인 pred_y이다.

            예 : 1,0,1,0,1,1,1,0,0


        Returns
        -------
        None

        '''

        tp, fp, fn, tn = 0, 0, 0, 0
        for x, y in zip(ty, py):
            if y == 1 and x == 1: tp += 1
            if y == 1 and x == 0: fp += 1
            if y == 0 and x == 1: fn += 1
            if y == 0 and x == 0: tn += 1

        try:
            acc = round((tp + tn) / len(py), 3)
            pre = round(tp / (tp + fp), 3)
            rec = round(tp / (tp + fn), 3)
        except(ZeroDivisionError):
            return 0, 0, 0

        return acc, pre, rec

    def merge_data(self, df, path, normal, value):
        '''
        지수데이터와 경제지표 데이터가 모두 들어있는 데이터셋을 만든다.

        Parameters
        ----------
        df : dataframe

            지수데이터가 들어있는 데이터프레임이다.

            예 :

        feature : str

            경제지표 데이터(csv파일)들이 들어있는 폴더(경로)이름이다.

            예 : 'independent'

        normal : str

            경제지표 데이터에서 어떤 정규화 데이터를 쓸것인가에 대한 옵션이다.

            예 : 'independent'

        value: int

            data shifting value이다.

            예 : 1 or 2 or 3

        Returns
        -------
        None

        '''

        import pandas as pd
        import os

        point = len(df.columns)

        folder = os.listdir(path)

        for i, v in enumerate(folder):
            folder[i] = v.replace('.csv', '')

        economy = [pd.read_csv(path + '/' + file + '.csv') for file in folder]

        for i1, i2 in zip(economy, folder):
            df = pd.merge(df, i1[['Date', i2 + normal]], on='Date')

        date = df['Date']

        origin = df[df.columns[:point]]
        index = df[df.columns[point:]].shift(value).dropna(axis=0)

        index['Date'] = date

        dataset = pd.merge(origin, index, on='Date')

        self._dataset = dataset

    def modeling(self):
        '''
        LSTM 알고리즘으로 이진 분류 모델을 생성하고 예측값을 생성한다.

        Parameters
        ----------
        self: class


        Returns
        -------
        y_pred_class :

            예측값이 들어있는 리스트이다.

            예 : 1,0,0,0,0,0,1,0,0,1,1,0,0,1

        report :

            정확도, 정밀도, 재현율 점수이다.

            예 : (0.762, 0.81, 0.617)

        '''

        import numpy as np
        import pandas as pd

        from keras.models import Sequential
        from keras.layers import LSTM, Dense
        from sklearn.preprocessing import LabelEncoder

        X, y = \
            np.array(pd.DataFrame(self._dataset, columns=self._feature)), \
            np.array(pd.DataFrame(self._dataset, columns=self._target))

        encoder = LabelEncoder()
        y1 = encoder.fit_transform(y)
        y = pd.get_dummies(y1).values

        train_x, train_y, test_x, test_y = \
            X[:self._tsize], y[:self._tsize], X[self._tsize:], y[self._tsize:]

        train_x = \
            train_x.reshape(
                train_x.shape[0], len(self._feature), len(self._target))

        test_x = \
            test_x.reshape(
                test_x.shape[0], len(self._feature), len(self._target))

        model = Sequential()

        model.add(LSTM(
            self._layer, input_shape=(
                len(self._feature), len(self._target)), activation='relu'))

        model.add(Dense(self._layer, activation='relu'))
        model.add(Dense(len(self._target) + 1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy',
                      # model.compile(loss='categorical_crossentropy',
                      optimizer='Adam',
                      metrics=['accuracy'])

        model.summary()

        model.fit(
            train_x, train_y, validation_data=(
                test_x, test_y), epochs=self._epo, verbose=4)

        y_pred = model.predict(test_x)
        y_test_class = np.argmax(test_y, axis=1)
        y_pred_class = np.argmax(y_pred, axis=1)

        report = self.score(y_test_class, y_pred_class)

        return y_pred_class, report


if __name__ == "__main__":
    import pandas as pd

    folder = 'independent'

    feature_list = ['BAArate', 'NEWORDERrate', 'T10Y2YMrate']

    target_list = ['HM4UP']

    data = pd.read_csv('dependent/^DJI.csv')

    train_size = int(len(data) * 0.7)

    mod = RNN_modeling()

    mod.set_option(feature_list, target_list, train_size)

    mod.set_model_option(40, 'relu', 'sigmoid', 200)

    mod.merge_data(data, folder, 'rate', 3)

    predict, scoring = mod.modeling()

    res = data[:-3][-35:]
    res['predicted'] = predict

    res.to_csv('save/modeling/RNN' + str(scoring) + '.csv', header=True, index=False)
