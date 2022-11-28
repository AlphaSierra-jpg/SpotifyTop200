from unittest import skip
import Script.getMusic
import Script.getLyrics
import Script.getMostUsedWord
import Script.getTrend
import argparse

cookie = '4fd83ae9eb0bce149533440fe303ad6738c17aab=eyJpdiI6ImV3dWl3aytFYXhlRmQrajV5XC9XTkFRPT0iLCJ2YWx1ZSI6IlFWY0phSmZxZDNOVW02SW9veFdMRERSQTFiWGU4NEEyOWpwS1ZsYTlpbitWbnFcLzg5ZGtzRHQrOXFxNU9aaXRuM1ZaSTRyY1hYV3lvUXBUMm5aZlhtejlOUUNONDZhdmdCU29jbHk5enNYVnkyRm5GOGFEY2s4ekllbEIzM2lPaVdKNG1wc0lYazRxdklRT3lBWjMxaHB0Nk56TU9WV1wvK01Ic0FSMDZuXC9VK2JPY3M3OVNzbG5WQ0g0dFVscXBBUWlQcGc2ajU2MzBxSzVUZFVQYlRVRlFqXC9FaElMdnNpcHpDckh1RitSZ09zMEV4RXBENFlvVmJ5Zk1BZ0dcL0E5eklpSkgzTGZldUVjU0xxZWdKejlYTlVtVFpseU94eVdlVnVIQjJPRVlVTG1PQ3NkYnVOOVBNYzZ4U3crbElVelJPTjlTanpmb1l0Q2hcL2sxQ3AwWXBsZHk2dGpLNjc2VDVYbVBHWVZQODZtdlV1WkNsQzNSWUdMd1F2UDloc1wvWkJIRGsxZENPRVpTcWZYOVEzdlRcL1BKUTQ5aFR6NGd6bitNY0hlRlVxVytySm1UOXhDSUJ1RWo3V2ZLeVlcL2lib3VTa0YzckMyUmY4Mm5yeXNQeFVKc2xWaDRZcmdCS1dkd2pKdkFON1hBa1hJZkE1am13VGJBV2tkWU1pWHpMZnEyIiwibWFjIjoiN2M2ZWVmNjc5MjUyNDFhM2NlMjkyMWY0NGI1MjA0ZDQxMmM5MDhmZmNlMGJkYjAyNmQ5OWQwYjlkN2I5ODcyMSJ9; X-Mapping-kjhgfmmm=9343FCBF8CF03218178FBD7548D564F1; XSRF-TOKEN=eyJpdiI6IlQwV1ZXbkxRNWdSVWlPak1HTW1NR2c9PSIsInZhbHVlIjoia1RyM1ZyQnRDc1czTGtkYlpsS2lYWGZvdCtma1FIZmVcL0hibVdlR09tSmNZbHUyYlVSN1d0eGhEZFh0V3krYzJ0RmJNYnlkdnM1OW83bTZYN0FlQlNnPT0iLCJtYWMiOiIxMDMzYWRkY2Y4ZTExN2FhYzAxZWU4ZDJjYjJhOTI0MGI0ODAzNWFhY2FkMDY1MjM5ZGZlNzBlNjdjNjllNjFlIn0%3D; laravel_session=eyJpdiI6IkRTcXJuSmt5ODhiSTBlc1h2K0pjXC9RPT0iLCJ2YWx1ZSI6IjlEd1hSb09MT3NrNnRXY2VXUlJxMWtMMzB1Y3RzdmdGQnFDZjR2eTV6XC9wbEpRYjFnWVJOVHhPZTJRZXhXNjBHbkdsTW1cL2I3MktTcmhTT1hYaFlGTWc9PSIsIm1hYyI6ImUxZWVhNWE2NmE3ODEzYzU2MTEwNjZjNjVjOWVmZTRhMzFiMjY1NzQ5YWM0M2ZjNjUzYTBlODcyYmYyOTA5NTYifQ%3D%3D; cf_chl_2=; cf_chl_prog=; cf_clearance=6hmz16MJ6A_FbmkQJi2UpjBgW4y3GiNKoEsk.2tHV0w-1652962681-0-150; cf_chl_prog=x14; cf_chl_2=4a9c2ad5e986a87'
token = ""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search',
                        default='localhost',
                        dest='word',
                        help='Search key words',
                        type=str
                        )
    parser.add_argument('-k', '--keywords',
                    action='store_true',
                    dest='getKeyWords',
                    help='Feed keywords'
                    )
    parser.add_argument('-l', '--lyrics',
                    action='store_true',
                    dest='getLyrics',
                    help='Feed lyrics'
                    )
    parser.add_argument('-c', '--csv',
                    action='store_true',
                    dest='getCsv',
                    help='Feed CSV'
                    )
    parser.add_argument('-g', '--graph',
                    action='store_true',
                    dest='showGraph',
                    help='Get Graph'
                    )
    args = parser.parse_args()

    if args.getCsv == True:
        Script.getMusic.getAllCSV(Script.getMusic.getAllDay(), cookie)

    if args.getLyrics == True:
        Script.getLyrics.getDBInfo(token)

    if args.getKeyWords == True:
        Script.getMostUsedWord.addKeywords()

    try:
        args.word
        Script.getTrend.searchInKeyWord(args.word)
    except:
        skip

    if args.showGraph == True:
        Script.getTrend.showGraph()
    
    

        
