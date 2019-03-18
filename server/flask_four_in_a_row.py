#! /usr/bin/env python
#-*- coding: utf-8 -*-
from datetime import datetime
import sys
import time
import os
import random
import pickle
import GraphManager

file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, jsonify, Response, request, send_file, redirect
from fourInARow import *
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)



gamePickleFileName = "gamePickleFile"
gameStatisticsPickleFileName = "gameStatisticsPickleFileName"

whiteLargeSquare = "em-white_large_square"
poop = "em-poop"

class GameStatistics():
    def __init__(self):
        self.gameSinceStartup = 0
        self.gameToday = 0

        self.gameKilled = 0
        self.gameKilledToday = 0

        self.gameKilledWithoutJoin = 0
        self.gameKilledWithoutJoinToday = 0

        self.meanPlayedGame = 0
        self.meanPlayedGameToday = 0
        self.severOnline = datetime.today()
        self.severStart = datetime.today()

timeCheck = 60*5
timeSleep = 4

game = Game(0)
gameStatistics = GameStatistics()
gameArray = []

if os.path.isfile(gamePickleFileName) == True:
    try:
        gameArray = pickle.load(open(gamePickleFileName, 'rb'))
        if isinstance(gameArray, list):
            if len(gameArray)>0:
                if not isinstance(gameArray[0], Game):
                    print("gamePickleFileName File doesn't contain a list of Game")
                    gameArray = []
                else:
                    print("gamePickleFileName File successfully loaded")
            else:
                print("gamePickleFileName File successfully loaded")
        else:
            print("gamePickleFileName File doesn't contain a list")
            gameArray = []
    except:
        print("gamePickleFileName File couldn't be loaded")
else:
	print("gamePickleFileName File doesn't exist")

if os.path.isfile(gameStatisticsPickleFileName) == True:
    try:
        gameStatistics = pickle.load(open(gameStatisticsPickleFileName, 'rb'))
        if not isinstance(gameStatistics, GameStatistics):
            print("gameStatisticsPickleFileName File doesn't contain GameStatistics")
            gameStatistics = GameStatistics()
        else:
            print("gameStatisticsPickleFileName File successfully loaded")
    except:
        print("gameStatisticsPickleFileName File couldn't be loaded")
else:
    print("gameStatisticsPickleFileName File doesn't exist")


gameStatistics.severStart = datetime.today()



@app.route('/', strict_slashes=False)
def homeRedirect():
    return redirect("http://github.com/jonathanmichel/connectFour", code=302)

@app.route('/createGame', strict_slashes=False)
def createGame():
    newGame = Game(random.randint(0,1))
    gameArray.append(newGame)
    pickle.dump(gameArray, open(gamePickleFileName, 'wb'))
    gameStatistics.gameSinceStartup = gameStatistics.gameSinceStartup +1
    gameStatistics.gameToday = gameStatistics.gameToday + 1
    pickle.dump(gameStatistics, open(gameStatisticsPickleFileName, 'wb'))

    tmp = newGame.getIdNew()
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp


@app.route('/joinGame/<string:gameID>', strict_slashes=False)
def joinGame(gameID):
    for game in gameArray:
        if game.getGameId() == gameID:
            tmp = game.getIdJoin()
            tmp.headers['Access-Control-Allow-Origin'] = '*'
            return tmp

    listDic = {}
    listDic['gameID'] = 0
    listDic['playerID'] = 0

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/quitGame/<string:playerID>', strict_slashes=False)
def quitGame(playerID):
    for game in gameArray:
        if game.isPlayer(playerID) == True:
            game.playerQuit()
            print(game.getNumberQuit())
            if game.getNumberQuit() == 2:
                gameArray.remove(game)
                break
            break
    pickle.dump(gameArray, open(gamePickleFileName, 'wb'))
    return "0"

@app.route('/game/<int:row>', strict_slashes=False)
def gameRow(row):
    game.setToken(row)
    return addHeader(game.emojiText())

@app.route('/play/<string:playerID>/<int:row>', strict_slashes=False)
def playRow(playerID,row):
    for game in gameArray:
        if game.isPlayer(playerID) == True:
            tmp = game.setPlayToken(playerID,row)
            tmp.headers['Access-Control-Allow-Origin'] = '*'
            return tmp
    listDic = {}
    listDic['ERROR'] = "Player has no Game Assigned"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp


@app.route('/getShittyEmojiGame', strict_slashes=False)
def getShittyEmojiGame():
    return addHeader(game.emojiText())

@app.route('/getGame/<string:playerID>', strict_slashes=False)
def getGame(playerID):
    for game in gameArray:
        if game.isPlayer(playerID) == True:
            tmp = game.getGame(playerID)
            tmp.headers['Access-Control-Allow-Origin'] = '*'
            return tmp
    listDic = {}
    listDic['ERROR'] = "Player has no Game Assigned"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/resetGame/<string:playerID>', strict_slashes=False)
def resetGame(playerID):
    for game in gameArray:
        if game.isPlayer(playerID) == True:
            return addHeader(game.reset())
    listDic = {}
    listDic['ERROR'] = "Player has no Game Assigned"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/setEmoji/<string:playerID>/<string:emojiCssRef>', strict_slashes=False)
def setEmoji(playerID, emojiCssRef):
    for game in gameArray:
        if game.isPlayer(playerID) == True:
            game.setPlayerEmoji(playerID, emojiCssRef)
            listDic = {}
            listDic['SUCCESS'] = "EMOJI SET"

            tmp = jsonify(listDic)
            tmp.headers['Access-Control-Allow-Origin'] = '*'
            return tmp

    listDic = {}
    listDic['ERROR'] = "Player has no Game Assigned"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/copyEmoji/<string:playerID>', strict_slashes=False)
def copyEmoji(playerID):
    for game in gameArray:
        if game.isPlayer(playerID) == True:
            if game.isPlayer0(playerID) == True:
                game.setPlayerEmoji(playerID, game.getPlayer1Emoji())
            else:
                game.setPlayerEmoji(playerID, game.getPlayer0Emoji())
            listDic = {}
            listDic['SUCCESS'] = "EMOJI SET"

            tmp = jsonify(listDic)
            tmp.headers['Access-Control-Allow-Origin'] = '*'
            return tmp

    listDic = {}
    listDic['ERROR'] = "Player has no Game Assigned"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/setBlankEmoji/<string:playerID>', strict_slashes=False)
def setBlankEmoji(playerID):
    for game in gameArray:
        if game.isPlayer(playerID) == True:
            game.setPlayerEmoji(playerID, whiteLargeSquare)
            listDic = {}
            listDic['SUCCESS'] = "EMOJI SET"

            tmp = jsonify(listDic)
            tmp.headers['Access-Control-Allow-Origin'] = '*'
            return tmp

    listDic = {}
    listDic['ERROR'] = "Player has no Game Assigned"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/setPoopEmoji/<string:playerID>', strict_slashes=False)
def setPoopEmoji(playerID):
    for game in gameArray:
        if game.isPlayer(playerID) == True:
            game.setPlayerEmoji(playerID, poop)
            listDic = {}
            listDic['SUCCESS'] = "EMOJI SET"

            tmp = jsonify(listDic)
            tmp.headers['Access-Control-Allow-Origin'] = '*'
            return tmp

    listDic = {}
    listDic['ERROR'] = "Player has no Game Assigned"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/messUp/<string:playerID>', strict_slashes=False)
def messUp(playerID):
    for game in gameArray:
        if game.isPlayer(playerID) == True:
            game.randomGrid()
            listDic = {}
            listDic['SUCCESS'] = "Messed up mah man"

            tmp = jsonify(listDic)
            tmp.headers['Access-Control-Allow-Origin'] = '*'
            return tmp

    listDic = {}
    listDic['ERROR'] = "Player has no Game Assigned"

    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/getDataFromGames', strict_slashes=False)
def getDataFromGames():
    tmp = jsonify(processDataFromGames())
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/getDataFromGamesCounterReset', strict_slashes=False)
def getDataFromGamesCounterReset():
    tmp = jsonify(processDataFromGames())
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    gameStatistics.gameToday = 0
    gameStatistics.gameKilledToday = 0
    gameStatistics.gameKilledWithoutJoinToday = 0
    gameStatistics.meanPlayedGameToday = 0
    pickle.dump(gameStatistics, open(gameStatisticsPickleFileName, 'wb'))
    return tmp

@app.route('/getGraph/gameSessionPlayed', strict_slashes=False)
def getGraphGameSessionPlayed():
    GraphManager.gameSessionPlayed(processDataFromGames())
    return send_file('gameSessionPlayed.png', mimetype='image/png')

@app.route('/getGraph/graphStatistic/<int:size>', strict_slashes=False)
def getGraphGraphStatistic(size):
    GraphManager.graphStatistic(processDataFromGames(),size)
    return send_file('graphStatistic.png', mimetype='image/png')

@app.route('/getGraph/graphStatisticRaw/<int:size>', strict_slashes=False)
def graphStatisticRaw(size):
    Json = GraphManager.graphStatisticRaw(processDataFromGames(),size)
    tmp = jsonify(Json)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/getGraph/gameSessionPlayedSVG', strict_slashes=False)
def getGraphGameSessionPlayedSVGsize():
    GraphManager.gameSessionPlayed(processDataFromGames())
    return send_file('gameSessionPlayed.svg', mimetype='image/svg+xml')

@app.route('/getGraph/graphStatisticSVG/<int:size>', strict_slashes=False)
def getGraphGraphStatisticSVG(size):
    GraphManager.graphStatistic(processDataFromGames(),size)
    return send_file('graphStatistic.svg', mimetype='image/svg+xml')

@app.route('/chat',methods=['POST'], strict_slashes=False)
def chat():
    if request.method=='POST':
        content = request.get_json()
        text = content['text']
        playerID = content['playerID']
        for game in gameArray:
            if game.isPlayer(playerID) == True:
                game.addMessage(text, playerID)
                listDic = {}
                listDic['Success'] = "message sent"
                tmp = jsonify(listDic)
                tmp.headers['Access-Control-Allow-Origin'] = '*'
                tmp.headers['Content-Type'] = 'application/json'
                return tmp

        listDic = {}
        listDic['ERROR'] = "Player has no Game Assigned"
        tmp = jsonify(listDic)
        tmp.headers['Access-Control-Allow-Origin'] = '*'
        return tmp

    listDic = {}
    listDic[request.method + ' request'] = request.method + ' request handeled'
    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/chatAdmin',methods=['POST'], strict_slashes=False)
def chatAdmin():
    if request.method=='POST':
        content = request.get_json()
        text = content['text']
        gameID = content['gameID']
        for game in gameArray:
            if game.getGameId() == gameID:
                game.addMessage(text, "Admin")
                listDic = {}
                listDic['Success'] = "message sent"
                tmp = jsonify(listDic)
                tmp.headers['Access-Control-Allow-Origin'] = '*'
                return tmp

        listDic = {}
        listDic['ERROR'] = "GameID has no Game Assigned"
        tmp = jsonify(listDic)
        tmp.headers['Access-Control-Allow-Origin'] = '*'
        return tmp

    listDic = {}
    listDic[request.method + ' request'] = request.method + ' request handeled'
    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.route('/chatTest',methods=['GET', 'POST'], strict_slashes=False)
def chatTest():
    for game in gameArray:
        game.addMessageRandom()
    listDic = {}
    listDic['SUCCESS'] = "message sent"
    tmp = jsonify(listDic)
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp

@app.before_request
def beforeRequest():
    gameTimeCheck()

def processDataFromGames():
    onlineGame = len(gameArray)
    onlinePlayer = 0
    offlinePlayer = 0
    gameIdList = {}
    for game in gameArray:
        gameStatus={}
        players = []
        players.append(game.getPlayerID(0))
        players.append(game.getPlayerID(1))
        gameStatus["player0Status"] = game.getPlayer0Status()
        gameStatus["player1Status"] = game.getPlayer1Status()
        gameStatus["playersID"] = players
        gameStatus['isWin'] = game.isWin()
        gameStatus['numberOfGame'] = game.getNumberOfGame()
        gameIdList[game.getGameId()] = gameStatus
        if game.getPlayer0Status() == True:
            onlinePlayer = onlinePlayer + 1
        if game.getPlayer1Status() == True:
            onlinePlayer = onlinePlayer + 1

        gameStatus['messages'] = []
        for message in game.getChat():
            messageDic = {}
            messageDic['playerID']=message.playerID
            messageDic['text']=message.text
            messageDic['timestamp']=message.timestamp
            gameStatus['messages'].append(messageDic)
        gameStatus['player0Emoji']=game.getPlayer0Emoji()
        gameStatus['player1Emoji']=game.getPlayer1Emoji()

    offlinePlayer = (onlineGame*2) - onlinePlayer
    listDic = {}
    listDic['severStart'] = str(gameStatistics.severStart)
    listDic['severOnline'] = str(gameStatistics.severOnline)
    listDic['onlineGame'] = onlineGame
    listDic['onlinePlayer'] = onlinePlayer
    listDic['offlinePlayer'] = offlinePlayer
    listDic['gameIdList'] = gameIdList
    listDic['gameSinceStartup'] = gameStatistics.gameSinceStartup
    listDic['gameToday'] = gameStatistics.gameToday
    listDic['gameKilledToday'] = gameStatistics.gameKilledToday
    listDic['gameKilledWithoutJoinToday'] = gameStatistics.gameKilledWithoutJoinToday
    listDic['gameKilled'] = gameStatistics.gameKilled
    listDic['gameKilledWithoutJoin'] = gameStatistics.gameKilledWithoutJoin
    listDic['meanPlayedGame'] = gameStatistics.meanPlayedGame
    listDic['meanPlayedGameToday'] = gameStatistics.meanPlayedGameToday
    pickle.dump(gameStatistics, open(gameStatisticsPickleFileName, 'wb'))
    return listDic

def addHeader(text):
    resp = Response(text)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def gameTimeCheck():
    toRemove = []
    global gameArray
    for game in gameArray:
        if time.time()-game.getTimeP0() > timeCheck:
            game.setPlayer0Quit(True)
        else:
            game.setPlayer0Quit(False)

        if time.time()-game.getTimeP1() > timeCheck:
            game.setPlayer1Quit(True)
        else:
            game.setPlayer1Quit(False)

        if game.getPlayersQuit() == True:
            nGamePlayed = game.getNumberOfGame()
            gameStatistics.gameKilled = gameStatistics.gameKilled +1
            gameStatistics.gameKilledToday = gameStatistics.gameKilledToday + 1
            if game.getPlayerID(1) == "":
                gameStatistics.gameKilledWithoutJoin = gameStatistics.gameKilledWithoutJoin + 1
                gameStatistics.gameKilledWithoutJoinToday = gameStatistics.gameKilledWithoutJoinToday +1
                nGamePlayed = 0

            gameStatistics.meanPlayedGame = (gameStatistics.meanPlayedGame * (gameStatistics.gameKilled -1) + nGamePlayed)/gameStatistics.gameKilled
            gameStatistics.meanPlayedGameToday = (gameStatistics.meanPlayedGameToday * (gameStatistics.gameKilledToday -1) + nGamePlayed)/gameStatistics.gameKilledToday
            pickle.dump(gameStatistics, open(gameStatisticsPickleFileName, 'wb'))
            toRemove.append(game)

    gameArray = [x for x in gameArray if x not in toRemove]
    pickle.dump(gameArray, open(gamePickleFileName, 'wb'))


from logging import FileHandler, Formatter, DEBUG

if __name__ == '__main__':
    try:
        file_handler = FileHandler("flask.log")
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)

        app.run(host='::', port = 5002, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("end of game rest server")
