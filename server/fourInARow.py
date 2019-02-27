from enum import Enum
import emoji
from flask import jsonify
import random
import string
import time
from datetime import datetime
from pytz import timezone

class Token(Enum):
    PLAYER0 = 0
    PLAYER1 = 1
    WIN = 3
    EMPTY = -1

class messageChat():
    def __init__(self, text, playerID):
        self.playerID = playerID
        self.text  = text
        self.timestamp = datetime.now(timezone('Europe/Zurich')).strftime('%H:%M%S')

width, height = 6, 7
DELAY_PLAYER_DEAD = 10

emCssSampleList = ["em-mahjong","em-candy","em-butterfly","em-sparkles","em-aquarius","em-popcorn","em-recycle","em-symbols","em-telephone_receiver","em-bicyclist","em-dizzy_face","em-airplane","em-bulb","em-burrito"]

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
        self.__timeP1 = 0
        self.__tokenWhoWin = -1
        self.__numberOfGame = 1
        self.__chat = []

        index1 = random.randrange(0,14)
        index2 = random.randrange(0,14)
        while index1 == index2:
            index2 = random.randrange(0,14)

        self.__emojiP0 = emCssSampleList[index1]
        self.__emojiP1 = emCssSampleList[index2]

    def addMessage(self, text, playerID):
        if len(self.__chat)>19:
            self.__chat.pop(0)
        self.__chat.append(messageChat(text, playerID))

    def addMessageRandom(self):
        if len(self.__chat)>19:
            self.__chat.pop(0)
        if random.randrange(0,10)>5:
            self.__chat.append(messageChat("test", self.__player1ID))
        else:
            self.__chat.append(messageChat("test", self.__player0ID))

    def getChat(self):
        return self.__chat

    def getPlayerID(self, index):
        if index == 0:
            return self.__player0ID
        elif index == 1:
            return self.__player1ID
        else:
            return "NO PLAYER"

    def reset(self):
        self.__grid = [[Token.EMPTY for x in range(width)] for y in range(height)]
        self.__player = random.randint(0,1)
        self.__tokenWhoWin = -1
        self.__numberOfGame = self.__numberOfGame +1

    def playerQuit(self):
        self.__numberQuit = self.__numberQuit + 1

    def getNumberQuit(self):
        return self.__numberQuit

    def getGrid(self):
        return self.__grid

    def getNumberOfGame(self):
        return self.__numberOfGame

    def setToken(self, line):
        if self.__player == 0:
            token = Token.PLAYER0
        else:
            token = Token.PLAYER1

        if line > width or line < 0:
            return False
        else:
            for w in range(0,height):
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

        if self.isWin() != -1:
            listDic["ERROR"] = "SOMEBODY WON DAMMIT, STOP PLAYING"
            return jsonify(listDic)
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
            for w in range(0,height):
                if self.__grid[line][w] == Token.EMPTY:
                    self.__grid[line][w] = token
                    if self.__player == 0:
                        self.__player = 1
                    else:
                        self.__player = 0
                    if player == self.__player0ID:
                        listDic['id'] = '0'
                    else:
                        listDic['id'] = '1'
                    listDic['grid'] = self.text()
                    listDic['currentPlayer'] = str(self.__player)
                    listDic['isWin'] = str(self.isWin())
                    listDic['player0Status'] = self.getPlayer0Status()
                    listDic['player1Status'] = self.getPlayer1Status()
                    listDic['player0Emoji'] = self.__emojiP0
                    listDic['player1Emoji'] = self.__emojiP1
                    listDic['messages'] = []
                    for message in self.__chat:
                        messageDic = {}
                        messageDic['playerID']=message.playerID
                        messageDic['text']=message.text
                        messageDic['timestamp']=message.timestamp
                        listDic['messages'].append(messageDic)
                    return jsonify(listDic)

            if player == self.__player0ID:
                listDic['id'] = '0'
            else:
                listDic['id'] = '1'
            listDic['grid'] = self.text()
            listDic['currentPlayer'] = str(self.__player)
            listDic['isWin'] = str(self.isWin())
            listDic['player0Status'] = self.getPlayer0Status()
            listDic['player1Status'] = self.getPlayer1Status()
            listDic['player0Emoji'] = self.__emojiP0
            listDic['player1Emoji'] = self.__emojiP1
            listDic['messages'] = []
            for message in self.__chat:
                messageDic = {}
                messageDic['playerID']=message.playerID
                messageDic['text']=message.text
                messageDic['timestamp']=message.timestamp
                listDic['messages'].append(messageDic)
            return jsonify(listDic)

    def getPlayer0Status(self):
        return (time.time()-self.__timeP0) < DELAY_PLAYER_DEAD

    def getPlayer1Status(self):
        return (time.time()-self.__timeP1) < DELAY_PLAYER_DEAD


    def isWin(self):
        isDraw = True
        for row in self.__grid:
            for gridToken in row:
                if gridToken == Token.EMPTY:
                    isDraw = False
        if isDraw == True:
            return 2

        if self.__tokenWhoWin != -1:

            return self.__tokenWhoWin

        for row in range(0,7):
            for col in range(0,7):
                try:
                    if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row+1][col] and self.__grid[row][col] == self.__grid[row+2][col] and self.__grid[row][col] == self.__grid[row+3][col]:
                           toReturn = self.__grid[row][col].value
                           self.__grid[row][col] = Token.WIN
                           self.__grid[row+1][col] = Token.WIN
                           self.__grid[row+2][col] = Token.WIN
                           self.__grid[row+3][col] = Token.WIN
                           self.__tokenWhoWin = toReturn
                           print("a")
                           print(row)
                           print(col)
                           return toReturn
                except:
                    tmp = 1
                try:
                    if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row][col+1] and self.__grid[row][col] == self.__grid[row][col+2] and self.__grid[row][col] == self.__grid[row][col+3]:
                           toReturn = self.__grid[row][col].value
                           self.__grid[row][col] = Token.WIN
                           self.__grid[row][col+1] = Token.WIN
                           self.__grid[row][col+2] = Token.WIN
                           self.__grid[row][col+3] = Token.WIN
                           self.__tokenWhoWin = toReturn
                           print("b")
                           print(row)
                           print(col)
                           return toReturn
                except:
                    tmp = 1
                try:
                    if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row+1][col+1] and self.__grid[row][col] == self.__grid[row+2][col+2] and self.__grid[row][col] == self.__grid[row+3][col+3]:
                           toReturn = self.__grid[row][col].value
                           self.__grid[row][col] = Token.WIN
                           self.__grid[row+1][col+1] = Token.WIN
                           self.__grid[row+2][col+2] = Token.WIN
                           self.__grid[row+3][col+3] = Token.WIN
                           self.__tokenWhoWin = toReturn
                           print("c")
                           print(row)
                           print(col)
                           return toReturn
                except:
                    tmp = 1
                try:
                    if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row-1][col+1] and self.__grid[row][col] == self.__grid[row-2][col+2] and self.__grid[row][col] == self.__grid[row-3][col+3] and row > 2:
                           toReturn = self.__grid[row][col].value
                           self.__grid[row][col] = Token.WIN
                           self.__grid[row-1][col+1] = Token.WIN
                           self.__grid[row-2][col+2] = Token.WIN
                           self.__grid[row-3][col+3] = Token.WIN
                           self.__tokenWhoWin = toReturn
                           print("d")
                           print(row)
                           print(col)
                           return toReturn
                except:
                    tmp = 1

        return -1

    def emojiText(self):
        txt = '<table style="width:100%">'
        for w in range(0,width):
            txt = txt + "<tr>"
            for h in range(0,height):
                txt = txt + "<td>"
                if self.__grid[h][height-1-w] == Token.PLAYER0:
                    txt = txt+emoji.emojize(':thumbs_up:')
                elif self.__grid[h][height-1-w] == Token.PLAYER1:
                    txt = txt+emoji.emojize(':scissors:')
                elif self.__grid[h][height-1-w] == Token.EMPTY:
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
        if playerID == self.__player0ID:
            listDic['id'] = '0'
        else:
            listDic['id'] = '1'
        listDic['grid'] = self.text()
        listDic['currentPlayer'] = str(self.__player)
        listDic['isWin'] = str(self.isWin())
        listDic['player0Status'] = self.getPlayer0Status()
        listDic['player1Status'] = self.getPlayer1Status()
        listDic['player0Emoji'] = self.__emojiP0
        listDic['player1Emoji'] = self.__emojiP1
        listDic['messages'] = []
        for message in self.__chat:
            messageDic = {}
            messageDic['playerID']=message.playerID
            messageDic['text']=message.text
            messageDic['timestamp']=message.timestamp
            listDic['messages'].append(messageDic)

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
        return self.__gameID

    def getTimeP0(self):
        return self.__timeP0

    def getTimeP1(self):
        return self.__timeP1

    def setPlayer0Quit(self, value):
        self.__player0Quit = value

    def setPlayer1Quit(self, value):
        self.__player1Quit = value

    def setPlayerEmoji(self, playerID, value):
        if playerID == self.__player0ID:
            self.setPlayer0Emoji(value)
            print("emoji 0")
        elif playerID == self.__player1ID:
            self.setPlayer1Emoji(value)
            print("emoji 1")
        else:
            print("emoji null")

    def setPlayer0Emoji(self, value):
        self.__emojiP0 = value

    def setPlayer1Emoji(self, value):
        self.__emojiP1 = value

    def getPlayersQuit(self):
        return self.__player0Quit and self.__player1Quit

    def text(self):
        self.__time = time.time()
        txt = ""
        #self.__grid = [[Token(random.randrange(-1,2)) for x in range(width)] for y in range(height)]
        for w in range(0,width):
            for h in range(0,height):
                if self.__grid[h][width-1-w] == Token.PLAYER0:
                    txt = txt+"0"
                elif self.__grid[h][height-1-w] == Token.PLAYER1:
                    txt = txt+"1"
                elif self.__grid[h][height-1-w] == Token.WIN:
                    txt = txt+"2"
                elif self.__grid[h][height-1-w] == Token.EMPTY:
                    txt = txt+"x"

            txt = txt + "\n"
        return txt

    def print(self):
        print(self.text())

    def printEmoji(self):
        self.__time = time.time()
        print(self.emojiText())




