import plotly.offline as py
import plotly.graph_objs as go


class Visualizer:

    @staticmethod
    def bar_graph(x,y,filename='temp-file.html'):
        trace=go.Bar(
                x=x,
                y=y
            )
        py.plot([trace],filename=filename)

    @staticmethod
    def scatter_graph(x,y,filename='temp-file.html'):
        trace=go.Scatter(
                x=x,
                y=y,
                # mode = 'markers+lines',
            )
        py.plot([trace],filename=filename)


# if __name__=="__main__":
#     pass
    # Visualizer.bargraph()