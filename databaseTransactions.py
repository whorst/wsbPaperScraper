import mysql.connector
import datetime


def createDatabaseConnection():

    cnx = mysql.connector.connect(user='root', password='password',
                                  host='127.0.0.1',
                                  database='tickers')

    return cnx


def closeDatabaseConnection(connection):
    connection.cursor().close()
    connection.close()

def isTickerInDatabase(ticker):
    connection = createDatabaseConnection()
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT idticker FROM tickers.tickers_table where idticker = \'{ticker}\';")
    row = cursor.fetchone()
    closeDatabaseConnection(connection)
    return bool(row)

def getLargestValueFromDatabase():
    connection = createDatabaseConnection()
    cursor = connection.cursor(buffered=True)
    cursor.execute(f"SELECT MAX(idNumberID) FROM tickers.numberid;")
    row = cursor.fetchone()
    closeDatabaseConnection(connection)
    return row[0]

def insertIntoNumberDataBase(numberToInsert):
    connection = createDatabaseConnection()
    cursor = connection.cursor(buffered=True)

    now = datetime.datetime.utcnow()
    cursor.execute(f"INSERT INTO tickers.numberid (idnumberId,dateAdded)VALUES(\'{numberToInsert}\',\'{now.strftime('%Y-%m-%d %H:%M:%S')}\');")
    connection.commit()
    closeDatabaseConnection(connection)

def insertIntoNumberDataBaseInverse(numberToInsert):
    connection = createDatabaseConnection()
    cursor = connection.cursor(buffered=True)

    now = datetime.datetime.utcnow()
    cursor.execute(f"INSERT INTO tickers.numberidinverse (idnumberId,dateAdded)VALUES(\'{numberToInsert}\',\'{now.strftime('%Y-%m-%d %H:%M:%S')}\');")
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


