#! /usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import os
import random

file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, render_template, jsonify, Response, request
from fourInARow import *

app = Flask(__name__)

game = Game(0)
gameArray = []

#'/createGame' return playerID and gameID

@app.route('/createGame', strict_slashes=False)
def createGame():
    newGame = Game(random.randint(0,1))
    gameArray.append(newGame)
    
    tmp = newGame.getIdNew()     
    tmp.headers['Access-Control-Allow-Origin'] = '*'
    return tmp
    
    
#'/joinGame/<int:game>' return playerID and gameID or error
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
    
#'/joinGame/<int:game>' return playerID and gameID or error
@app.route('/quitGame/<string:playerID>', strict_slashes=False)
def quitGame(playerID):
    print(len(gameArray))
    for game in gameArray:
        if game.isPlayer(playerID) == True:                     
            game.playerQuit()
            print(game.getNumberQuit())
            if game.getNumberQuit() == 2:
                gameArray.remove(game)
                break
            break
    print(len(gameArray))
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
            tmp = game.getGame() 
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
    
def addHeader(text):
    resp = Response(text)    
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    
def gameTimeCheck():
    while(1):
        print(len(gameArray))
        for game in gameArray:
            if time.time()-game.getTime() == 60*1:      
                gameArray.remove(game)
                break
        print(len(gameArray))
        time.sleep(5)

from logging import FileHandler, Formatter, DEBUG

if __name__ == '__main__':
    try:
        thread.start_new_thread(gameTimeCheck,())
        file_handler = FileHandler("flask.log")
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)

        app.run(host='::', port = 5002, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("end of game rest server")
