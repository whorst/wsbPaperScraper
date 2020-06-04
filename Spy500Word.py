import enchant

from nltk.corpus import words as nltk_words


def isEnglishWordATicker(word):
    tickerArray = []
    englishWordTickerFile = open("resources/files/tickersThatAreWords", "r")
    for line in englishWordTickerFile:
        ticker = str(line.strip())
        tickerArray.append(ticker)
    englishWordTickerFile.close()
    return word in tickerArray



def isPossibleTickerUsable(word):
    dictionary = dict.fromkeys(nltk_words.words(), None)
    ticker = word.strip()
    try:
        isWordInDictionary = dictionary[ticker.lower()]
        dictionary.clear()
        if(isWordInDictionary == None):
            #If it is an english word, check if it exists as an english word in the preselected english word ticker list
           return isEnglishWordATicker(ticker)
    except KeyError:
        #If it's not an english word, its probably a ticker. Return True
        dictionary.clear()
        return True

def findTickerThatisEnglishWord():
    dictionary = dict.fromkeys(nltk_words.words(), None)

    fileTicker = open("resources/files/tickerFile", "r")
    for line in fileTicker:
        ticker = line.strip()
        try:
            d = dictionary[ticker.lower()]
            print(ticker)
        except KeyError:
            pass
        # print(str(line) + "\n")
    fileTicker.close()