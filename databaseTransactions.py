import mysql.connector


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

def insertTickerIntoDatabase(ticker, connection, cursor):
    # add_ticker = ("INSERT INTO tickers.tickers_table(idticker) VALUES (%s)")
    # data_ticker = ("MU")

    ticker=ticker.strip()
    if(len(ticker)<7):
        try:
            cursor.execute(f"INSERT INTO tickers.tickers_table (idticker) VALUES(\'{ticker}\')")
            connection.commit()
        except:
            pass

# connection = createDatabaseConnection()
# cursor = connection.cursor()
#
# tickerFile = open("resources/files/tickerFile", "r")
# for line in tickerFile:
#     ticker = str(line.strip())
#     insertTickerIntoDatabase(ticker, connection, cursor)
# tickerFile.close()
# closeDatabaseConnection(connection)

