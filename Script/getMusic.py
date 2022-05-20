import requests
from datetime import date, timedelta
import datetime
import csv
import pymongo
import time
import threading
from colorama import Fore

tic = time.perf_counter()
stopDate = "2016-12-23"
#stopDate = "2021-01-01"


def get_database():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["SpotifyTop200"]
    csvCol = mydb["csv"]

    return csvCol


def getAllDay():
    date_today = datetime.date.today()
    theDay = date_today.strftime('%A')
    i = 0
    dates = []

    ref = ["Thursday", 6, "Wednesday", 5, "Tuesday",
           4, "Monday", 3, "Sunday", 2, "Saturday", 1]

    if theDay == "Friday":
        tempo = date_today
        dates.append(tempo)
    else:
        while i < 10:
            if theDay == ref[i]:
                dates.append(str(date_today - timedelta(ref[i+1])))
                tempo = dates[0]
            i = i + 2

    while str(tempo) != stopDate:
        tempo = str(tempo).split("-")
        firstDay = datetime.date(int(tempo[0]), int(tempo[1]), int(tempo[2]))
        dt = firstDay - timedelta(7)
        tempo = dt
        dates.append(str(dt))
    return dates
def writeFile(fileName, content):
    if content == 0:
        print(Fore.RED + "For " + Fore.WHITE + fileName + Fore.RED + ", Content is empty:" + Fore.WHITE ,content)
        return 0

    file = open("Script/allCSV/" + fileName + ".csv", "w")
    file.write(content)
    file.close

    oneCSVtoMongo(fileName)

def fetchData(url, cookie, i, dates):
    headers = {
        'Cookie': cookie,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'spotifycharts.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
        'Accept-Language': 'fr-FR,fr;q=0.9',
        'Referer': url,
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers)
    
    if response.status_code == 200:
        tempo = response.text
        tempo = tempo.replace(
            ",,,\"Note that these figures are generated using a formula that protects against any artificial inflation of chart positions.\",\n", "")
        print(f"For {url}, OK")
        writeFile(f"{dates[i+1]}--{dates[i]}", tempo)
        if dates[i+1] == stopDate:
            print(f"{time.perf_counter() - tic:0.1f} seconds")
        return tempo
    else:
        print( Fore.RED + "error with " + Fore.WHITE + url + Fore.RED + ": something is wrong:" + Fore.WHITE, response.status_code)
        if dates[i+1] == stopDate:
            print(f"{time.perf_counter() - tic:0.1f} seconds")
        return 0

def getAllCSV(dates, cookie):
    InterruptedError = False
    i = 0

    while InterruptedError == False:
        url = f"https://spotifycharts.com/regional/global/weekly/{dates[i+1]}--{dates[i]}/download"
        
        threading.Thread(target = fetchData, args = (url, cookie, i, dates)).start()
        #fetchData(url, cookie, i, dates)
        i = i + 1
        try:
            dates[i+1]
        except:
            print(f"All CSV get since {dates[0]} to {dates[len(dates)-1]}")
            InterruptedError = True

def oneCSVtoMongo(fileName):
    csvCol = get_database()
    header = ["Position", "Track Name", "Artist", "Streams", "URL", "Date"]
    
    fileName = "Script/allCSV/" + fileName + ".csv"
    try: 
        csvfile = open(fileName, 'r')
    except:
        print(Fore.RED + "Can't open file" + Fore.WHITE, fileName)
        return

    
    reader = csv.DictReader(csvfile)
    
    try: 
        for each in reader:
            row = {}

            for field in header:

                if field == "Date":

                    row[field] = fileName.replace("Script/allCSV/", "").replace(".csv", "")
                else:
                    row[field] = each[field]

            csvCol.insert_one(row)
        print(f"CSV: {fileName} in mongo")
    except:
        print(Fore.RED + "CVS file can't be parsed" + Fore.WHITE , fileName)
        return



