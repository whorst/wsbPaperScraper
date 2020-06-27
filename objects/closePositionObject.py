class closePosition:
    id = None
    isCall = None
    isCallInverse = None
    ticker = None

    def __str__(self):
        print(self.ticker, self.id, self.isCall, self.isCallInverse)

    def __init__(self, id, isCall, ticker):
        self.ticker = ticker
        self.id = id
        self.isCall = bool(isCall)
        self.isCallInverse = not bool(isCall)