import re
from idlelib.multicall import r

import praw
from datetime import date

# Valid regex to get date with p or c appended

reddit = praw.Reddit('bot1')

# subreddit = reddit.subreddit("https://www.reddit.com/r/wallstreetbets/")

# today = date.today()
# print(subreddit.hot())
# exit(0)

def getStrikeDatesInComment(comment):
    return re.findall(r'\s([0-9]{0,1}[0-9]{1}/[0-9]{1}[0-9]{0,1}[(p|c)]?)\s', comment.body)

def getPriceInComment(comment):
    return re.findall(r'\s([$]?[0-9]?[0-9]?[0-9]?[0-9]+[(p|c)]?)\s', comment.body)

def getTickerInComment(comment):
    return re.findall(r'([$]?[A-Z]?[A-Z]?[A-Z]{1}[A-Z]{1})\s', comment.body)

def getMostCommonTickers():
    return ["MSFT", "BA", "SPY", "BABA", "SQQQ", "SPXS", "TSLA", "DIS", "AMZN", "AMD", "LYFT", "NDAQ", "QQQ", "SPCE", "FB", "DKNG", "ZM", "VXX"]

def getExclusionWord():
    return ["ALL", "US", "USSR", "ITM", "AND", "OTM", "USD", "CAD", "PE", "I", "SAAS", "GTFO", "BTFD", "DD", "LMAO", "LOL", "AMA"]

def validateDatePriceAndTickerInComment(comment):
    occurencesOfStrikeDate = getStrikeDatesInComment(comment)
    occurencesOfPrice = getPriceInComment(comment)
    occurencesOfTicker = getTickerInComment(comment)
    if (bool(occurencesOfPrice) and bool(occurencesOfStrikeDate) ):
        print(comment.body + "\n")


def printValidComments(submission_id):
    for comment in reddit.subreddit("wallstreetbets").stream.comments():
        try:
            commentSubmissionId = comment.link_id[-6:]
            if(commentSubmissionId == submission_id):
                if("http" not in comment.body):
                    validateDatePriceAndTickerInComment(comment)
                    # print(comment.body + "\n")
                    # file = open("commentFile", "a")
                    # file.write(comment.body + "\n\n")
                    # file.close()
        except UnicodeEncodeError:
            pass

for submission in reddit.subreddit("wallstreetbets").hot(limit=1):
    print(submission.title)
    if ("Daily Discussion Thread for" in  submission.title):
        printValidComments(submission.id)
    if ("What Are Your Moves Tomorrow" in submission.title):
        printValidComments(submission.id)


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