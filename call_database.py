# Script to retrieve data from our Azure Database

import os
import csv
from flask import Flask
from flaskr import cnxn
# OS file separator
sep = os.path.sep
# Root directory
root = os.getcwd()

# Dynamic path to the MachineLearning directory
# Removes the need for hard-coding the path
machineLearningDir = root + sep + "MachineLearning" + sep

cursor = cnxn.cursor()

app = Flask(__name__)


# *************GET ALL DATA***************************************
def pullAllData():
    all = "SELECT * FROM StockAdviseDB.dbo.MAIN;"
    cursor.execute(all)
    fetch = cursor.fetchall()
    cursor.commit()
# #This iterates through all the rows of data and prints on console
    with open(machineLearningDir + "AllData.csv", "w", newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow({'Index,Stock,Date,Open,High,Low,Close,Volume'})
        for i in fetch:
            spamwriter.writerow(i)
    csvfile.close()
        #To get specific values from columns, index the lists
        #For example, to get just the dates, print(i[2])

# ****************GET DATA FOR A SINGLE STOCK**********************
def pullTodaysStockData(symbol):
    # Type in the symbol for what data you want
    # symbol = 'MSFT'
    # This calls the data for whatever symbol you have set to that variable above
    query = "SELECT * FROM StockAdviseDB.dbo.MAIN WHERE SYMBOL = '%s';" % symbol
    # all = "SELECT * FROM StockAdviseDB.dbo.MAIN WHERE SYMBOL = 'MSFT' order by DATE desc"

    cursor.execute(query)
    fetch = cursor.fetchall()
    cursor.commit()

    with open(machineLearningDir +"testme.csv", "w", newline="") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter= ';')
        for i in fetch:
            spamwriter.writerow(i)
        csvfile.close()

    with open(machineLearningDir + "testme.csv", "r", newline="") as csvfile1:
        with open(machineLearningDir + "today.csv", "w",
                  newline="") as csvfile2:
            spamreader = csv.reader(csvfile1, delimiter=';')
            row1 = next(spamreader)
            stringRow1 = str(row1)
            newString = stringRow1.replace("\'", "")
            newString = newString.replace("[", "")
            newString = newString.replace("]", "")
            spamwriter = csv.writer(csvfile2, delimiter=';')
            spamwriter.writerow({"Index,Stock,Date,Open,High,Low,Close,Volume"})
            spamwriter.writerow({newString})

def pullAllStockData(symbol):
    # Type in the symbol for what data you want
    # symbol = 'MSFT'
    # This calls the data for whatever symbol you have set to that variable above
    query = "SELECT * FROM StockAdviseDB.dbo.MAIN WHERE SYMBOL = '%s';" % symbol

    cursor.execute(query)
    fetch = cursor.fetchall()
    cursor.commit()

    with open(machineLearningDir + "testme.csv", "w", newline="") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter= ';')

        for i in fetch:
            spamwriter.writerow(i)
        csvfile.close()

    with open(machineLearningDir + "testme.csv", "r", newline="") as csvfile1:
        with open(machineLearningDir + "All" + str(symbol) + "Data.csv", "w",
                  newline="") as csvfile2:
            spamreader = csv.reader(csvfile1, delimiter=';')
            spamwriter = csv.writer(csvfile2, delimiter=';')
            spamwriter.writerow({"Index,Stock,Date,Open,High,Low,Close,Volume"})

            for _ in spamreader:
                row = ','.join(_)
                stringRow1 = str(row)
                newString = stringRow1.replace("\'", "")
                newString = newString.replace("[", "")
                newString = newString.replace("]", "")
                spamwriter.writerow({newString})