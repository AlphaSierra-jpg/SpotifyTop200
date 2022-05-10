import requests
from datetime import date, timedelta
import datetime
import csv
import pymongo
import os
import time

tic = time.perf_counter()
cookie = 'cf_chl_2=; cf_chl_prog=; cf_clearance=AWRlxfh1KnSojc35r5mAi49AX4KTPF4YXj1r595DUCI-1652182137-0-150; 850bcede40217f5e29cd09097cc083f9f306638a=eyJpdiI6IklqQ1FGSzdvNk43ek1oWEdPVnRmUlE9PSIsInZhbHVlIjoiVW1GWmpTQWxoZlB6b1hxdmpZODN4czRDR3hKYTdMK3JmSlZcL1hVSmNKbHYwN3lLYjZmbWJHc1VqaTJhQUpqRWdCeU9rN0JSUUttYXk3WFl2Q05TQ24yWVhxcmd6KzZcL0VUUUd2VXlZbTlSOUJUUGprV3BzYm9vRVpqZjBLVVBFTmRSblwvQVhcLzF6VFZuN1wvZHZzYVdRSjhHY3o4TitONG9CRmw3ZjhnQVlNWWFNNHFTb0lXWHhDRExVWEdrazZBRDFrbVp1MVBKWVhcL0tWUHhVWjk2S0VxcUM0R1dqWVh2YVJ1OEZaUVRoc282RDhISUtOZnRSWlBnVTJkbmpvcml1VmZIbXJRcnlWOVdDN0trV0FHWEVzTkZxelFzRWx0K29vME5VMTlzUXdvSDdlOE5abVloQ2FuWmFESE50SEF3RTRha2d0RUloemhQSTIzckRRa0REdnZXM1wvTDJDWTB4MWZBRUNncXprVzJyamhHc2ppKzd5TE5BNWFrdVwvTkhvTEhRVStaYlRiNXN1Zlk2ZUpXejNJK3pIT0ZyOWhwWUVUM3FBem5TQ3lGMzZlVkNsVytSU00zNlVjZ25TUUhBRGQyZXB6dXF6WFZEc00ycituYkowWmJsb1dhYkVCb2N0SDg0MVA1ZHhYQkI2RXVhQnlnR1NGTnRCMmtIK2RzMEQ2ZyIsIm1hYyI6IjNhNzgzZmRjYjVlMDg2MTEzYWQ5ZmYzNjFkNTRhYzI1N2ZkZTdmOGJlNDkwMDEyNGQ3ZjExNDk1ODljNGQzODQifQ%3D%3D; X-Mapping-kjhgfmmm=9343FCBF8CF03218178FBD7548D564F1; XSRF-TOKEN=eyJpdiI6Im1Ca0VHMFVQblh5RjVrK0xFQTJ2amc9PSIsInZhbHVlIjoiWXJBaEFRc3lCcE11MURNMzdwWXR6WlMrV3hlVGw3bzRnOWJ6UUJkUnpkNlN1YU1BN2Q1cWxnOUhOZXArRitid0RTMEFocjY0SE9UMGczbTBFS2syRkE9PSIsIm1hYyI6ImZjZTZiMTU0YTQzZjVhMDBhN2NhNDZiYjcxMTU2Y2MwZjU3YTk3NjVkOGVmY2JjNWE4MGE3NjdhYjViYTNkMWQifQ%3D%3D; laravel_session=eyJpdiI6IlNuVnpkblJZb29DVGM1UjYwdEJJb0E9PSIsInZhbHVlIjoiYmJHZ3lsMnFhVjNBZjdFTE5ZVlFnZElieW9yRXhZSGhDZ2tNOWRUYXlJdU1rXC9sTjQxZTJmRjM0cDFFeTQ2SzE0NW5QTFBGUDk0TUZMWUthV3NQdVNnPT0iLCJtYWMiOiJkNzYyNjQ5ZDZkMWNiMDc2NWM3YWY0OWMzNDhhZDE5YTY0ZmRlOWZiYzM0OGFkZTIyNDlhNzYzOGU3MDkyZjMxIn0%3D; cf_chl_prog=x11; cf_chl_2=c62a84d06e9ab5a; cf_chl_rc_m='
stopDate = "2016-12-23"
#stopDate = "2022-01-07"


def get_database():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["SpotifyTop200"]
    csvCol = mydb["csv"]
    lyricsCol = mydb["lyrics"]

    return csvCol, lyricsCol


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


def fetchData(url, cookie):
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
        return tempo
    else:
        print(f"error with {url}: something is wrong:", response.status_code)
        return 0


def writeFile(fileName, content):
    if content == 0:
        print(f"For {fileName}, Content is empty:",content)
        return 0

    file = open("allCSV/" + fileName + ".csv", "w")
    file.write(content)
    file.close


def getAllCSV(dates):
    InterruptedError = False
    i = 0

    while InterruptedError == False:
        url = f"https://spotifycharts.com/regional/global/weekly/{dates[i+1]}--{dates[i]}/download"
        writeFile(f"{dates[i+1]}--{dates[i]}", fetchData(url, cookie))
        i = i + 1
        

        try:
            dates[i+1]
        except:
            print(f"All CSV get since {dates[0]} to {dates[len(dates)-1]}")
            InterruptedError = True

        print(f"└─[ {i}/{len(dates)-1} ] -- {time.perf_counter() - tic:0.1f} seconds")
  


def oneCSVtoMongo(fileName):
    csvCol, lyricsCol = get_database()
    header = ["Position", "Track Name", "Artist", "Streams", "URL", "Date"]
    csvfile = open(fileName, 'r')
    reader = csv.DictReader(csvfile)

    for each in reader:
        row = {}

        for field in header:

            if field == "Date":

                row[field] = fileName.replace(
                    "./allCSV/", "").replace(".csv", "")
            else:
                row[field] = each[field]

        csvCol.insert_one(row)
    print(f"CSV: {fileName} in mongo")


def allCSVtoMongo():
    allFileName = os.listdir("./allCSV")
    if allFileName == []:
        print("Error, directory is empty or does not exist")
        return
    i = 0
    for fileName in allFileName:
        i = i + 1
        oneCSVtoMongo(f"./allCSV/{fileName}")
        print(f"└─[ {i}/{len(allFileName)} ] -- {time.perf_counter() - tic:0.1f} seconds")
    print("All CSV are in mongo")



