class validPosition:
    ticker = None
    price = None
    strikeDate = None
    isCall = None

    def __init__(self, newTicker, newPrice, newStrikeDate):
        self.ticker = newTicker.strip()
        self.price = newPrice.strip()
        self.strikeDate = newStrikeDate.strip()
        self.getPutOrCall()

    def __str__(self):
        return "{0} {1} {2} isCall: {3}".format(self.ticker, self.price, self.strikeDate, self.isCall)

    def getPutOrCall(self):
        priceLastCharacter = self.price[-1]
        dateLastCharacter = self.strikeDate[-1]

        if(priceLastCharacter.lower()=="p" or dateLastCharacter.lower()=="p"):
            self.isCall = False
        elif(priceLastCharacter.lower()=="c" or dateLastCharacter.lower()=="c"):
            self.isCall = True
