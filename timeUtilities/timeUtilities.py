import datetime

def getCurrentDayEst():
    return  ((datetime.datetime.utcnow()+datetime.timedelta(hours=-4)).strftime('%Y-%m-%d'))

def getCurrentHourEst():
    return  ((datetime.datetime.utcnow()+datetime.timedelta(hours=-4)).strftime('%H'))

