from unittest import skip
import Script.getMusic
import Script.getLyrics
import Script.getMostUsedWord
import Script.getTrend
import argparse

cookie = ''
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
    
    

        
