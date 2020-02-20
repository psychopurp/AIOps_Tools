


class DataHandler:
    
    def __init__(self,filename='', *args, **kwargs):
        self.filename=filename

    
    def read_file(self,**kwargs):
        '''
        return: 
        file_lines_list
        '''
        filename=self.filename
        if 'filename' in kwargs:
            filename=kwargs.get('filename')
        with open(filename) as f:
            return f.readlines()

    def separate(self,line:str):
        '''
        处理数据中间件
        '''
        result=line.split('\t')
        time=result[0]
        value=result[1].split('\n')[0]
        return time,value
    

    def get_data(self,lines=None):
        '''
        :param lines读取的行数
        :return 
        timelist:时间列表
        valuelist:数据列表
        '''
        time_list=[]
        value_list=[]
        raw_data=self.read_file()
        if not lines:
            lines=len(raw_data)
        for k,item in enumerate(raw_data):
            if k>=lines:
                break
            result=item.split('\t')
            time=result[0]
            value=int(result[1].split('\n')[0])
            time_list.append(time)
            value_list.append(value)
        return time_list,value_list




# if __name__=="__main__":
#     dataHandler=DataHandler('./data/1/1_7days.txt')
#     x,y=dataHandler.get_data()
#     dt=datetime_indexed(x,y)
#     # Visualizer.scatter_graph(dt.index,dt)
#     # print(dt)
#     # print(dt[0])
#     # print(dt[1:2])
#     dt=pd.Series([0,4,8,12])
#     print(dt.get(0))
    # dif=dt.diff().dropna()
    # print(dt[dt>5])
   
    # diff_smooth(dt,60)