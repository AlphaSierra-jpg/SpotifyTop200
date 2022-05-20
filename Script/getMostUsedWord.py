from unittest import result
from multi_rake import Rake
import pymongo
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

pool = ThreadPoolExecutor(max_workers=200)

def get_database():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["SpotifyTop200"]
    lyricsCol = mydb["lyrics"]

    return lyricsCol

def analyzeTexteAndUpdate(trackName, artist, date, i, ntracks):
    lyricsCol = get_database()
    query = {"Track Name": trackName, "Artist" : artist, "Date": date}
    text = lyricsCol.find(query)
    rake = Rake()

    for x in text:
        keywords = rake.apply(x['Lyrics'])

    
    newvalues = { "$set": { "keywords": normalizeKeyWords(keywords[:20]) } }

    lyricsCol.update_one(query, newvalues)
    print(f"Track {trackName} by {artist} updated -- {i}/{ntracks}")

def normalizeKeyWords(keywords):
    result = []
    for word  in keywords:
        result.append(word[0])
    
    return result

def addKeywords():
    lyricsCol = get_database()
    allMusic = lyricsCol.find({})
    ntracks = lyricsCol.count_documents({})
    i = 0
    
    futures = [pool.submit(analyzeTexteAndUpdate, music["Track Name"], music["Artist"], music["Date"], i, ntracks) for music in allMusic]
    wait(futures, return_when=ALL_COMPLETED)  
    print("finished processing")
    

    print(pool.map)



