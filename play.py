import re
import enchant
from nltk.corpus import words
import datetime
from redditScraper import getPositionsThatHaveExpired
from redditScraper import closePositions
from objects.validPositionObject import validPosition
from objects.closePositionObject import closePosition
from database import databaseTransactions

# position = validPosition("MSFT", "100", "06/28c")
# databaseTransactions.insertIntoNumberDataBase(50, position)


# close = closePosition(49, False, "MSFT")
# databaseTransactions.removePositionFromDatabase(close)


# me = datetime.datetime(2020, 6, 26)
# print(me.strftime('%Y-%m-%d'))

# positionsToClose = getPositionsThatHaveExpired()
# closePositions(positionsToClose)