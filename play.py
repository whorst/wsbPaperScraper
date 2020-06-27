import re
import enchant
from nltk.corpus import words
import datetime
from redditScraper import getPositionsThatHaveExpired
from redditScraper import closePositions
from objects.validPositionObject import validPosition
from database import databaseTransactions

position = validPosition("MSFT", "100", "06/27p")

databaseTransactions.insertIntoNumberDataBase(48, position)


me = datetime.datetime(2020, 6, 26)
print(me.strftime('%Y-%m-%d'))

# positionsToClose = getPositionsThatHaveExpired()
# closePositions(positionsToClose)