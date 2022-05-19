import Script.getMusic as getMusic
import Script.getTrend as getTrend

date = getMusic.getAllDay()
dataPoint = []

for i in range(0, len(date)):
    dataPoint.append(i)

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Word in top 200 analyzer '),
    dcc.Graph(id="time-series-chart"),
    html.P("Tap the word"),
    # dcc.Dropdown(
    #     id="ticker",
    #     options=["AMZN", "FB", "NFLX"],
    #     value="AMZN",
    #     clearable=False,
    # ),
    dcc.Textarea(
        id='ticker',
        value='love',
        style={'width': 200, 'height': 20},
        
    ),
])


@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))
def display_time_series(word):

    fig = px.line( x=date , y=getTrend.searchInKeyWord(word))
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Occurence')
    return fig


app.run_server(debug=True)

 