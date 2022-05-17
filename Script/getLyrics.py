import lyricsgenius
import pymongo
from colorama import Fore
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import re


pool = ThreadPoolExecutor(max_workers=100)
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

    row ={ 
        "Track Name": songName,
        "Artist": artistName,
        "Date": Date,
        "Lyrics": lyrics,
        "keywords": []
    }
        
    lyricsCol.insert_one(row)

def getDBInfo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["SpotifyTop200"]
    csvCol = mydb["csv"]
    count = csvCol.count_documents({})
    i = 0


        
    # for x in csvCol.find({}, {"Track Name": 1, "Artist": 1, "Date": 1}):
    #     i = i + 1
        
    #     try: 
    #         if i > maxMusic:
    #             return
    #         print(f"{i}/{maxMusic}")
    #         maximize =  maxMusic
            
    #     except:
    #         print(f"{i}/{count}")
    #         maximize =  count

    futures = [pool.submit(getLyrics, token, x["Track Name"], x["Artist"], x["Date"], count) for x in csvCol.find({}, {"Track Name": 1, "Artist": 1, "Date": 1})]
    wait(futures, return_when=ALL_COMPLETED)  
    print("finished processing")
        

def getLyrics(token, songName, artistName, date, i):
    genius = lyricsgenius.Genius(token)
    global howMany
    reg = r'\s\(feat[\s\S]*\)'
    output = re.sub(reg, '', songName)

    try:
        song = genius.search_song(output, artistName)
        howMany += 1
        oneLyricsToMongo(song.lyrics, songName, artistName, date, i)
        print(f"Lyrics: {songName} {artistName} {date} in mongo -- {time.perf_counter() - tic:0.1f} seconds -- {howMany}/{i}")

    except:
        oneLyricsToMongo("", songName, artistName, date, i)
        howMany += 1
        print(Fore.RED + "Error: something is wrong with the song " + Fore.WHITE + songName + Fore.RED + " by artist " + Fore.WHITE + artistName + Fore.RED + f" {howMany}/{i}" + Fore.WHITE)
        print(f"{time.perf_counter() - tic:0.1f} seconds")
    

    

if __name__ == "__main__":
    getDBInfo()


