import pandas as pd

def diff_smooth(ts,interval):
    '''时间序列平滑处理'''
    # interval最小单位为秒，除以60就变为分钟，方便下面处理.
    # wide = interval/60
    # 一阶差分
    dif = ts.diff().dropna()
    print(dif)


def datetime_indexed(time_list,value_list):
    '''将数据变为Series类型'''
    dta=pd.Series(value_list)
    dta.index=pd.DatetimeIndex(time_list)
    return dta