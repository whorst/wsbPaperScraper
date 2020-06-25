import alpaca_trade_api as tradeapi
from database import databaseTransactions


def openPosition(positionObject):
    api = getRestApiInterface()
    apiInverse = getRestApiInterfaceInverse()
    largestId = databaseTransactions.getLargestValueFromDatabase()
    if(not largestId):
        largestId = 0
    newId = largestId+1
    ##ToDO Add logic here for short selling and inversing
    try:
        openNormalPositions(api, newId, positionObject)
        openInversePositions(apiInverse, newId, positionObject)
    except Exception as e:
        print("Opening Position Failed for ID:" + str(newId))
        pass

def closeNormalPositions(api, id):
    api.close_position(id)

def closeInversePositions(api, id):
    api.close_position(id)


def closePositions(idList):
    api = getRestApiInterface()
    apiInverse = getRestApiInterfaceInverse()
    for id in idList:
        try:
            closeNormalPositions(api, id)
            closeInversePositions(apiInverse, id)
        except Exception as e:
            print("Closing Position Failed for ID:" + str(id))
            pass

def openNormalPositions(api, newId, positionObject):
        if (positionObject.isCall == True):
            api.submit_order(symbol=positionObject.ticker, qty=1, side='buy', time_in_force='gtc', type='market',
                             client_order_id=str(newId))
            databaseTransactions.insertIntoNumberDataBase(newId, positionObject.strikeDateTime, int(positionObject.isCall))
        elif (positionObject.isCall == False):
            api.submit_order(symbol=positionObject.ticker, qty=1, side='sell', time_in_force='gtc', type='market',
                             client_order_id=str(newId))
            databaseTransactions.insertIntoNumberDataBase(newId, positionObject.strikeDateTime, int(positionObject.isCall))

def openInversePositions(api, newId, positionObject):
    if (positionObject.isCall == False):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='buy', time_in_force='gtc', type='market',
                         client_order_id=str(newId))
        databaseTransactions.insertIntoNumberDataBaseInverse(newId, positionObject.strikeDateTime, int(not positionObject.isCall))
    elif (positionObject.isCall == True):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='sell', time_in_force='gtc', type='market',
                         client_order_id=str(newId))
        databaseTransactions.insertIntoNumberDataBaseInverse(newId, positionObject.strikeDateTime, int(not positionObject.isCall))

def closePositionsById():
    api = getRestApiInterface()
    apiInverse = getRestApiInterfaceInverse()

def getRestApiInterface():
    #authentication and connection details
    api_key = 'PK22MZ9LJ5G2NA4UCPHI'
    api_secret = 'yRa4pT3tECXJ4ij88SnQVJJeu972exmxtqg8lxXR'
    base_url = 'https://paper-api.alpaca.markets'
    #instantiate REST API
    return tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

def getRestApiInterfaceInverse():
    ##Inverse
    api_key = 'PK4P8ZBJ35OCTOLNYHMA'
    api_secret = 'SSs3404C9EvXjl3RwtjOnMA2WmDn/kof9tMljBSk'
    base_url = 'https://paper-api.alpaca.markets'
    #instantiate REST API
    return tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

def getCurrentTickerPrice(api, ticker):
    tickerJson = api.alpha_vantage.current_quote(ticker)
    return tickerJson["05. price"]



