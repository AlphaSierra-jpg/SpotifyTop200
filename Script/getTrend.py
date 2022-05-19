import pymongo
import Script.getMusic as getMusic
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

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
    html.H4('Word in top 200 analyzer '),
    dcc.Graph(id="time-series-chart"),
    html.P("Tap the word"),
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

    fig = px.line( x=date , y=searchInKeyWord(word))
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Occurence')
    return fig

def showGraph():
    app.run_server(debug=True)