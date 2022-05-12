import lyricsgenius
import pymongo
from colorama import Fore
import time
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(max_workers=20)
tic = time.perf_counter()
token = "OXOfo-hXZSbr5k5_qp7UgUpqgM6C40jdH0q2QNZNBZ_FTPgQ9W5KCJSH6TSbe-MJqlTer-HA8FLwx_wHKD5QUw"
howMany =  0
maxMusic = 1000


def get_database():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["SpotifyTop200"]
    lyricsCol = mydb["lyrics"]

    return lyricsCol

def oneLyricsToMongo(lyrics, songName, artistName, Date, i):
    lyricsCol = get_database()
    global howMany

    row ={ 
        "Track Name": songName,
        "Artist": artistName,
        "Date": Date,
        "Lyrics": lyrics
    }
        
    lyricsCol.insert_one(row)
    howMany += 1
    print(f"Lyrics: {songName} {artistName} in mongo -- {time.perf_counter() - tic:0.1f} seconds -- {howMany}/{i}")

def getDBInfo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["SpotifyTop200"]
    csvCol = mydb["csv"]
    count = csvCol.count_documents({})
    i = 0
 
    for x in csvCol.find({}, {"Track Name": 1, "Artist": 1, "Date": 1}):
        i = i + 1
        try: 
            print(f"{i}/{maxMusic}")
            maximize =  maxMusic
            if i >= maxMusic:
                return
        except:
            print(f"{i}/{count}")
            maximize =  count
        
        #threading.Thread(target = getLyrics, args = (token, x["Track Name"], x["Artist"], x["Date"])).start()
        pool.submit(getLyrics, token, x["Track Name"], x["Artist"], x["Date"], maximize)
        #getLyrics(token, x["Track Name"], x["Artist"], x["Date"])
        
        

def getLyrics(token, songName, artistName, date, i):
    genius = lyricsgenius.Genius(token)
    global howMany
    try:
        song = genius.search_song(songName, artistName)
        oneLyricsToMongo(song.lyrics, songName, artistName, date, i)
        return song.lyrics
    except:
        howMany += 1
        oneLyricsToMongo("", songName, artistName, date, i)
        print(Fore.RED + "Error: something is wrong with the song " + Fore.WHITE + songName + Fore.RED + " by artist " + Fore.WHITE + artistName + Fore.RED + f" {howMany}/{i}" + Fore.WHITE)
        print(f"{time.perf_counter() - tic:0.1f} seconds")
        return "Empty"
    

    

if __name__ == "__main__":
    getDBInfo()
    

