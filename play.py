import re
import enchant
from nltk.corpus import words
from redditScraper import getPositionsThatHaveExpired
from objects.validPositionObject import validPosition
from objects.closePositionObject import closePosition
from database import databaseTransactions
from paperTrading import paperTradingUtilities
from timeUtilities import timeUtilities

import datetime
from pytz import timezone
tz = timezone('EST')
print(timeUtilities.getCurrentHourEst())

# position = validPosition("VXX", "40", "09/28c")
# paperTradingUtilities.openPosition(position)

# print(position)
# databaseTransactions.insertIntoNumberDataBase(50, position)


# close = closePosition(49, False, "MSFT")
# databaseTransactions.removePositionFromDatabase(close)

# print(datetime.datetime.utcnow().strftime('%Y-%m-%d %h:%m:%s'))

api = paperTradingUtilities.getRestApiInterface()
# print(type(api.get_barset("CLDR", "day", limit=1)["CLDR"][0].o))
print(api.get_asset("MSFT").__getattr__('shortable'))
# i+=1


# me = datetime.datetime(2020, 6, 26)
# print(me.strftime('%Y-%m-%d'))

# positionsToClose = getPositionsThatHaveExpired()
# closePositions(positionsToClose)