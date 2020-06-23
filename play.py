import re
import enchant
from nltk.corpus import words
from objects.validPositionObject import validPosition

position = validPosition("MSFT", "100", "04/19")

print(position.strikeDate)