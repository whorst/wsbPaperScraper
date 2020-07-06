from _datetime import datetime
import re
from paperTrading.paperTradingUtilities import getPriceOfStock

class validPosition:
    ticker = None
    price = None
    strikeDate = None
    strikeDateTime = None
    isCall = None


    def __init__(self, newTicker, newPrice, newStrikeDate):
        self.ticker = newTicker.strip()
        newPrice = newPrice.strip()
        newPrice = newPrice.replace('$','')
        priceWithoutStrike = self.getPriceWithoutPutOrCall(newPrice)
        priceIntOrFloat = self.getPriceInIntOrFloat(priceWithoutStrike)
        self.price = priceIntOrFloat
        self.formatStrikeDateAndDateTime(newStrikeDate.strip())
        self.getPutOrCall(newPrice)

    def __str__(self):
        return "{0} {1} {2} isCall: {3}".format(self.ticker, self.price, self.strikeDate, self.isCall)

    def getDateTimeObjectFromStrikeDate(self, day, month, year):
        return datetime(int(year), int(month), int(day))

    def formatStrikeDateAndDateTime(self, date):
        numArray = date.split("/")
        strikeMonth = numArray[0].lstrip('0')
        strikeDay = numArray[1].lstrip('0')
        currentMonth = str(datetime.utcnow().strftime("%m")).lstrip('0')
        currentYear = str(datetime.utcnow().strftime("%Y"))

        if (strikeMonth < currentMonth):
            currentYear = str(int(currentYear) + 1)

        self.strikeDate = date

        strikeMonth = re.sub('[^0-9]','', strikeMonth)
        strikeDay = re.sub('[^0-9]','', strikeDay)

        self.strikeDateTime = self.getDateTimeObjectFromStrikeDate(strikeDay, strikeMonth, currentYear)

    @staticmethod
    def getPriceWithoutPutOrCall(price):
        priceWithoutStrike = price.upper()
        priceWithoutStrike = priceWithoutStrike.replace('C', '')
        priceWithoutStrike = priceWithoutStrike.replace('P', '')
        return priceWithoutStrike

    @staticmethod
    def getPriceInIntOrFloat(price):
        if ('.' in price):
            return float(price)
        else:
            return int(price)

    def getPutOrCall(self, unformattedPrice):
        priceLastCharacter = unformattedPrice[-1]
        dateLastCharacter = self.strikeDate[-1]

        if (priceLastCharacter.lower() == "p" or dateLastCharacter.lower() == "p"):
            self.isCall = False
        elif (priceLastCharacter.lower() == "c" or dateLastCharacter.lower() == "c"):
            self.isCall = True
        else:
            try:
                priceOfStock = getPriceOfStock(self.ticker)
                if(priceOfStock):
                    if(self.price > priceOfStock):
                        self.isCall = True
                    if (self.price < priceOfStock):
                        self.isCall = False
            except Exception as e:
                print("Couldnt get stock price")
                return