

import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller


class ARIMAModel:
    '''
    ts: pandas series对象 
    index为DatetimeIndex
    value 为 int
    '''

    def __init__(self, ts, test_size=1440):
        self.test_size = test_size
        self.ts = ts

    def decompose(self, period=1440):
        '''
         将数据进行分解
         :param :period单位为minute
        '''
        decomposition = seasonal_decompose(
            self.ts, period=1440, two_sided=False)
        self.trend = decomposition.trend
        self.seasonal = decomposition.seasonal
        self.redidual = decomposition.resid

    def trend_model(self, order):
        '''
        对趋势部分单独用ARIMA模型做训练
        '''
        self.trend.dropna(inplace=True)
        train = self.trend[: self.trend.size - self.test_size]
        self.trend_model = ARIMA(train, order).fit(method='css-mle')

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

    def train(self, dta, x, y):
        predict_data = []
        if np.max(y) - np.min(y) == 0:
            for i in range(0, self.predict_time):
                predict_data.append(round(np.max(y), 2))
            return predict_data

        """
        for i in range(0, len(mydata_tmp)):
            mydata_tmp[i] = math.log(mydata_tmp[i])
        """
        """
        p为ARMA模型的参数，一般p去小于length/10的数
        但是由于数据的问题，所以分情况设置
        """
        res = sm.tsa.arma_order_select_ic(
            dta, max_ar=7, max_ma=0, ic=['bic'], trend='nc')
        p = res.bic_min_order[0]
        q = res.bic_min_order[1]
        # 建立ARMA模型
        # freq为时间序列的偏移量
        try:
            model_tmp = ARIMA(dta, order=(p, 1, q))
            # method为css-mle
            #model = model_tmp.fit(disp=-1)
            model = model_tmp.fit(disp=-1, method='mle')
            return model
        except:
            model_tmp = ARIMA(dta, order=(1, 1, 1))
            model = model_tmp.fit(disp=-1, method='mle')
            return model

    def predict(self, model, y):
        predict_outcome = model.forecast(self.predict_time)
        return predict_outcome[0]
