import requests
from datetime import date, timedelta
import datetime
import csv
import pymongo
import time
import threading
from colorama import Fore

tic = time.perf_counter()
cookie = 'cf_chl_2=; cf_chl_prog=; cf_clearance=ZzCgM7vF5._t_cXizBcqJsUrXzv9aFTB3by9BGnrIuE-1652263317-0-150; 850bcede40217f5e29cd09097cc083f9f306638a=eyJpdiI6IjBZV0ZvMmNEVWxGUml5MHVzdDhjamc9PSIsInZhbHVlIjoic0FET0g1NmZUN1gzTEpTYkJodkRVaE9uY1c2YzU4b2cwNnk0YlY5eWhDK0IyS1RLcVwva0VINXJ6RWowTnI2YlpaT1VCMXQzTTZYajl3VmoxWlwvMkFjVlE2UWIxM0R6OEtWSU9oM3NPcmJOMHVoN0hTY3FsRWg4NlRzZE9GNHV3dlhwRkE2MWNxSDEwV205VVpsYjVOXC9NZ3owVTF6aVpaQ0JUdHZzeUJyYjJDdE11NTVWXC80d2g2WFhITVU2OE5maG1MR0wrd0NNS0ticTlTTkJYZVA5dWF5QzE0YnJtVnJQTXdjQW5QcmQ4Y05pRXFtUGllenJhb2pIUnZid0dsZG1jNlMxMkhNM3ZzdVVjUXlCQU1OV0pFRUJ3cm9cL3NcL0FRSGEyM0VIeXgzeG1zdUtxczg2OGJtaEdTZFFzK2t4Nm4wMjVnd1BuSUxCWU9FXC9tWDViWVNLWGNkWmRreFdxYzlITUVGSTFLSWRHXC9xY2w4ZENLdDVBdDRyZGxZYUo0cWhrc0xCVElPNmhhOCtLWHROZVBmMm0rejdQSm41aFJ0dTRRMm8xTDJxMmFXMWs1cVE1akJ5Z09rZVdTUldraFdhRmNxdzIybmtMY0I5TjdPZlJKdWtoaU9QdmlMNkhTclFKTDE3VGc2RHh2MVdoRWN5SUcwM1c2eE1xVTNZcnRSTyIsIm1hYyI6IjQ3ODAyMGJlYjEwNTJmOTZkMDY2MzdjNTUwNGIyMWQwNWViNzhjMmQyZjUzMTQyYzQ5ZjUwNWU2MDM5NjkzNjgifQ%3D%3D; X-Mapping-kjhgfmmm=9343FCBF8CF03218178FBD7548D564F1; XSRF-TOKEN=eyJpdiI6ImdVUVh1WU1Fc0dBTnExXC9odDVSbTh3PT0iLCJ2YWx1ZSI6InV4REZaSVJvT040TEo1U3BjMW1ZMGpoQzcrQWQ5QkcxSlJLSXR3dWJlWkV0R2duOVZ0V3FCUXBYSkVKRkl5SlpaY2VHalphN0pPbHNHQitVSmJ2WkpnPT0iLCJtYWMiOiJjODQ2MmNkYzU2ZDVjNGI5NmExMTVlZGM5NzE4N2E1MzUwMTM3ZmRiZjhhZGMwMTkxNWExOGQ2MjAzM2E1NTc4In0%3D; laravel_session=eyJpdiI6Im9SUkNVS09XWnhKN1dpMUdSdFkxdWc9PSIsInZhbHVlIjoiR3ZTTzRTUFlPN3pCKzFtZFVaNzRQZXFMd1hydEJEQVF2cW1oN08zK0pXQVR2OEtJUmFFa3NYK0dyXC9aVlltTGhQMytMblZWcklDMU9jeDRQNUp2cjdRPT0iLCJtYWMiOiI0NjdiZTQ2OGEwZjY1YTI1MjEyZTQ5MDM4ODAyMmUwNTBhNDcyZTI5N2M5MGViZjRmMWUxYTgyODRmNmQ0ZTg3In0%3D; cf_chl_prog=x13; cf_chl_2=20e65488113fefb; cf_chl_rc_m='
stopDate = "2016-12-23"
#stopDate = "2022-01-07"


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

def getAllCSV(dates):
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

        print(f"└─[ {i}/{len(dates)-1} ] -- {time.perf_counter() - tic:0.1f} seconds")
  


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



