from _datetime import datetime

class validPosition:
    ticker = None
    price = None
    strikeDate = None
    strikeDateTime = None
    isCall = None

    def __init__(self, newTicker, newPrice, newStrikeDate):
        self.ticker = newTicker.strip()
        self.price = newPrice.strip()
        self.strikeDate = self.formatStrikeDate(newStrikeDate.strip())
        self.getPutOrCall()

    def __str__(self):
        return "{0} {1} {2} isCall: {3}".format(self.ticker, self.price, self.strikeDate, self.isCall)

    def getDateTimeObjectFromStrikeDate(self, day, month, year):
        return datetime(int(year), int(month), int(day))

    def formatStrikeDate(self, date):
        numArray = date.split("/")
        strikeMonth = numArray[0].lstrip('0')
        strikeDay = numArray[1].lstrip('0')
        currentMonth = str(datetime.utcnow().strftime("%m")).lstrip('0')
        currentYear = str(datetime.utcnow().strftime("%Y"))

        if (strikeMonth < currentMonth):
            currentYear = str(int(currentYear) + 1)

        self.strikeDateTime = self.getDateTimeObjectFromStrikeDate(strikeDay, strikeMonth, currentYear)

        return "{}/{}/{}".format(strikeMonth, strikeDay, currentYear)

    def getPutOrCall(self):
        priceLastCharacter = self.price[-1]
        dateLastCharacter = self.strikeDate[-1]

        if (priceLastCharacter.lower() == "p" or dateLastCharacter.lower() == "p"):
            self.isCall = False
        elif (priceLastCharacter.lower() == "c" or dateLastCharacter.lower() == "c"):
            self.isCall = True
