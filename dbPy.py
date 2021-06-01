# This is a script of functions that will be imported into bot.py to be used for persistent storage.
import os
import random

dir_path = os.path.dirname(os.path.realpath(__file__))
directory = "databasePY"
path = os.path.join(dir_path, directory)

# For internal use
def nR(list):
    list2 = []
    for el in list:
        el = el.replace("\n", "", 1)
        list2.append(el)
    
    return list2

def initiate():
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))

        directory = "databasePY"

        path = os.path.join(dir_path, directory)
        os.mkdir(path)
    except:
        print("You've already initiated databasePY! Error handled.")

def storeDBValue(dbName, value):
    f = open(f"{os.path.join(path, dbName)}.txt", "w")
    f.write(str(value))
    f.close()

def getDBValue(dbName):
    f = open(f"{os.path.join(path, dbName)}.txt", "r")
    values = f.readlines()
    value = """"""
    for line in values:
        value += f"""{line}"""
    f.close()
    return value

def storeDBList(dbName, value):
    f = open(f"{os.path.join(path, dbName)}.txt", "w")
    f.write("")
    f.close()
    f = open(f"{os.path.join(path, dbName)}.txt", "a")
    for item in value:
        f.write(str(item) + "\n")
    f.close()

def getDBList(dbName):
    f = open(f"{os.path.join(path, dbName)}.txt", "r")
    value = f.readlines()
    f.close()
    return nR(value)

def delDB(dbName):
    os.remove(f"databasePY/{dbName}.txt")