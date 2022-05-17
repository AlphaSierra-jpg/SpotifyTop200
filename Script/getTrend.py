import pymongo

def searchInKeyWord(search):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["SpotifyTop200"]
    lyrCol = mydb["lyrics"]

 
    for x in lyrCol.find({}, {"keywords": 1, "Track Name": 1, "Artist" : 1, "Date": 1, "Lyrics": 1}):
        
        for i in range(len(x["keywords"])):
           
            if search in x["keywords"][i].split():
                print(x["Artist"], x["Track Name"])
                print(x["keywords"])