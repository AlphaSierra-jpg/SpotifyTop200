import requests
from datetime import date, timedelta
import datetime
import csv
import pymongo
import time
import threading
from colorama import Fore

tic = time.perf_counter()
cookie = '91c5df3306cde820d8ebbbac2b0b26bfe1cc7fce=eyJpdiI6Imc2OTRsWFZ6RnI4ZXNDM1FRWm55YUE9PSIsInZhbHVlIjoiK0J0azZcL2dWOTZcL0tsSCtFaXZJbzlNK3BHYUhLSitLSUo3VVZHNUlzY3ZXNjlEWityWnIrUk84RzV4RzlTWnkwSTRzVTFzajNYK2pGRFBXUGJcL2x2OFozSXV5SVVPR1QyTFwvZUpFN3BPUjF1UnNNVTh1YmhTNnF4TUZMTTA2R2psUlg5SW5aeEEyYXF0XC9abkhwanAzVUR5UjRIbkttUmJud3p1MTgrTWFjYWxvVzd5R1hMd3VNVUJHTDlpUVwvcUg1cWNVXC9ONm9OcUNJNGQ5eURYOElcL0t0WG91Tnd6XC8yRVBmTHJ2UTlIM2Y3VWV6OGF5QWgzVVwvMWFtT1NBSjBpeDVCcUx2d0Y0YlpyYUgybHhuRmJybkc2T3ArVFNibHE1aUk4Tjk2WDVqVHRQSWlNdmlibkZkNytRK0NqVGszRUJrVUJuYWliVGhqK2pwMlNlTkRHQW5wN3orK21CakV0TFA4cXJJUmVoN1RaZWZxdXB4UWpkQURkOVBmaFZGMGNseERDQmpaU2hrTGpBQjZ1S0tcL0g5WllQZlhnTytsSU9rK2o1SERacjV5dE5TMVdTODlURStQUEFWRm90WWRSdG82WkgxdWVQM213cXF4YnJmRmE1VzJaWWNBQThLTXpGVUJBRGxsSGNZOEVZQktkNlVPWElIQ25CYUFQYkdyaTNyUSIsIm1hYyI6ImY3Y2M4MDVhMDQ2NzBkZmJmNGVkMzAzNTJiODVlZmViYjBiOTRiMjdiMjZiMmEyMDcyZTdjMTdkMzRlYjgwZmUifQ%3D%3D; X-Mapping-kjhgfmmm=35F848C5D7F69E3AC4DE9A21CE4F27CE; XSRF-TOKEN=eyJpdiI6InhVcFhhSkJ5cUc4amJIdjFBaHh1Y3c9PSIsInZhbHVlIjoiT05XREhoS2UwYkpraXEwc3VQWFo0alA5S3U2RUxXN2w5Mm95V0tidnJuSWJWa3pIbzZEam1tVXJ5cVNVc1V2SUhwaytwRFFaenFWOXVMaW5SSFNnNVE9PSIsIm1hYyI6ImI0MzRlOTJhNjJlNTUwYmY3NTQ3OWZhZDY2YmIwN2FiOGI1MjcxNjAzODM2NjhhM2EyNjA2NDhjNjc0ZTk3OTEifQ%3D%3D; laravel_session=eyJpdiI6IlM2ZEU2SkRhWk1xMnNiVnF2UGVjNUE9PSIsInZhbHVlIjoiaUx2OEtlbERjYUczcmJRYW41anR6YTNqWUJUbmRqaG94OTRMUEJneHVqWkRUWWFYZWRFM3RyTXRwaElGUjhDV1VWXC9oRlZQTEFzYUhKZFc3V1lkSGZnPT0iLCJtYWMiOiIwMjg1MWM5OTdhODEyMzEyMDI5NTY3ZTliNGZjNGE2ZDVmNTA2Nzg0MmIxZWU1MGFlM2RkYTg2Y2Y5MWIzYmVlIn0%3D; cf_chl_2=; cf_chl_prog=; cf_clearance=D.5C0AeDKCcwKQzugWwg6nUdD33i3lnYeCckTT.yys8-1652348248-0-150; cf_chl_prog=x10; cf_chl_2=3d554955b2f02cf'
#stopDate = "2016-12-23"
stopDate = "2021-01-01"


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



