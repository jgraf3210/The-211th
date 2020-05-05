import datetime
from datetime import date
import time
import calendar

def schedule():
    currentDate = datetime.datetime.now().date()
    currentDate = str(currentDate)
    currentDate.split(sep='-')
    year = (currentDate[0] + currentDate[1] + currentDate[2] + currentDate[3])
    month = currentDate[5] + currentDate[6]
    day = currentDate[8] + currentDate[9]
    if currentDate[5].startswith('0'):
        month = currentDate[6]
    if currentDate[6].startswith('0'):
        day = currentDate[9]
    currentHour = datetime.datetime.now().hour
    currentMinute = datetime.datetime.now().minute
    currentSecond = datetime.datetime.now().second
    datetime.datetime(int(year), int(month), int(day),
                      currentHour, currentMinute, currentSecond)
    currentDay = datetime.datetime.today().weekday()

    if currentDay == calendar.FRIDAY:
        print('STOCK MARKET CLOSED on [Friday]')
        time.sleep(60)
        return False
    if currentDay == calendar.SATURDAY:
        print('STOCK MARKET CLOSED on [Saturday]')
        time.sleep(60)
        return False
    if currentDay == calendar.SUNDAY:
        print('STOCK MARKET CLOSED on [Sunday]')
        time.sleep(60)
        return False
    if currentHour >= 16 and currentMinute >= 0:
        print('STOCK MARKET CLOSED: ' + str(currentHour) + ':' + str(currentMinute))
        time.sleep(60)
        return False
    print('Time is: ' + str(currentHour) + ':' + str(currentMinute))
    time.sleep(60)
    return True
