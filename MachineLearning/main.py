from MachineLearning.LinearRegression import *
from call_database import *
from MachineLearning.Scheduler import *


# The main class will allow you to test some of the functionality of our project.
def main():
    pullAllData()
    pullAllStockData("AAPL")
    pullAllStockData("MSFT")
    pullAllStockData("GOOGL")
    train()
    predictTomorrowValue("AAPL")
    predictTomorrowValue("MSFT")
    predictTomorrowValue("GOOGL")


if __name__ == "__main__":
    while True:
        while schedule():
            main()
