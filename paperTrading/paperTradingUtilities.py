import alpaca_trade_api as tradeapi
from database import databaseTransactions

# Add logic for closing position at end of the day, figuring out why adding to DB doesnt work

def isStockShortable(ticker):
    api = getRestApiInterface()
    resultInDatabase = databaseTransactions.getIsTickerShortable(ticker)[0]
    if(resultInDatabase == None):
        apiCallIsShortable = api.get_asset(ticker).__getattr__('shortable')
        databaseTransactions.insertIsTickerShortable(ticker, int(apiCallIsShortable))
        return apiCallIsShortable
    return bool(resultInDatabase)

def writeFailureToFile(msg):
    outFile = open("resources/files/closePositionFailure", "a")
    outFile.write(msg+"\n\n")
    outFile.close()

def openPosition(positionObject):
    api = getRestApiInterface()
    apiInverse = getRestApiInterfaceInverse()
    largestId = databaseTransactions.getLargestValueFromDatabase()
    if(not largestId):
        largestId = 0
    newId = largestId+1
    try:
        if(isStockShortable(positionObject.ticker)):
            openNormalPositions(api, newId, positionObject)
            openInversePositions(apiInverse, newId, positionObject)
            insertPositionObjectIntoDB(newId, positionObject)
    except Exception as e:
        print("Opening Position Failed for ID:" + str(newId) + " For reason" + str(e))
        pass

def closeNormalPositions(api, positionObject):
    if (positionObject.isCall == True):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='sell', time_in_force='gtc', type='market')
    elif (positionObject.isCall == False):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='buy', time_in_force='gtc', type='market')

def closeInversePositions(api, positionObject):
    if (positionObject.isCallInverse == True):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='sell', time_in_force='gtc', type='market')
    elif (positionObject.isCallInverse == False):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='buy', time_in_force='gtc', type='market')

def closePositions(closePositionList):
    api = getRestApiInterface()
    apiInverse = getRestApiInterfaceInverse()
    for closePositionObject in closePositionList:
        try:
            print("Closed Position" + str(closePositionObject.id))
            closeNormalPositions(api, closePositionObject)
            closeInversePositions(apiInverse, closePositionObject)
            databaseTransactions.removePositionFromDatabase(closePositionObject)
        except Exception as e:
            print("Closing Position Failed for ID:" + str(closePositionObject.id) + " For reason" + str(e))
            writeFailureToFile(str(e))
            pass

def insertPositionObjectIntoDB(newId, positionObject):
    databaseTransactions.insertIntoNumberDataBase(newId, positionObject)

def openNormalPositions(api, newId, positionObject):
        if (positionObject.isCall == True):
            api.submit_order(symbol=positionObject.ticker, qty=1, side='buy', time_in_force='gtc', type='market',
                             client_order_id=str(newId))
        elif (positionObject.isCall == False):
            api.submit_order(symbol=positionObject.ticker, qty=1, side='sell', time_in_force='gtc', type='market',
                             client_order_id=str(newId))

def openInversePositions(api, newId, positionObject):
    if (positionObject.isCall == False):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='buy', time_in_force='gtc', type='market',
                         client_order_id=str(newId))
    elif (positionObject.isCall == True):
        api.submit_order(symbol=positionObject.ticker, qty=1, side='sell', time_in_force='gtc', type='market',
                         client_order_id=str(newId))

def getPriceOfStock(ticker):
    api = getRestApiInterface()
    return (api.get_barset(ticker, "day", limit=1)[ticker][0].o)

def getRestApiInterface():
    #authentication and connection details
    api_key = 'PK88YTDVNV64L62GF2DO'
    api_secret = '/5v3oTnWpQv89BjTUoCcEG1VAkVUxSZbW/MNFCAF'
    base_url = 'https://paper-api.alpaca.markets'
    #instantiate REST API
    return tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

def getRestApiInterfaceInverse():
    ##Inverse
    api_key = 'PKLW4891U0DACFSEZ41B'
    api_secret = 'Jxw5u8qcQW9J6V9BPXj/YkMIgktG8bcfzLkvgB2h'
    base_url = 'https://paper-api.alpaca.markets'
    #instantiate REST API
    return tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

def getCurrentTickerPrice(api, ticker):
    tickerJson = api.alpha_vantage.current_quote(ticker)
    return tickerJson["05. price"]



