import re
from idlelib.multicall import r

#(\s|[][$]?[A-Z]{0,1}[A-Z]{0,1}[A-Z]{1}[A-Z]{1})[,]?\s

import praw
from databaseTransactions import isTickerInDatabase
from objects.validPositionObject import validPosition
from datetime import date

# Valid regex to get date with p or c appended

reddit = praw.Reddit('bot1')

# subreddit = reddit.subreddit("https://www.reddit.com/r/wallstreetbets/")


def getStrikeDatesInComment(comment):
    return re.findall(r'\s([0-9]{0,1}[0-9]{1}/[0-9]{1}[0-9]{0,1}[(p|c)]?)\s', comment)
# //ADD Capital p and c and lowercase P and C

def getPriceInComment(comment):
    return re.findall(r'\s([$]?[0-9]?[0-9]?[0-9]?[0-9]+[(p|c)]?)\s', comment)

def getTickerInComment(comment):
    return re.findall(r'[$]{0,2}\b(?!ALL|ER|PDT|FREE|ATH|NBA|NFL|NHL|UP|FUCK|US|USSR|THE|ITM|AND|RIP|OTM|USD|EOD|CAD|PE|YOLO|I|SAAS|GIGS|GDP|GTFO|BTFD|EXP|MINS|PP|DD|LMAO|LOL|AMA|TLDR|RN|TME|GUH|FUK|WUT|WAT|WSB|TEH|WTF|FOMO|ROPE|IDK|AI|TP|IV|DOWN|IMO|PLS\b)[A-Z]{1,4}\b', comment)

def getvalidTickersFromPotentialTickers(potentialTickerList):
    validTickerList = []
    for potentialTicker in potentialTickerList:
        if potentialTicker in getExclusionWord():
            continue
        formattedTicker = potentialTicker.strip()
        formattedTicker = formattedTicker.replace('$','')
        isValidTicker = isTickerInDatabase(formattedTicker)
        if(isValidTicker):
            validTickerList.append(formattedTicker)
    return validTickerList

def getMostCommonTickers():
    return ["MSFT", "BA", "SPY", "BABA", "SQQQ", "SPXS", "TSLA", "DIS", "AMZN", "AMD", "LYFT", "NDAQ", "QQQ", "SPCE",
            "FB", "DKNG", "ZM", "VXX", "WORK", "LULU", "MU", "DOQ", "DIS", "DAL", "HOG", "SNAP"]

def getExclusionWord():
    return ["ALL", "US", "USSR", "THE", "ITM", "AND", "RIP" "OTM", "ASAP", "USD", "EOD", "CAD", "PE", "YOLO", "I", "SAAS", "GIGS",
            "GDP", "GTFO", "BTFD", "EXP", "MINS", "PP", "DD", "LMAO", "LOL", "AMA", "TLDR", "RN", "TME", "GUH", "FUK",
            "WUT", "WAT","WSB", "TEH", "WTF", "FOMO", "IDK", "AI", "TP","IV", "DOWN", "IMO", "PLS"]

def validateDatePriceAndTickerInComment(comment):
    occurencesOfStrikeDate = getStrikeDatesInComment(comment)
    occurencesOfPrice = getPriceInComment(comment)
    occurencesOfTicker = getTickerInComment(comment)
    validTickers = getvalidTickersFromPotentialTickers(occurencesOfTicker)

    if(False):
        if (bool(validTickers) and (bool(occurencesOfPrice) or bool(occurencesOfStrikeDate))):
            print(comment + "\n")
            file = open("resources/files/commentFile", "a")
            file.write(comment + "\n\n")
            file.close()
    else:
        validTickersLength = len(validTickers)
        occurencesOfPriceLength = len(occurencesOfPrice)
        occurencesOfStrikeDateLength = len(occurencesOfStrikeDate)

        if(validTickersLength == occurencesOfPriceLength == occurencesOfStrikeDateLength):
            printValidPositions(comment, occurencesOfPrice, occurencesOfStrikeDate, occurencesOfTicker, validTickersLength)


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


def printValidComments(submission_id):
    for comment in reddit.subreddit("wallstreetbets").stream.comments():
        try:
            commentSubmissionId = comment.link_id[-6:]
            if(commentSubmissionId == submission_id):
                if("http" not in comment.body):
                    validateDatePriceAndTickerInComment(comment.body)
        except UnicodeEncodeError:
            pass

def testvalidComments():
    for comment in open("resources/files/commentFile", "r"):
        validateDatePriceAndTickerInComment(comment)

# testvalidComments()

for submission in reddit.subreddit("wallstreetbets").hot(limit=1):
    print(submission.title)
    if ("Daily Discussion Thread for" in  submission.title):
        printValidComments(submission.id)
    if ("What Are Your Moves Tomorrow" in submission.title):
        printValidComments(submission.id)

# Traceback (most recent call last):
#   File "C:/Users/William/PycharmProjects/redditCommentScraper/redditScraper.py", line 58, in <module>
#     printValidComments(submission.id)
#   File "C:/Users/William/PycharmProjects/redditCommentScraper/redditScraper.py", line 46, in printValidComments
#     for comment in reddit.subreddit("wallstreetbets").stream.comments():
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\praw\models\util.py", line 186, in stream_generator
#     for item in reversed(list(function(limit=limit, **function_kwargs))):
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\praw\models\listing\generator.py", line 61, in __next__
#     self._next_batch()
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\praw\models\listing\generator.py", line 71, in _next_batch
#     self._listing = self._reddit.get(self.url, params=self.params)
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\praw\reddit.py", line 490, in get
#     return self._objectify_request(method="GET", params=params, path=path)
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\praw\reddit.py", line 573, in _objectify_request
#     self.request(
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\praw\reddit.py", line 726, in request
#     return self._core.request(
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\prawcore\sessions.py", line 332, in request
#     return self._request_with_retries(
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\prawcore\sessions.py", line 252, in _request_with_retries
#     return self._do_retry(
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\prawcore\sessions.py", line 162, in _do_retry
#     return self._request_with_retries(
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\prawcore\sessions.py", line 252, in _request_with_retries
#     return self._do_retry(
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\prawcore\sessions.py", line 162, in _do_retry
#     return self._request_with_retries(
#   File "C:\Users\William\PycharmProjects\redditCommentScraper\venv\lib\site-packages\prawcore\sessions.py", line 265, in _request_with_retries
#     raise self.STATUS_EXCEPTIONS[response.status_code](response)
# prawcore.exceptions.ServerError: received 503 HTTP response





# Traceback (most recent call last):
#   File "C:/Users/William/PycharmProjects/redditCommentScraper/redditScraper.py", line 27, in <module>
#     getContinuousRedditStream(submission, submission.id)
#   File "C:/Users/William/PycharmProjects/redditCommentScraper/redditScraper.py", line 21, in getContinuousRedditStream
#     file.write(comment.body + "\n\n")
#   File "C:\Users\William\AppData\Local\Programs\Python\Python38-32\lib\encodings\cp1252.py", line 19, in encode
#     return codecs.charmap_encode(input,self.errors,encoding_table)[0]
# UnicodeEncodeError: 'charmap' codec can't encode characters in position 122-123: character maps to <undefined>
# Traceback (most recent call last):
#   File "C:/Users/William/PycharmProjects/redditCommentScraper/redditScraper.py", line 27, in <module>
#     getContinuousRedditStream(submission, submission.id)
#   File "C:/Users/William/PycharmProjects/redditCommentScraper/redditScraper.py", line 21, in getContinuousRedditStream
#     file.write(comment.body + "\n\n")
#   File "C:\Users\William\AppData\Local\Programs\Python\Python38-32\lib\encodings\cp1252.py", line 19, in encode
#     return codecs.charmap_encode(input,self.errors,encoding_table)[0]
# UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f614' in position 29: character maps to <undefined>