import pandas as pd
import datetime
import numpy as np
import data_handler
from visualizer import Visualizer

def diff_smooth(ts,interval):
    '''时间序列平滑处理'''
    # 目前为止观察到 interval=5时 效果较好
    # interval最小单位为秒，除以60就变为分钟，方便下面处理.
    wide = interval/60
    wide=interval
    # 一阶差分
    dif = ts.diff().dropna()
    # 描述性统计得到：min，25%，50%，75%，max值
    td = dif.describe()
    # 定义高点阈值，1.5倍四分位距之外
    high = td['75%'] + 1.5 * (td['75%'] - td['25%'])
    # 定义低点阈值
    low = td['25%'] - 1.5 * (td['75%'] - td['25%'])
    # 变化幅度超过阈值的点的索引
    forbid_index = dif[(dif > high) | (dif < low)].index
    i=0
    while i < len(forbid_index) - 1:
        n = 1
        # 异常点的起始
        start = forbid_index[i]
        while forbid_index[i+n] == start + datetime.timedelta(minutes=n):
            n += 1
        i += n - 1
        # 异常点的结束
        end = forbid_index[i]
        # np.linspace(start, end, num)生成等差数列
        # 用前后值均匀填充
        test=ts[start]
        a=ts.get(start - datetime.timedelta(minutes=wide),ts[start])
        b=ts.get(end + datetime.timedelta(minutes=wide),ts[end])
        value = np.linspace(a,b, n)
        ts[start: end] = value
        i += 1
    return ts


def datetime_indexed(time_list,value_list):
    '''将数据变为Series类型'''
    dta=pd.Series(value_list)
    dta.index=pd.DatetimeIndex(time_list)
    dta.index.name='time'
    return dta




if __name__=="__main__":
    dataHandler=data_handler.DataHandler('./data/1/1_30days.txt')
    x,y=dataHandler.get_data()
    dt=datetime_indexed(x,y)
    Visualizer.append(dt)
    ts=diff_smooth(dt,5)
    Visualizer.append(ts)
    Visualizer.draw()
    
    # Visualizer.scatter_graph(dt,ts)
    