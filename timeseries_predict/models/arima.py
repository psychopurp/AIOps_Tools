

import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import datetime
import pandas as pd


class ARIMAModel:
    '''
    ts: pandas series对象 
    index为DatetimeIndex
    value 为 int
    '''

    def __init__(self, ts, test_size=1440, predict_size=60, period=1440):
        '''
        传入需要训练的数据
        数据分成训练集和测试集
        并将数据进行分解
        predict_size为预测时长 min
        '''
        self.test_size = test_size
        self.ts = ts
        self.train_set = ts[:-test_size if test_size > 0 else len(ts)]
        self.predict_size = predict_size
        self.__decompose(period=period)

    def __decompose(self, period=1440):
        '''
         将训练数据进行分解
         :param :period单位为minute
        '''
        decomposition = seasonal_decompose(
            self.train_set, period=1440, two_sided=False)
        self.trend = decomposition.trend
        self.trend.dropna(inplace=True)
        self.seasonal = decomposition.seasonal
        self.residual = decomposition.resid
        return decomposition

    def __trend_model(self, order):
        '''
        对趋势部分单独用ARIMA模型做训练
        order tuple(p,d,q)
        '''

        self.trend_model = ARIMA(self.trend, order).fit(
            disp=-1, method='css-mle')

    def get_order(self, ts):
        '''
        获取ARIMA模型的参数 p , q , d
        return order(p,d,q)
        '''
        aic = sm.tsa.arma_order_select_ic(ts, max_ar=6, max_ma=4, ic='aic')[
            'aic_min_order']
        return (aic[0], 0, aic[1])

    def ADF_test(self, ts=None):
        '''
        ADF检验
        :param ts
        :return bool 是否平稳
        数据平稳性检测，具有平稳性的数据可以用ARIMA模型进行检测
        #返回值依次为adf、pvalue、usedlag、nobs、critical values、icbest、regresults、resstore
        单位根统计量对应的p的值显著大于0.05，最终判断该序列是非平稳序列的（非平稳不一定不是白噪声）
        '''
        result = adfuller(ts if ts else self.ts)
        return result[1] <= 0.05

    def __predict_trend(self):
        '''
        预测趋势新数据

        '''
        # 预测时间长度
        n = self.predict_size
        # 从训练数据的最后开始预测
        lastTime = self.trend.index[-1]
        start_index = lastTime
        end_index = start_index+datetime.timedelta(minutes=n)
        self.trend_predict = self.trend_model.predict(
            start=start_index, end=end_index)
        # self.add_season()

    def __add_season(self):
        '''
        为预测出的趋势数据添加周期数据和残差数据
        '''
        values = []
        low_conf_values = []
        high_conf_values = []
        d = self.residual.describe()
        delta = d['75%'] - d['25%']
        low_error, high_error = (d['25%'] - 1 * delta, d['75%'] + 1 * delta)
        for i, t in enumerate(self.trend_predict):
            trend_part = t
            # 相同时间点的周期数据均值
            season_part = self.seasonal[self.seasonal.index.time ==
                                        self.trend_predict.index[i].time()].mean()

            predict = trend_part+season_part
            low_bound = predict+low_error
            high_bound = predict + high_error

            values.append(predict)
            low_conf_values.append(low_bound)
            high_conf_values.append(high_bound)

        self.final_pred = pd.Series(
            values, index=self.trend_predict.index, name='predict')
        self.low_conf = pd.Series(
            low_conf_values, index=self.trend_predict.index, name='low')
        self.high_conf = pd.Series(
            high_conf_values, index=self.trend_predict.index, name='high')
        return (self.final_pred, self.low_conf, self.high_conf)

    def train(self, order=None):
        '''
        训练出数据模型，并返回模型使用的参数
        '''
        import logging

        # 获取一个logger对象
        logger = logging.getLogger(__name__)
        # 获取模型训练参数 (p,d,q)
        if not order:
            logger.warning("模型参数训练")
            order = self.get_order(self.trend)

        logger.warning("模型参数为：{}  开始训练".format(order))
        # 训练趋势模型
        try:
            self.__trend_model(order)
        except Exception as e:
            logger.warning("模型训练失败 {}".format(e))
            self.ts.to_csv(
                './log/result{}.csv'.format(datetime.datetime.now()))
            order = self.get_order(self.trend)
            logger.warning("重新获取参数 {}".format(order))
            self.__trend_model(order)

        return order

    def predict(self):
        # 预测
        self.__predict_trend()
        # 为预测出的趋势数据添加周期数据和残差数据
        self.__add_season()
        return (self.final_pred, self.low_conf, self.high_conf)
