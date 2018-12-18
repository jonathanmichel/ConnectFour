from enum import Enum
import emoji
from flask import jsonify
import random
import string
import _thread as thread
import time

class Token(Enum):
    EMPTY = 0
    PLAYER0 = 1
    PLAYER1 = 2
    
width, height = 6, 7

class Game():

    def __init__(self, player):
        self.__gameID = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
        self.__player0ID = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
        self.__player1ID = ""
        self.__player0Quit = False
        self.__player1Quit = False
        self.__player = player
        self.__numberQuit = 0
        self.__grid = [[Token.EMPTY for x in range(width)] for y in range(height)] 
        self.__timeP0 = time.time()
        self.__timeP1 = time.time()
        
    def reset(self):
        self.__grid = [[Token.EMPTY for x in range(width)] for y in range(height)] 
        self.__player = random.randint(0,1)
        
    def playerQuit(self):
        self.__numberQuit = self.__numberQuit + 1
    
    def getNumberQuit(self):
        return self.__numberQuit
        
    def getGrid(self):
        return self.__grid
    
    def setToken(self, line):
        if self.__player == 0:
            token = Token.PLAYER0
        else:
            token = Token.PLAYER1
        
        if line > width or line < 0:
            return False
        else:
            for w in range(0,height-1):
                if self.__grid[line][w] == Token.EMPTY:
                    self.__grid[line][w] = token
                    if self.__player == 0:
                        self.__player = 1
                    else:
                        self.__player = 0
                    return True
            return False
           

    def setPlayToken(self, player, line):  
        listDic = {}    
        print(player)
        print(self.__player0ID)
        if self.__player == 0 and player != self.__player0ID:
            listDic["ERROR"] = "NOT YOUR TURN"
            return jsonify(listDic)
        if self.__player == 1 and player != self.__player1ID:
            listDic["ERROR"] = "NOT YOUR TURN"
            return jsonify(listDic)
        
        if self.__player == 0:
            token = Token.PLAYER0
        else:
            token = Token.PLAYER1
        
        if line > width or line < 0:
            listDic["ERROR"] = "TOKEN OUT OF GRID"
            return jsonify(listDic)
        else:
            for w in range(0,height-1):
                if self.__grid[line][w] == Token.EMPTY:
                    self.__grid[line][w] = token
                    if self.__player == 0:
                        self.__player = 1
                    else:
                        self.__player = 0
                   
                    listDic['grid'] = self.text()
                    listDic['player'] = str(self.__player)
                    listDic['isWin'] = str(self.isWin())
                    listDic['player0Status'] = str(not self.__player0Quit)
                    listDic['player1Status'] = str(not self.__player1Quit)
                    return jsonify(listDic)
                    
            listDic['grid'] = self.text()
            listDic['player'] = str(self.__player)
            listDic['isWin'] = str(self.isWin())
            listDic['player0Status'] = str(not self.__player0Quit)
            listDic['player1Status'] = str(not self.__player1Quit)
            return jsonify(listDic)
            
            
    def isWin(self): 
        for row in range(0,7):
            for col in range(0,7):
                try:
                    if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row+1][col] and self.__grid[row][col] == self.__grid[row+2][col] and self.__grid[row][col] == self.__grid[row+3][col]:
                           return self.__grid[row][col]
                except:
                    tmp = 1
                try:
                    if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row][col+1] and self.__grid[row][col] == self.__grid[row][col+2] and self.__grid[row][col] == self.__grid[row][col+3]:
                           return self.__grid[row][col]
                except:
                    tmp = 1
                try:
                    if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row+1][col+1] and self.__grid[row][col] == self.__grid[row+2][col+2] and self.__grid[row][col] == self.__grid[row+3][col+3]:
                           return self.__grid[row][col]
                except:
                    tmp = 1
                try:
                    if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row-1][col+1] and self.__grid[row][col] == self.__grid[row-2][col+2] and self.__grid[row][col] == self.__grid[row-3][col+3]:
                           return self.__grid[row][col]
                except:
                    tmp = 1
                
        return 0
            
    def emojiText(self):
        txt = '<table style="width:100%">'
        for w in range(0,width):
            txt = txt + "<tr>"
            for h in range(0,height):
                txt = txt + "<td>"
                if self.__grid[h][width-1-w] == Token.PLAYER0:
                    txt = txt+emoji.emojize(':thumbs_up:')
                elif self.__grid[h][width-1-w] == Token.PLAYER1:
                    txt = txt+emoji.emojize(':scissors:')
                elif self.__grid[h][width-1-w] == Token.EMPTY:
                    txt = txt+emoji.emojize(':white_large_square:')
            
                txt = txt + "</td>"
            txt = txt + "</th>"
        txt = txt + "</table>"
        return txt     

    

    def getGame(self,playerID):    
        if playerID == self.__player0ID:
            self.__timeP0 = time.time()
        else:
            self.__timeP1 = time.time()
        
        listDic = {}
        listDic['grid'] = self.text()
        listDic['player'] = str(self.__player)
        listDic['isWin'] = str(self.isWin())
        listDic['player0Status'] = str(not self.__player0Quit)
        listDic['player1Status'] = str(not self.__player1Quit)
    
        return jsonify(listDic)
        
    def getIdNew(self):    
        self.__time = time.time()
        listDic = {}
        listDic['gameID'] = self.__gameID
        listDic['playerID'] = self.__player0ID
    
        return jsonify(listDic)
        
    def getIdJoin(self):   
        listDic = {}
        if self.__player1ID == "":        
            self.__player1ID = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
            listDic['gameID'] = self.__gameID
            listDic['playerID'] = str(self.__player1ID)
        else:
            listDic['gameID'] = 0
            listDic['playerID'] = 0
            
        return jsonify(listDic)
    
    def isPlayer(self, testPlayerID):
        if testPlayerID == self.__player0ID or testPlayerID == self.__player1ID :
            return True
        else:
            return False
            
    def getGameId(self):
        self.__time = time.time()
        return self.__gameID
        
    def getTimeP0(self):
        return self.__timeP0  
        
    def getTimeP1(self):
        return self.__timeP1
    
    def setPlayer0Quit(self, value):
        self.__player0Quit = value
        
    def setPlayer1Quit(self, value):
        self.__player1Quit = value
        
    def getPlayersQuit(self):
        return self.__player0Quit and self.__player1Quit
    
    def text(self):
        self.__time = time.time()
        txt = ""
        for w in range(0,width):
            for h in range(0,height):
                if self.__grid[h][width-1-w] == Token.PLAYER0:
                    txt = txt+"1"
                elif self.__grid[h][width-1-w] == Token.PLAYER1:
                    txt = txt+"0"
                elif self.__grid[h][width-1-w] == Token.EMPTY:
                    txt = txt+"x"
            
            txt = txt + "\n"
        return txt
        
    def print(self):
        print(self.text())
        
    def printEmoji(self):
        self.__time = time.time()
        print(self.emojiText())
    
        
        
        
