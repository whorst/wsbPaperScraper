import re
import enchant
from nltk.corpus import words
import datetime
from objects.validPositionObject import validPosition
from database import databaseTransactions
from paperTrading.paperTradingUtilities import openPosition

position = validPosition("MSFT", "100p", "04/19")

# databaseTransactions.insertIntoNumberDataBase(2, position.strikeDateTime)

openPosition(position)

# me = datetime.datetime(2020, 6, 26)
# print(me.strftime('%Y-%m-%d'))
# print(databaseTransactions.getRecordsWithMatchingExpiryFromDatabase(me.strftime('%Y-%m-%d')))
