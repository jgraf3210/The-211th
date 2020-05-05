import numpy as np
import pandas as pd
from sklearn import linear_model
import sklearn
import pickle
import random
from call_database import *
from MachineLearning.Confidence import *
import os

dir = os.getcwd()
sep = os.path.sep

# Dynamic path to the MachineLearning directory
# Removes the need for hard-coding the path
machineLearningDir = root + sep + "MachineLearning" + sep

def stockData(stock):
    while True:
        if str(stock).casefold() == 'GOOGL'.casefold():
            pullTodaysStockData('GOOGL')
            data = pd.read_csv(machineLearningDir + "today.csv", sep=',')
            return data
        elif str(stock).casefold() == 'AAPL'.casefold():
            pullTodaysStockData('AAPL')
            data = pd.read_csv(machineLearningDir + "today.csv", sep=',')
            return data
        elif str(stock).casefold() == 'MSFT'.casefold():
            pullTodaysStockData('MSFT')
            data = pd.read_csv(machineLearningDir + "today.csv", sep=',')
            return data
        else:
            print('We Do Not Follow ' + str(stock) + ' At This Time. Please Try Again.')

def train():

    data = pd.read_csv(machineLearningDir + "AllData.csv")

    data = data[["Open", "High", "Low", "Close", "Volume"]]

    x = np.array(data.drop(["Close"], 1))
    y = np.array(data["Close"])

    with open(machineLearningDir + "Best.txt", "r") as r:
        best_in = r.read()
    best = float(best_in)
    i = 0
    for _ in range(5000):  # The greater the range, the greater the accuracy may be
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.6)

        linear = linear_model.LinearRegression()

        linear.fit(x_train, y_train)
        acc = linear.score(x_test, y_test)
        i += 1
        print("Accuracy: " + str(acc) + ": " + str(i))
        if acc >= best:
            best = acc
            print("Best: " + str(best))
            with open(machineLearningDir + "prediction.pickle", "wb") as f:
                pickle.dump(linear, f)
            with open(machineLearningDir + "Best.txt", "w+") as g:
                g.write(str(best))

def test(symbol):
    data, stock = stockData(symbol)

    data = data[["Open", "High", "Low", "Close", "Volume"]]

    x = np.array(data.drop(["Close"], 1))
    y = np.array(data["Close"])
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.4)

    # This section will test the current stock data with the model
    pickle_in = open(machineLearningDir + "prediction.pickle", "rb")
    linear = pickle.load(pickle_in)

    print("-------------------------")
    print('Coefficient: \n', linear.coef_)
    print('Intercept: \n', linear.intercept_)
    print('Accuracy: \n', 100 + linear.intercept_)
    print("-------------------------")

    predicted = linear.predict(x_test)
    for x in range(len(predicted)):
        if predicted[x] < 0:
            predicted[x] = -1 * predicted[x]
        print("Predicted: " + str(predicted[x]), "Actual: " + str(y_test[x]))

def predictTomorrowValue(symbol):
    data = stockData(symbol)
    tomorrow = printNextDate(data.get(['Date']))
    data = data[["Open", "High", "Low", "Close", "Volume"]]

    x = np.array(data.drop(["Close"], 1))
    y = np.array(data["Close"])
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.4)

    # This section will test the current stock data with the model
    pickle_in = open(machineLearningDir + "prediction.pickle", "rb")
    linear = pickle.load(pickle_in)

    predicted = linear.predict(x_test)
    for x in range(len(predicted)):
        if predicted[x] < 0:
            predicted[x] = -1 * predicted[x]

        with open(machineLearningDir + 'predicted_' + str(symbol) + '.csv',
                  mode='a') as predicted_file:
            fieldname = ['Symbol', 'Date', 'Predicted Close']
            predicted_writer = csv.DictWriter(predicted_file, fieldnames=fieldname)
            predicted_writer.writerow({'Symbol': symbol, 'Date': tomorrow, 'Predicted Close': predicted[x]})
            pushPredictions(symbol, tomorrow, predicted[x], callConfidence(symbol))

def tomorrowValues(symbol):
    with open(machineLearningDir + "All" + str(symbol) + "Data.csv", "r",
              newline="") as csvfile1:
        spamreader = csv.reader(csvfile1, delimiter=',')
        values = [row for idx, row in enumerate(spamreader) if idx in (1,0)]

        tempValue = 0
        for _ in range(0, 5):
            j = random.randint(2, 5)
            j = j * 0.01
            i = (-1)**random.randrange(2)
            tempValue = tempValue + float(values[1][6]) + ((float(values[1][6]) * j) * i)

        predictOpen = str(tempValue / 5)
        print("Predicted Open: " + predictOpen)
        print(values[1][6])

        prevHigh = float(values[1][4])
        prevLow = float(values[1][5])
        prevClose = float(values[1][6])

        predictHigh = 0
        predictLow = 0
        print("Low: " + str(prevLow))
        print("High: " + str(prevHigh))
        print("Close: " + str(prevClose))

        if min(prevLow, prevClose) == prevClose:
            print('Low')
            predictLow = prevLow - (abs(prevHigh - prevLow)) / 2
            predictHigh = prevHigh - (abs(prevHigh - prevLow)) / 2
        if (min(prevHigh, prevClose) == prevClose):
            print('High')
            predictLow = prevLow + (abs(prevHigh - prevLow)) / 2
            predictHigh = prevHigh + (abs(prevHigh - prevLow)) / 2

        print("Predicted Low: " + str(predictLow))
        print("Predicted High: " + str(predictHigh))
    csvfile1.close()

    with open(machineLearningDir + "All" + str(symbol) + "DataPredicted.csv", "w",
              newline="") as csvfile2:
        spamwriter = csv.writer(csvfile2, delimiter=';')
        spamwriter.writerow({"Open,High,Low,Close,Volume"})
        spamwriter.writerow({str(predictOpen) + "," + str(predictHigh) + "," + str(predictLow) + ", 0, 0"})
    csvfile2.close()

def printNextDate(Date):
    today = str(Date)
    today = today.split(sep=' ')
    today = today[13]
    today = today.split(sep='-')
    tomorrow = ''
    if today[1].endswith('02'):
        if today[2].endswith('28'):
            tomorrow = today[0] + '-0' + str(int(today[1]) + 1) + '-01'
        else:
            tomorrow = today[0] + '' + today[1] + str(int(today[2]) + 1)
        return tomorrow
    if today[1].endswith('01') or today[1].endswith('03')\
            or today[1].endswith('05') or today[1].endswith('07')\
            or today[1].endswith('08') or today[1].endswith('10')\
            or today[1].endswith('12'):
        if today[2].endswith('31'):
            if today[1].startswith('12'):
                tomorrow = today[0] + '-01-01'
            else:
                if today[1].startswith('0'):
                    tomorrow = today[0] + '-0' + str(int(today[1]) + 1) + '-01'
        else:
            tomorrow = today[0] + '-' + today[1] + '-' + str(int(today[2]) + 1)
        return tomorrow
    else:
        if today[2].startswith('0'):
            today1 = today[2].split('0')
            temp = today1
            if int(temp[1]) == 9:
                tomorrow = today[0] + '-' + today[1] + '-' + str(int(today[2]) + 1)
            else:
                tomorrow = today[0] + '-' + today[1] + '-0' + str(int(today[2]) + 1)
        else:
            if today[2].startswith('30'):
                tomorrow = today[0] + '-0' + str(int(today[1]) + 1) + '-01'
        return tomorrow
