import alpaca_trade_api as tradeapi
from objects import validPositionObject
import databaseTransactions

def openPosition(positionObject, isInverse):
    api = getRestApiInterface(isInverse)
    # getCurrentTickerPrice(api, positionObject.ticker)
    largestId = databaseTransactions.getLargestValueFromDatabase()
    newId = largestId+1
    if(positionObject.isCall==True):
        ##ToDO Add logic here for short selling and inversing
        api.submit_order(symbol=positionObject.ticker, qty=1, side='buy', time_in_force='gtc', type='market', client_order_id=str(newId))
        databaseTransactions.insertIntoNumberDataBase(newId)
    if(positionObject.isCall==False):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='buy', time_in_force='gtc', type='market', client_order_id=str(newId))
        databaseTransactions.insertIntoNumberDataBase(newId)
    print(newId)
    exit(1)

def getRestApiInterface(isInverse):
    if(not isInverse):
        #authentication and connection details
        api_key = 'PKVQBAVIQJ9E6XBFZBTR'
        api_secret = 'jqEuu2wuPtijD9LPVRbdkZGSHXqg4p4VTR0FdQ95'
        base_url = 'https://paper-api.alpaca.markets'
        #instantiate REST API
        return tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
    elif(isInverse):
        ##Inverse
        api_key = 'PKQGSGYKHSFVBATRYEQ0'
        api_secret = 'jPgTr/xj0viMAwAg9CCcSDV7bG3FTZisF6x3qzKZ'
        base_url = 'https://paper-api.alpaca.markets'
        #instantiate REST API
        return tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

def getCurrentTickerPrice(api, ticker):
    tickerJson = api.alpha_vantage.current_quote(ticker)
    return tickerJson["05. price"]



