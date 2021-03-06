import re

import praw
from database.databaseTransactions import getValidTickersInDatabase
from database.databaseTransactions import getRecordsWithMatchingExpiryFromDatabase
from objects.validPositionObject import validPosition
from paperTrading import paperTradingUtilities
from timeUtilities import timeUtilities


def isStrikePriceRidiculouslyHighOrLow(strikePrice, ticker):
    actualPrice = paperTradingUtilities.getPriceOfStock(ticker)
    actualPriceUpperBound = actualPrice + (actualPrice *.65)
    actualPriceLowerBound = actualPrice - (actualPrice *.65)
    isRidiculouslyHighOrLow = ((strikePrice > actualPriceUpperBound) or (strikePrice < actualPriceLowerBound))
    if(isRidiculouslyHighOrLow):
        comment = (f"Ticker: {ticker}, Actual Price: {actualPrice}, Upper: {actualPriceUpperBound}, Lower {actualPriceLowerBound}, Stated Price: {strikePrice}")
        outFile = open("resources/files/ridiculouslyHighOrLowReason", "a")
        outFile.write(comment)
        outFile.write("\n\n")
        outFile.close()
    return isRidiculouslyHighOrLow

def isPutReferenceInComment(comment):
    return bool(re.findall(r'\bput\b|\bputs\b', comment.lower()))

def isCallReferenceInComment(comment):
    return bool(re.findall(r'\bcall\b|\bcalls\b', comment.lower()))

def getStrikeDatesInComment(comment):
    return re.findall(r'(?<!\S)[0-9]{0,1}[0-9]{1}/[0-9]{1}[0-9]{0,1}[(p|c|P|C)]?(?!\S)', comment)
# //ADD Capital p and c and lowercase P and C

def getPriceInComment(comment):
    return re.findall(r'(?<!\S)\$?[0-9]?[0-9]?[0-9]?[0-9]{1}\.?[0-9]{1,2}?[(p|c|P|C)]?(?!\S)', comment)

def getTickerInComment(comment):
    return re.findall(r'[$]{0,2}\b(?!ALL|ER|PDT|FREE|RH|ATH|NBA|NFL|NHL|UP|FUCK|US|USSR|THE|ITM|AND|RIP|OTM|USD|EOD|CAD|PE|YOLO|I|SAAS|GIGS|GDP|GTFO|BTFD|EXP|MINS|PP|DD|LMAO|LOL|AMA|TLDR|RN|TME|GUH|FUK|WUT|WAT|WSB|TEH|WTF|FOMO|ROPE|IDK|AI|TP|IV|DOWN|IMO|PLS\b)[A-Z]{1,4}\b', comment)

def isTickerInDatabase(ticker):
    return bool(getValidTickersInDatabase(ticker))

def getValidTickersFromPotentialTickers(potentialTickerList):
    validTickerList = []
    for potentialTicker in potentialTickerList:
        if potentialTicker in getExclusionWord():
            continue
        strippedTicker = potentialTicker.strip()
        correctTicker = strippedTicker.replace('$','')
        isValidTicker = isTickerInDatabase(correctTicker)
        if(isValidTicker):
            validTickerList.append(correctTicker)
    return validTickerList

def getMostCommonTickers():
    return ["MSFT", "BA", "SPY", "BABA", "SQQQ", "SPXS", "TSLA", "DIS", "AMZN", "AMD", "LYFT", "NDAQ", "QQQ", "SPCE",
            "FB", "DKNG", "ZM", "VXX", "WORK", "LULU", "MU", "DOQ", "DIS", "DAL", "HOG", "SNAP"]

def getExclusionWord():
    return ["ALL", "US", "USSR", "THE", "ITM", "AND", "RIP" "OTM", "ASAP", "USD", "EOD", "CAD", "PE", "YOLO", "I", "SAAS", "GIGS",
            "GDP", "GTFO", "BTFD", "EXP", "OTM", "MINS", "PP", "DD", "LMAO", "LOL", "AMA", "TLDR", "RN", "TME", "GUH", "FUK",
            "WUT", "WAT","WSB", "TEH", "WTF", "FOMO", "IDK", "AI", "TP", "IV", "DOWN", "IMO", "PLS"]

def returnValidPositionsInComment(comment):
    occurencesOfStrikeDate = getStrikeDatesInComment(comment)
    occurencesOfPrice = getPriceInComment(comment)
    occurencesOfTicker = getTickerInComment(comment)

    validTickers = getValidTickersFromPotentialTickers(occurencesOfTicker)

    validTickersLength = len(validTickers)
    occurencesOfPriceLength = len(occurencesOfPrice)
    occurencesOfStrikeDateLength = len(occurencesOfStrikeDate)

    if((validTickersLength == occurencesOfPriceLength == occurencesOfStrikeDateLength) and validTickersLength!=0):
        return createNewPositions(occurencesOfPrice, occurencesOfStrikeDate, validTickers, validTickersLength)
    else:
        return []

def createNewPositions(occurencesOfPrice, occurencesOfStrikeDate,
                       occurencesOfTicker, validTickersLength):
    validPositions = []
    length = validTickersLength
    i = 0
    while (i < length):
        try:
            newPosition = validPosition(occurencesOfTicker[i], occurencesOfPrice[i], occurencesOfStrikeDate[i])
        except ValueError:
            continue


        validPositions.append(newPosition)
        i += 1
    return validPositions


def printValidPositions(comment, occurencesOfPrice, occurencesOfStrikeDate, occurencesOfTicker, validTickersLength):
    validPositions = []
    length = validTickersLength
    i = 0
    while (i < length):
        newPosition = validPosition(occurencesOfTicker[i], occurencesOfPrice[i], occurencesOfStrikeDate[i])
        validPositions.append(newPosition)
        outFile = open("resources/files/commentFileOut", "a")
        outFile.write("\n\n")
        outFile.write(comment)
        outFile.write("\n")
        outFile.write(newPosition.__str__())
        outFile.write("\n\n")
        outFile.close()
        i += 1


def searchCommentsForPositions(submission_id, commentObject):
        try:
            commentSubmissionId = commentObject.link_id[-6:]
            if((commentSubmissionId == submission_id) and ("http" not in commentObject.body)):
                validPositions = returnValidPositionsInComment(commentObject.body)
                if (validPositions):
                    for pos in validPositions:
                        if((pos.isCall != None) and (not isStrikePriceRidiculouslyHighOrLow(pos.price, pos.ticker))):
                            print(pos.__str__())
                            paperTradingUtilities.openPosition(pos)
        except UnicodeEncodeError:
            pass

def testvalidComments():
    for comment in open("resources/files/commentFile", "r"):
        validPositions = returnValidPositionsInComment(comment)
        if(validPositions):
            for pos in validPositions:
                if((pos.isCall != None) and (not isStrikePriceRidiculouslyHighOrLow(pos.price, pos.ticker))):
                    paperTradingUtilities.openPosition(pos)
        else:
            continue

def getPositionsThatHaveExpired():
    day = timeUtilities.getCurrentDayEst()
    return getRecordsWithMatchingExpiryFromDatabase(day)

    # me = datetime.datetime(2020, 6, 26)
    # day = me
    # return getRecordsWithMatchingExpiryFromDatabase(day.strftime('%Y-%m-%d'))


if __name__ == '__main__':
    reddit = praw.Reddit('bot1')
    # testvalidComments()

    for submission in reddit.subreddit("wallstreetbets").hot(limit=1):
        print(submission.title)
        if ("Daily Discussion Thread for" in submission.title):
            for commentObject in reddit.subreddit("wallstreetbets").stream.comments():
                if(timeUtilities.getCurrentHourEst() != "17"):
                    searchCommentsForPositions(submission.id, commentObject)
                else:
                    positionsToClose = getPositionsThatHaveExpired()
                    if (positionsToClose):
                        paperTradingUtilities.closePositions(positionsToClose)
                    exit(0)

        if ("What Are Your Moves Tomorrow" in submission.title):
            for comment in reddit.subreddit("wallstreetbets").stream.comments():
                if (timeUtilities.getCurrentHourEst() != "17"):
                    searchCommentsForPositions(submission.id, comment)
                else:
                    positionsToClose = getPositionsThatHaveExpired()
                    if (positionsToClose):
                        paperTradingUtilities.closePositions(positionsToClose)
                    exit(0)