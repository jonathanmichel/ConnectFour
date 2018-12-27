from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import json
import datetime

import numpy as np

mypath = '/home/lucblender/ConnectFour/server/ConnectFourStats/'


def graphStatistic(dict=None):
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

    fig, ax = plt.subplots()
    ax.plot(sorteddates, gameKilledToday, label = 'gameKilledToday')
    ax.plot(sorteddates, gameKilledWithoutJoinToday, label = 'gameKilledWithoutJoinToday')
    ax.plot(sorteddates, gameToday, label = 'gameToday')
    ax.plot(sorteddates, meanPlayedGameToday, label = 'meanPlayedGameToday')

    ax.set(xlabel='Date', ylabel='Number of games',
           title='ConnectFour statistics: ' + datetime.datetime.today().strftime('%d.%m.%Y'))
    ax.grid()

    ax.legend()

    fig.savefig("/home/lucblender/ConnectFour/server/graphStatistic.png")

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
    fig.savefig("/home/lucblender/ConnectFour/server/gameSessionPlayed.png")

