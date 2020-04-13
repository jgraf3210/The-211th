# Script to retrieve data from our Azure Database

import os
import sys
import json
import pyodbc
import csv

dir = os.getcwd()
sep = os.path.sep

# Dynamic path to the MachineLearning directory
# Removes the need for hard-coding the path
machineLearningDir = dir + sep + "MachineLearning" + sep

# Environment variables for the database information
server = os.getenv('DBURL')
database = os.getenv('DBNAME')
username = os.getenv('DBUSER')
password = os.getenv('DBPASS')

# SQL Database Connection
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' +
                      'SERVER=' + server +
                      ';DATABASE=' + database +
                      ';UID=' + username +
                      ';PWD=' + password)
cursor = cnxn.cursor()


# *************GET ALL DATA***************************************
def pullAllData():
    all = "SELECT * FROM StockAdviseDB.dbo.MAIN;"
    cursor.execute(all)
    fetch = cursor.fetchall()
    cursor.commit()
# #This iterates through all the rows of data and prints on console
    for i in fetch:
        # To get specific values from columns, index the lists
        # For example, to get just the dates, print(i[2])
        print(i)


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
            row1 = next(spamreader)
            for _ in spamreader:
                stringRow1 = str(row1)
                newString = stringRow1.replace("\'", "")
                newString = newString.replace("[", "")
                newString = newString.replace("]", "")
                spamwriter.writerow({newString})


# Check if the email is already in the database
# Used in auth.py for verification
def check_email(email):
    query = "SELECT EMAIL FROM StockAdviseDB.dbo.Users WHERE EMAIL=" + email
    cursor.execute(query)
    cursor.fetchall()
    if(cursor.rowcount > 0):
        return False
    else:
        return True


# Check if the email is already in the database
# Used in auth.py for verification
def check_username(username):
    query =  "SELECT USERNAME FROM StockAdviseDB.dbo.Users WHERE USERNAME=" + username
    cursor.execute(query)
    cursor.fetchall()
    if(cursor.rowcount > 0):
        return False
    else:
        return True
