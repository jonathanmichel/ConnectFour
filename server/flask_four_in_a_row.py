#! /usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import os

file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, render_template, jsonify, Response, request
from fourInARow import *

app = Flask(__name__)

game = Game(0)

@app.route('/game/<int:row>', strict_slashes=False)
def gameRow(row):
    game.setToken(row)
    return addHeader(game.emojiText())
   
@app.route('/play/<int:player>/<int:row>', strict_slashes=False)
def playRow(player,row):    
    return addHeader(game.setPlayToken(player,row))
    
@app.route('/getShittyEmojiGame', strict_slashes=False)
def getShittyEmojiGame():
    return addHeader(game.emojiText())

@app.route('/getGame', strict_slashes=False)
def getGame():
    return addHeader(game.text())    
    
@app.route('/resetGame', strict_slashes=False)
def resetGame():
    return addHeader(game.reset())    
    
def addHeader(text):
    resp = Response(text)    
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

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
