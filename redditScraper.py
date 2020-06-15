import re

import praw
from database.databaseTransactions import getValidTickersInDatabase
from objects.validPositionObject import validPosition
from paperTrading import paperTradingUtilities


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
            "WUT", "WAT","WSB", "TEH", "WTF", "FOMO", "IDK", "AI", "TP","IV", "DOWN", "IMO", "PLS"]

def returnValidPositionsInComment(comment):
    occurencesOfStrikeDate = getStrikeDatesInComment(comment)
    occurencesOfPrice = getPriceInComment(comment)
    occurencesOfTicker = getTickerInComment(comment)
    doesPutReferenceExist = isPutReferenceInComment(comment)
    doesCallReferenceExist = isCallReferenceInComment(comment)

    validTickers = getValidTickersFromPotentialTickers(occurencesOfTicker)

    validTickersLength = len(validTickers)
    occurencesOfPriceLength = len(occurencesOfPrice)
    occurencesOfStrikeDateLength = len(occurencesOfStrikeDate)

    if((validTickersLength == occurencesOfPriceLength == occurencesOfStrikeDateLength) and validTickersLength!=0):
        return createNewPositions(doesCallReferenceExist, doesPutReferenceExist, occurencesOfPrice, occurencesOfStrikeDate, validTickers, validTickersLength)
    else:
        return []

def createNewPositions(doesCallReferenceExist, doesPutReferenceExist, occurencesOfPrice, occurencesOfStrikeDate,
                       occurencesOfTicker, validTickersLength):
    validPositions = []
    length = validTickersLength
    i = 0
    while (i < length):
        newPosition = validPosition(occurencesOfTicker[i], occurencesOfPrice[i], occurencesOfStrikeDate[i])
        if (newPosition.isCall == None):
            if (doesCallReferenceExist):
                newPosition.isCall = True
            if (doesPutReferenceExist):
                newPosition.isCall = False
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


def searchCommentsForPositions(submission_id):
    for comment in reddit.subreddit("wallstreetbets").stream.comments():
        try:
            commentSubmissionId = comment.link_id[-6:]
            if(commentSubmissionId == submission_id):
                if("http" not in comment.body):
                    validPositions = getValidTickersFromPotentialTickers(comment.body)
                    if (validPositions):
                        for pos in validPositions:
                            if (pos.isCall != None):  ###Add Refactor Logic Here Later
                                paperTradingUtilities.openPosition(pos)
                    else:
                        continue
        except UnicodeEncodeError:
            pass

def testvalidComments():
    for comment in open("resources/files/commentFile", "r"):
        validPositions = returnValidPositionsInComment(comment)
        if(validPositions):
            for pos in validPositions:
                if(pos.isCall != None):   ###Add Refactor Logic Here Later
                    paperTradingUtilities.openPosition(pos)
        else:
            continue

if __name__ == '__main__':
    reddit = praw.Reddit('bot1')
    # testvalidComments()

    for submission in reddit.subreddit("wallstreetbets").hot(limit=1):
        print(submission.title)
        if ("Daily Discussion Thread for" in submission.title):
            returnValidPositionsInComment(submission.id)
        if ("What Are Your Moves Tomorrow" in submission.title):
            returnValidPositionsInComment(submission.id)