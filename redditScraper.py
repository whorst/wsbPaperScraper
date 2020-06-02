from idlelib.multicall import r

import praw
from datetime import date

reddit = praw.Reddit('bot1')

# subreddit = reddit.subreddit("https://www.reddit.com/r/wallstreetbets/")

# today = date.today()
# print(subreddit.hot())
# exit(0)

def getContinuousRedditStream(submission, submission_id):
    for comment in reddit.subreddit("wallstreetbets").stream.comments():
        try:
            commentSubmissionId = comment.link_id[-6:]
            if(commentSubmissionId == submission_id):
                if("/" in comment.body):
                    print(comment.body + "\n")
                    file = open("commentFile", "a")
                    file.write(comment.body + "\n\n")
                    file.close()
        except UnicodeEncodeError:
            pass

for submission in reddit.subreddit("wallstreetbets").hot(limit=1):
    print(submission.title)
    if ("Daily Discussion Thread for" in  submission.title):
        getContinuousRedditStream(submission, submission.id)
    if ("What Are Your Moves Tomorrow" in submission.title):
        getContinuousRedditStream(submission, submission.id)


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