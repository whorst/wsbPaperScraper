import re
import enchant
from nltk.corpus import words
import datetime
from objects.validPositionObject import validPosition
from database import databaseTransactions

position = validPosition("MSFT", "100", "04/19")

# databaseTransactions.insertIntoNumberDataBase(2, position.strikeDateTime)


me = datetime.datetime(2020, 6, 26)
print(me.strftime('%Y-%m-%d'))
print(databaseTransactions.getRecordsWithMatchingExpiryFromDatabase(me.strftime('%Y-%m-%d')))
