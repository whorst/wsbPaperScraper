import re
import enchant
from nltk.corpus import words
from objects.validPositionObject import validPosition
from database import databaseTransactions

position = validPosition("MSFT", "100", "04/19")

databaseTransactions.insertIntoNumberDataBase(2, position.strikeDateTime)