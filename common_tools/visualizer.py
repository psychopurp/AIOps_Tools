import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd


class Visualizer:

    plot_list = []

    @staticmethod
    def draw(filename='temp-file.html'):
        py.plot(Visualizer.plot_list, filename=filename)
        print("绘制完成")

    @staticmethod
    def show():
        go.Figure(data=Visualizer.plot_list).show()

    @staticmethod
    def append(*ts):
        '''time_series'''
        for item in ts:
            trace = go.Scatter(
                x=item.index,
                y=item,
                # mode = 'markers+lines',
            )
            Visualizer.plot_list.append(trace)

    @staticmethod
    def bar_graph(x, y, filename='temp-file.html'):
        trace = go.Bar(
            x=x,
            y=y
        )
        py.plot([trace], filename=filename)

    @staticmethod
    def scatter_graph(*args, filename='temp-file.html'):
        plot_list = []
        for ts in args:
            trace = go.Scatter(
                x=ts.index,
                y=ts,
                # mode = 'markers+lines',
            )
            plot_list.append(trace)
        py.plot(plot_list, filename=filename)


if __name__ == "__main__":
    ts = pd.Series([1, 4, 8, 12], index=[1, 2, 3, 4])
    Visualizer.append(ts, ts)
    # Visualizer.show()
