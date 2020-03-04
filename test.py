
import os
import common_tools as ct
import plotly.offline as py
import plotly.graph_objs as go
from timeseries_predict.models import ARIMAModel


def test(a):
    b = a
    b[0] = 'test'
    print(a, id(a))
    print(b, id(b))
    return a


if __name__ == "__main__":
    # %%
    print(dir(ARIMAModel))
    x, y = ct.DataHandler('../机器学习/data/1/1_7days.txt').get_data()
    dta = ct.data_to_series(x, y)
    dta = dta.resample('T').mean()
    ts = ct.diff_smooth(dta)
    arima = ARIMAModel(ts, test_size=1440, predict_size=60*5)
    # arima.train()
    print(type(arima.train))
