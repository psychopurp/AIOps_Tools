import plotly.offline as py
import plotly.graph_objs as go


class Visualizer:

    plot_list=[]

    @staticmethod
    def draw(filename='temp-file.html'):
        py.plot(Visualizer.plot_list,filename=filename)
        print("绘制完成")

    @staticmethod
    def append(ts):
        trace=go.Scatter(
                    x=ts.index,
                    y=ts,
                    # mode = 'markers+lines',
                )
        Visualizer.plot_list.append(trace)

    @staticmethod
    def bar_graph(x,y,filename='temp-file.html'):
        trace=go.Bar(
                x=x,
                y=y
            )
        py.plot([trace],filename=filename)

    @staticmethod
    def scatter_graph(*args,filename='temp-file.html'):
        plot_list=[]
        for ts in args:
            trace=go.Scatter(
                    x=ts.index,
                    y=ts,
                    # mode = 'markers+lines',
                )
            plot_list.append(trace)
        py.plot(plot_list,filename=filename)


if __name__=="__main__":
    print(Visualizer.plot_list)
    Visualizer.plot_list.append(5)
    Visualizer.draw()
    # print(Visualizer.plot_list)