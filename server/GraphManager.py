from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import json
import datetime

import numpy as np

mypath = '/home/lucblender/ConnectFour/server/ConnectFourStats/'
storePath = '/home/lucblender/ConnectFour/server/'


def graphStatistic(dict=None, dataSize=0):
    if dict != None:
        with open(mypath+datetime.datetime.today().strftime('%d-%m-%Y')+'.json','w+') as file:
            file.write(str(json.dumps(dict, indent=4, sort_keys=True, ensure_ascii=False)))

    jsonFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    datesFile=[]

    for jsonFile in jsonFiles:
        datesFile.append(jsonFile.replace('.json',''))


    dates = [datetime.datetime.strptime(ts, "%d-%m-%Y") for ts in datesFile]
    dates.sort()
    sorteddates = [datetime.datetime.strftime(ts, "%d-%m-%Y") for ts in dates]

    sortedJsonFiles = []
    for date in sorteddates:
        sortedJsonFiles.append(date+'.json')

    gameKilledToday = []
    gameKilledWithoutJoinToday = []
    gameToday = []
    meanPlayedGameToday = []

    for jsonFile in sortedJsonFiles:
        with open(mypath+jsonFile, "rb") as myFile:
            jsonData = myFile.read()

        parsed = json.loads(jsonData)
        gameKilledToday.append(parsed.get('gameKilledToday'))
        gameKilledWithoutJoinToday.append(parsed.get('gameKilledWithoutJoinToday'))
        gameToday.append(parsed.get('gameToday'))
        meanPlayedGameToday.append(parsed.get('meanPlayedGameToday'))

    sorteddates = sorteddates[-dataSize:]
    gameKilledToday = gameKilledToday[-dataSize:]
    gameKilledWithoutJoinToday = gameKilledWithoutJoinToday[-dataSize:]
    gameToday = gameToday[-dataSize:]
    meanPlayedGameToday = meanPlayedGameToday[-dataSize:]

    fig, ax = plt.subplots()
    ax.plot(sorteddates, gameKilledToday, label = 'gameKilledToday', alpha=0.7, marker='1')
    ax.plot(sorteddates, gameKilledWithoutJoinToday, label = 'gameKilledWithoutJoinToday', alpha=0.7, marker='2')
    ax.plot(sorteddates, gameToday, label = 'gameToday', alpha=0.7, marker='3')
    ax.plot(sorteddates, meanPlayedGameToday, label = 'meanPlayedGameToday', alpha=0.7, marker='4')

    ax.set(xlabel='Date', ylabel='Number of games',
           title='ConnectFour statistics: ' + datetime.datetime.today().strftime('%d.%m.%Y'))

    ax.legend()

    major_ticks = []

    plt.xticks(rotation=90)
    every_nth = round(len(ax.xaxis.get_ticklabels())/15)

    if every_nth<=0:
        every_nth=1

    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth == 0:
            major_ticks.append(n)
    plt.tight_layout()


    ax.set_xticks(major_ticks)
    ax.grid()


    fig.savefig(storePath+"graphStatistic.png")
    fig.savefig(storePath+"graphStatistic.svg")

def graphStatisticRaw(dict=None, dataSize=0):
    if dict != None:
        with open(mypath+datetime.datetime.today().strftime('%d-%m-%Y')+'.json','w+') as file:
            file.write(str(json.dumps(dict, indent=4, sort_keys=True, ensure_ascii=False)))

    jsonFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    datesFile=[]

    for jsonFile in jsonFiles:
        datesFile.append(jsonFile.replace('.json',''))


    dates = [datetime.datetime.strptime(ts, "%d-%m-%Y") for ts in datesFile]
    dates.sort()
    sorteddates = [datetime.datetime.strftime(ts, "%d-%m-%Y") for ts in dates]

    sortedJsonFiles = []
    for date in sorteddates:
        sortedJsonFiles.append(date+'.json')

    gameKilledToday = []
    gameKilledWithoutJoinToday = []
    gameToday = []
    meanPlayedGameToday = []

    for jsonFile in sortedJsonFiles:
        with open(mypath+jsonFile, "rb") as myFile:
            jsonData = myFile.read()

        parsed = json.loads(jsonData)
        gameKilledToday.append(parsed.get('gameKilledToday'))
        gameKilledWithoutJoinToday.append(parsed.get('gameKilledWithoutJoinToday'))
        gameToday.append(parsed.get('gameToday'))
        meanPlayedGameToday.append(parsed.get('meanPlayedGameToday'))

    output={}
    output['dates'] = sorteddates[-dataSize:]
    output['gameKilledToday'] = gameKilledToday[-dataSize:]
    output['gameKilledWithoutJoinToday'] = gameKilledWithoutJoinToday[-dataSize:]
    output['gameToday'] = gameToday[-dataSize:]
    output['meanPlayedGameToday'] = meanPlayedGameToday[-dataSize:]

    return output

def gameSessionPlayed(dict):
    dataName = []
    dataMean = []
    dataName.append('meanPlayedGame')
    dataMean.append(dict.get("meanPlayedGame"))
    dataName.append('meanPlayedGameToday')
    dataMean.append(dict.get("meanPlayedGameToday"))

    gameList = dict.get('gameIdList')
    if len(gameList) != 0:
        gameListKeys = gameList.keys()
        for key in gameListKeys:
            dataName.append(key)
            dataMean.append(gameList.get(key).get("numberOfGame"))


    fig, ax = plt.subplots()

    y_pos = np.arange(len(dataName))
    ax.barh(y_pos, dataMean, align='center', color='blue')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(dataName)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of game Session')
    ax.set_title('Number of game Session of online game and mean')
    for i, v in enumerate(dataMean):
        ax.text(v+0.05 , i , str(v), color='black')

    plt.tight_layout()
    fig.savefig(storePath+"gameSessionPlayed.png")
    fig.savefig(storePath+"/gameSessionPlayed.svg")

