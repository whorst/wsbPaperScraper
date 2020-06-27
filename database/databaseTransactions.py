import mysql.connector
import datetime
from objects.closePositionObject import closePosition

# I need to write logic to delete the position out of the DB after I have retrieved it
def createDatabaseConnection():

    cnx = mysql.connector.connect(user='root', password='password',
                                  host='127.0.0.1',
                                  database='tickers')

    return cnx


def closeDatabaseConnection(connection):
    connection.cursor().close()
    connection.close()

def getValidTickersInDatabase(ticker):
    connection = createDatabaseConnection()
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT idticker FROM tickers.tickers_table where idticker = \'{ticker}\';")
    row = cursor.fetchone()
    closeDatabaseConnection(connection)
    return row

def getRecordsWithMatchingExpiryFromDatabase(expiry):
    connection = createDatabaseConnection()
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT idnumberid,isCall,tickerSymbol FROM tickers.numberid where expiryDate = \'{expiry}\*';")
    rows = cursor.fetchall()
    closeDatabaseConnection(connection)
    newRows = []
    for databaseTuple in rows:
        newRows.append(closePosition(databaseTuple[0], databaseTuple[1], databaseTuple[2]))
    return newRows

def getLargestValueFromDatabase():
    connection = createDatabaseConnection()
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT MAX(idNumberID) FROM tickers.numberid;")
    row = cursor.fetchone()
    closeDatabaseConnection(connection)
    return row[0]


def insertIntoNumberDataBase(numberToInsert, positionObject):
    strikeDate = positionObject.strikeDateTime
    isCall = int(positionObject.isCall)
    tickerSymbol = positionObject.ticker

    connection = createDatabaseConnection()
    cursor = connection.cursor(buffered=True)
    now = datetime.datetime.utcnow()
    cursor.execute(f"INSERT INTO tickers.numberid (idnumberId,dateAdded,expiryDate,isCall,tickerSymbol)VALUES(\'{numberToInsert}\',\'{now.strftime('%Y-%m-%d %H:%M:%S')}\',\'{strikeDate.strftime('%Y-%m-%d')}\',{isCall},\'{tickerSymbol}\');")
    connection.commit()
    closeDatabaseConnection(connection)

def insertTickerIntoDatabase(ticker, connection, cursor):
    ticker=ticker.strip()
    if(len(ticker)<7):
        try:
            cursor.execute(f"INSERT INTO tickers.tickers_table (idticker) VALUES(\'{ticker}\')")
            connection.commit()
        except:
            pass