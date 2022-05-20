import pymongo
import Script.getMusic as getMusic
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.graph_objects as go

def searchInKeyWord(search):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["SpotifyTop200"]
    lyrCol = mydb["lyrics"]
    print("Searching")
    isFind = False
    output = []
    dates = getMusic.getAllDay()
    for date in dates:
        tempo = [date, 0]
        output.append(tempo)
    

 
    for x in lyrCol.find({}, {"keywords": 1, "Track Name": 1, "Artist" : 1, "Date": 1, "Lyrics": 1}):
        
        for i in range(len(x["keywords"])):
            
            if search in x["keywords"][i].split():
                print(x["Artist"], x["Track Name"], x["Date"])
                for i in range(0, len(output)):
                    if output[i][0] == x["Date"][12:]:
                        output[i][1] += 1

                isFind = True
    



    if isFind == False:
        print("No keywords found")
    
    

    return outputFormater(output)

def outputFormater(output):
    for i in range(0, len(output)):
        output[i] = output[i][1]
    return output


date = getMusic.getAllDay()
dataPoint = []

for i in range(0, len(date)):
    dataPoint.append(i)



app = Dash(__name__)


app.layout = html.Div([
    html.H1('Word in top 200 analyzer', style={'font-family': 'Arial'}),
    dcc.Graph(id="time-series-chart"),
    html.H3("Tap the word", style={'font-family': 'Arial'}),
    dcc.Input(id="input1", type="text", placeholder="Word", style={'width': 200, 'height': 20, 'font-family': 'Arial', 'marginRight':'10px'}),
    dcc.Input(id="input2", type="text", placeholder="Word2", style={'width': 200, 'height': 20, 'font-family': 'Arial'}),
    html.Div([
        html.H3("Some cool word", style={'font-family': 'Arial'}),
        html.P("love", style={'font-family': 'Arial'}),
        html.P("gun", style={'font-family': 'Arial'}),
        html.P("girl", style={'font-family': 'Arial'}),
        html.P("you", style={'font-family': 'Arial'}),
        html.P("me", style={'font-family': 'Arial'}),
        html.P("war", style={'font-family': 'Arial'}),
        html.P("ex", style={'font-family': 'Arial'}),
        html.P("ex", style={'font-family': 'Arial'}),
        html.P("ex", style={'font-family': 'Arial'}),
        html.P("ex", style={'font-family': 'Arial'})
    ]),
    html.Div([
        dash_table.DataTable(
            id='memory-table',
            columns=[{'name': i, 'id': i} for i in range(10)],
        ),
    ])
    
])


@app.callback(
    Output("time-series-chart", "figure"), 
    Input("input1", "value"),
    Input("input2", "value")
    )
def display_time_series(input1, input2):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=date, y=searchInKeyWord(input1), name=input1, line=dict(color='blue', width=2)))
    if input2 != None:
        fig.add_trace(go.Scatter(x=date, y=searchInKeyWord(input2), name=input2, line=dict(color='firebrick', width=2)))

    return fig
def makeArray():
    
    return

def showGraph():
    app.run_server(debug=True)