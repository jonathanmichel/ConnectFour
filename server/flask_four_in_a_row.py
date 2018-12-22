#! /usr/bin/env python
#-*- coding: utf-8 -*-
from datetime import datetime
from threading import Timer
import sys
import time
import os
import random
import pickle
import json
import SendMail

file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, render_template, jsonify, Response, request
from fourInARow import *

app = Flask(__name__)

gamePickleFileName = "gamePickleFile"

gameSinceStartup = 0
gameToday = 0

timeCheck = 60*5
timeSleep = 4

game = Game(0)
gameArray = []
severStart = datetime.today()

if os.path.isfile(gamePickleFileName) == True:
	try:
		gameArray = pickle.load(open(gamePickleFileName, 'rb'))
		if isinstance(gameArray, list):
			if len(gameArray)>0:
				if not isinstance(gameArray[0], Game):
					print("Picke File doesn't contain a list of Game")
					gameArray = []
				else:					
					print("Picke File successfully loaded")
			else:					
				print("Picke File successfully loaded")
		else:
			print("Picke File doesn't contain a list")
			gameArray = []
	except:
		print("Pickle File couldn't be loaded")
else:
	print("Pickle File doesn't exist")
   

@app.route('/createGame', strict_slashes=False)
def createGame():
    newGame = Game(random.randint(0,1))
    gameArray.append(newGame)
    pickle.dump(gameArray, open(gamePickleFileName, 'wb'))
    global gameSinceStartup
    global gameToday
    gameSinceStartup = gameSinceStartup +1
    gameToday = gameToday + 1 
    
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
    
@app.route('/getDataFromGames', strict_slashes=False)
def getDataFromGames():  
    tmp = jsonify(processDataFromGames())    
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
def processDataFromGames():
    global gameSinceStartup
    global gameToday
    
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
        gameIdList[game.getGameId()] = gameStatus
        if game.getPlayer0Status() == True:
            onlinePlayer = onlinePlayer + 1
        if game.getPlayer1Status() == True:
            onlinePlayer = onlinePlayer + 1
    offlinePlayer = (onlineGame*2) - onlinePlayer
    listDic = {}     
    listDic['severStart'] = str(severStart)
    listDic['onlineGame'] = onlineGame
    listDic['onlinePlayer'] = onlinePlayer
    listDic['offlinePlayer'] = offlinePlayer
    listDic['gameIdList'] = gameIdList
    listDic['gameSinceStartup'] = gameSinceStartup
    listDic['gameToday'] = gameToday
    return listDic
    
def addHeader(text):
    resp = Response(text)    
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    
def gameTimeCheck():     
    while(1):
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
                gameArray.remove(game)
                break
        pickle.dump(gameArray, open(gamePickleFileName, 'wb'))
        time.sleep(timeSleep)
        
        

    
def everyDayTask():
    SendMail.sendMail("ConnectFour EveryDayStats from: "+ severStart.strftime('%d.%m.%Y'),json.dumps(processDataFromGames(), indent=4, sort_keys=True, ensure_ascii=False))
    global gameToday
    x=datetime.today()
    y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
    #y=x.replace(minute=x.minute+2)
    delta_t=y-x
    secs=delta_t.total_seconds()+1
    t = Timer(secs, everyDayTask)
    t.start()    
    gameToday = 0
    print("everyDayTask")
        
        
        
from logging import FileHandler, Formatter, DEBUG

if __name__ == '__main__':
    try:
        everyDayTask()
        thread.start_new_thread(gameTimeCheck,())
        file_handler = FileHandler("flask.log")
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)

        app.run(host='::', port = 5002, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("end of game rest server")
