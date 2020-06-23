import alpaca_trade_api as tradeapi
from database import databaseTransactions


def openPosition(positionObject):
    api = getRestApiInterface()
    apiInverse = getRestApiInterfaceInverse()
    largestId = databaseTransactions.getLargestValueFromDatabase()
    newId = largestId+1
    ##ToDO Add logic here for short selling and inversing
    try:
        openNormalPositions(api, newId, positionObject)
        openInversePositions(apiInverse, newId, positionObject)
    except Exception as e:
        print("Failed fopr ID:" + str(newId))
        pass

def openNormalPositions(api, newId, positionObject):
        if (positionObject.isCall == True):
            api.submit_order(symbol=positionObject.ticker, qty=1, side='buy', time_in_force='gtc', type='market',
                             client_order_id=str(newId))
            databaseTransactions.insertIntoNumberDataBase(newId)
        elif (positionObject.isCall == False):
            api.submit_order(symbol=positionObject.ticker, qty=1, side='sell', time_in_force='gtc', type='market',
                             client_order_id=str(newId))
            databaseTransactions.insertIntoNumberDataBase(newId)


def openInversePositions(api, newId, positionObject):
    if (positionObject.isCall == False):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='buy', time_in_force='gtc', type='market',
                         client_order_id=str(newId))
        databaseTransactions.insertIntoNumberDataBaseInverse(newId)
    elif (positionObject.isCall == True):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='sell', time_in_force='gtc', type='market',
                         client_order_id=str(newId))
        databaseTransactions.insertIntoNumberDataBaseInverse(newId)


def getRestApiInterface():
    #authentication and connection details
    api_key = 'PKVQBAVIQJ9E6XBFZBTR'
    api_secret = 'jqEuu2wuPtijD9LPVRbdkZGSHXqg4p4VTR0FdQ95'
    base_url = 'https://paper-api.alpaca.markets'
    #instantiate REST API
    return tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

def getRestApiInterfaceInverse():
    ##Inverse
    api_key = 'PKQGSGYKHSFVBATRYEQ0'
    api_secret = 'jPgTr/xj0viMAwAg9CCcSDV7bG3FTZisF6x3qzKZ'
    base_url = 'https://paper-api.alpaca.markets'
    #instantiate REST API
    return tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

def getCurrentTickerPrice(api, ticker):
    tickerJson = api.alpha_vantage.current_quote(ticker)
    return tickerJson["05. price"]



