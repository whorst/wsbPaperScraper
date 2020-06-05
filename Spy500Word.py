import enchant
import databaseTransactions

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
    return databaseTransactions.isTickerInDatabase(word)
