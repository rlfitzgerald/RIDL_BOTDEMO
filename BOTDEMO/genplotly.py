import plotly.graph_objs as go
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import  numpy as np

def gen_plot():
	colorscale = [[0, '#FAEE1C'], [0.33, '#F3558E'], [0.66, '#9C1DE7'], [1, '#581B98']]
	trace1 = go.Scatter(
    		y = np.random.randn(100),
    		mode='markers',
    		marker=dict(
        	size='20',
        	color = np.random.randn(5),
        	colorscale=colorscale,
        	showscale=True
    	)
	)
	data = [trace1]
	url_1 = plot(data, filename='s.html', auto_open=False,output_type='div', include_plotlyjs=False)
	return url_1


def gen_barchart():
	data = [go.Bar(
            x=['DK', 'US','LR','PA','GR','HK','VU','MT'],
            y=[5,25,2,5,3,5,2,3]
    )]
	url=plot(data,output_type="div",filename="bar.html",include_plotlyjs=False)
	return url
#gen_barchart()
#gen_plot()
