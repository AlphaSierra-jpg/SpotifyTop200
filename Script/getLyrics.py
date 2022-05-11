import lyricsgenius
import pymongo
from colorama import Fore
import time

tic = time.perf_counter()

token = "0XOfo-hXZSbr5k5_qp7UgUpqgM6C40jdH0q2QNZNBZ_FTPgQ9W5KCJSH6TSbe-MJqlTer-HA8FLwx_wHKD5QUw"

def get_database():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["SpotifyTop200"]
    lyricsCol = mydb["lyrics"]

    return lyricsCol

def oneLyricsToMongo(lyrics, songName, artistName, Date):
    lyricsCol = get_database()

    row ={ 
        "Track Name": songName,
        "Artist": artistName,
        "Date": Date,
        "Lyrics": lyrics
    }
        
    lyricsCol.insert_one(row)
    print(f"Lyrics: {songName} {artistName} in mongo -- {time.perf_counter() - tic:0.1f} seconds")

def getDBInfo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["SpotifyTop200"]
    csvCol = mydb["csv"]
    count = csvCol.count_documents({})
    i = 0
 
    for x in csvCol.find({}, {"Track Name": 1, "Artist": 1, "Date": 1}):
        oneLyricsToMongo(getLyrics(token, x["Track Name"], x["Artist"]),  x["Track Name"], x["Artist"], x["Date"])
        i = i + 1
        print(f"{i}/{count}")

def getLyrics(token, songName, artistName):
    genius = lyricsgenius.Genius(token)
    try:
        song = genius.search_song(songName, artistName)
        return song.lyrics
    except:
        print(Fore.RED + "Error: something is wrong with the song " + Fore.WHITE + songName + Fore.RED + " by artist " + Fore.WHITE + artistName)
        print(f"{time.perf_counter() - tic:0.1f} seconds")
        return "Empty"
    

    

if __name__ == "__main__":
    getDBInfo()
