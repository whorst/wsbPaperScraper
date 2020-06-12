import re

import praw
from databaseTransactions import isTickerInDatabase
from objects.validPositionObject import validPosition
from paperTrading import paperTradingUtilities

reddit = praw.Reddit('bot1')


def isPutReferenceInComment(comment):
    return (("put" in comment.lower()) or "puts" in comment.lower())

def isCallReferenceInComment(comment):
    return (("call" in comment.lower()) or "calls" in comment.lower())


def getStrikeDatesInComment(comment):
    return re.findall(r'\s([0-9]{0,1}[0-9]{1}/[0-9]{1}[0-9]{0,1}[(p|c)]?)\s', comment)
# //ADD Capital p and c and lowercase P and C

def getPriceInComment(comment):
    return re.findall(r'\s([$]?[0-9]?[0-9]?[0-9]?[0-9]+[(p|c)]?)\s', comment)

def getTickerInComment(comment):
    return re.findall(r'[$]{0,2}\b(?!ALL|ER|PDT|FREE|RH|ATH|NBA|NFL|NHL|UP|FUCK|US|USSR|THE|ITM|AND|RIP|OTM|USD|EOD|CAD|PE|YOLO|I|SAAS|GIGS|GDP|GTFO|BTFD|EXP|MINS|PP|DD|LMAO|LOL|AMA|TLDR|RN|TME|GUH|FUK|WUT|WAT|WSB|TEH|WTF|FOMO|ROPE|IDK|AI|TP|IV|DOWN|IMO|PLS\b)[A-Z]{1,4}\b', comment)

def getvalidTickersFromPotentialTickers(potentialTickerList):
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
            "GDP", "GTFO", "BTFD", "EXP", "MINS", "PP", "DD", "LMAO", "LOL", "AMA", "TLDR", "RN", "TME", "GUH", "FUK",
            "WUT", "WAT","WSB", "TEH", "WTF", "FOMO", "IDK", "AI", "TP","IV", "DOWN", "IMO", "PLS"]

def returnValidpositionsInComment(comment):
    occurencesOfStrikeDate = getStrikeDatesInComment(comment)
    occurencesOfPrice = getPriceInComment(comment)
    occurencesOfTicker = getTickerInComment(comment)
    doesPutReferenceExist = isPutReferenceInComment(comment)
    doesCallReferenceExist = isCallReferenceInComment(comment)

    validTickers = getvalidTickersFromPotentialTickers(occurencesOfTicker)

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
                    validPositions = returnValidpositionsInComment(comment.body)
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
        validPositions = returnValidpositionsInComment(comment)
        if(validPositions):
            for pos in validPositions:
                if(pos.isCall != None):   ###Add Refactor Logic Here Later
                    paperTradingUtilities.openPosition(pos)
        else:
            continue

# testvalidComments()

for submission in reddit.subreddit("wallstreetbets").hot(limit=1):
    print(submission.title)
    if ("Daily Discussion Thread for" in  submission.title):
        returnValidpositionsInComment(submission.id)
    if ("What Are Your Moves Tomorrow" in submission.title):
        returnValidpositionsInComment(submission.id)