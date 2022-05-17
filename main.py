from unittest import skip
import Script.getMusic
import Script.getLyrics
import Script.getMostUsedWord
import Script.getTrend
import argparse


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
    args = parser.parse_args()

    if args.getCsv == True:
        Script.getMusic.getAllCSV(Script.getMusic.getAllDay())

    if args.getLyrics == True:
        Script.getLyrics.getDBInfo()

    if args.getKeyWords == True:
        Script.getMostUsedWord.addKeywords()

    try:
        args.search
        Script.getTrend.searchInKeyWord(args.word)
    except:
        skip
    
    

        
