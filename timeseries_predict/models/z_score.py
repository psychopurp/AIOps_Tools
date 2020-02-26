import datetime
import pandas as pd


class ZScoreModel:
    '''
    z-score空间转换模型
    目前适用于以天为单位的数据异常检测
    '''

    def __init__(self, ts, window_size=10, days=7):
        '''
        :param 
        :ts为训练数据集pandas series
        :window_size 为抽样窗口大小 min
        '''
        self.ts = ts
        self.days = days
        self.window_size = window_size
        self.param = {}  # 训练后会获取参数

    def train(self, time):
        '''
        :time为训练的某个时间点 str or datetime
        :days为抽样天数
        :return 模型参数(u,sigma) 抽样区域的均值和方差
        '''
        frame = {}
        train = pd.Series(dtype='float64')
        for day in range(0, self.days):
            tmp = time+datetime.timedelta(days=day-self.days)
            start = tmp+datetime.timedelta(minutes=-self.window_size)
            end = tmp + datetime.timedelta(minutes=self.window_size)
            # print(start, end)
            train = train.append(self.ts[start:end])

        # dtf = pd.DataFrame(frame)
        # print(train)
        param = {'time': time, 'mean': train.mean(), 'std': train.std()}
        self.param = param
        print('计算参数 {}'.format(self.param))
        return train

    def get_z_score(self, ts, n=5):
        '''
        :parma
        :ts 为检测数据集
        :n 为滞后系数，相当于每n分钟重新计算一次模型参数
        '''
        # 数据深拷贝
        result = ts.copy(deep=True)
        for time in result.index:
            # 时间差
            if not self.param.get('time'):
                self.train(time)
            tmp = (time - self.param.get('time')).total_seconds()/60
            if tmp > n:
                # 重新计算模型参数
                self.train(time)

            # 标准化 获取z-score
            result[time] = (result[time]-self.param.get('mean')) / \
                self.param.get('std')
        return result
