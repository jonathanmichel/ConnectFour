from enum import Enum
import emoji
from flask import jsonify
import random
import string
import time
from datetime import datetime
from pytz import timezone
import svgwrite
import cairosvg
from copy import deepcopy

class Token(Enum):
    PLAYER0 = 0
    PLAYER1 = 1
    WIN = 3
    EMPTY = -1

class messageChat():
    def __init__(self, text, playerID):
        self.playerID = playerID
        self.text  = text
        self.timestamp = datetime.now(timezone('Europe/Zurich')).strftime('%H:%M:%S')

height, width = 6, 7
DELAY_PLAYER_DEAD = 10
radiusSvgCircle = 20
storePath = '/home/lucblender/ConnectFour/server/'

emCssSampleList = ["em-mahjong","em-candy","em-butterfly","em-sparkles","em-aquarius","em-popcorn","em-recycle","em-symbols","em-telephone_receiver","em-bicyclist","em-dizzy_face","em-airplane","em-bulb","em-burrito"]

class Token(Enum):
    PLAYER0 = 0
    PLAYER1 = 1
    WIN = 3
    EMPTY = -1


class Game():

    nodes = {}

    def __init__(self, player=0, other=None):
        self.__gameID = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
        self.__player0ID = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
        self.__player1ID = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
        self.__joined = False
        self.__player0Quit = False
        self.__player1Quit = False
        self.empty = Token.EMPTY
        self.__AI = False

        if player == 0:
            self.player = Token.PLAYER0
            self.opponent = Token.PLAYER1
        else:
            self.player = Token.PLAYER1
            self.opponent = Token.PLAYER0

        self.__player = player
        self.__numberQuit = 0
        self.__grid = [[Token.EMPTY for x in range(height)] for y in range(width)]
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
        if other:
            self.__dict__ = deepcopy(other.__dict__)

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

    def getJoined(self):
        return self.__joined

    def getPlayerID(self, index):
        if index == 0:
            return self.__player0ID
        elif index == 1:
            return self.__player1ID
        else:
            return "NO PLAYER"


    def getOpponentPlayerID(self, id):
        if id == self.__player0ID:
            return self.__player1ID
        elif id == self.__player1ID:
            return self.__player0ID
        else:
            return "NO PLAYER"

    def reset(self):
        self.__grid = [[Token.EMPTY for x in range(height)] for y in range(width)]
        player = random.randint(0,1)
        if player == 0:
            self.player = Token.PLAYER0
            self.opponent = Token.PLAYER1
        else:
            self.player = Token.PLAYER1
            self.opponent = Token.PLAYER0
        self.__tokenWhoWin = -1
        self.__numberOfGame = self.__numberOfGame +1

    def randomGrid(self):
        self.__grid = [[Token(random.randrange(-1,2)) for x in range(height)] for y in range(width)]

    def playerQuit(self):
        self.__numberQuit = self.__numberQuit + 1

    def getNumberQuit(self):
        return self.__numberQuit

    def getGrid(self):
        return self.__grid

    def getNumberOfGame(self):
        return self.__numberOfGame

    def setToken(self, line):
        if line > width or line < 0:
            return False
        else:
            for w in range(0,height):
                if self.__grid[line][w] == Token.EMPTY:
                    self.__grid[line][w] = self.player
                    self.player,self.opponent = self.opponent,self.player
                    return True
            return False


    def setPlayToken(self, player, line):
        listDic = {}

        if self.isWin() != -1:
            listDic["ERROR"] = "SOMEBODY WON DAMMIT, STOP PLAYING"
            return jsonify(listDic)
        #TODO CHANGED
        if self.player.value == 0 and player != self.__player0ID:
            listDic["ERROR"] = "NOT YOUR TURN"
            return jsonify(listDic)
        if self.player.value == 1 and player != self.__player1ID:
            listDic["ERROR"] = "NOT YOUR TURN"
            return jsonify(listDic)

        if line > width or line < 0:
            listDic["ERROR"] = "TOKEN OUT OF GRID"
            return jsonify(listDic)
        else:
            for w in range(0,height):
                if self.__grid[line][w] == Token.EMPTY:
                    self.__grid[line][w] = self.player
                    self.player,self.opponent = self.opponent,self.player

                    if player == self.__player0ID:
                        listDic['id'] = '0'
                    else:
                        listDic['id'] = '1'
                    listDic['grid'] = self.text()
                    listDic['currentPlayer'] = str(self.player.value)
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
            listDic['currentPlayer'] = str(self.player.value)
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

    def getAI(self):
        return self.__AI

    def setAI(self, AI):
        self.__AI = AI


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
                           return toReturn
                except:
                    tmp = 1

        return -1

    def emojiText(self):
        txt = '<table style="width:100%">'
        for h in range(0,height):
            txt = txt + "<tr>"
            for w in range(0,width):
                txt = txt + "<td>"
                if self.__grid[w][height-1-h] == Token.PLAYER0:
                    txt = txt+emoji.emojize(':thumbs_up:')
                elif self.__grid[w][height-1-h] == Token.PLAYER1:
                    txt = txt+emoji.emojize(':scissors:')
                elif self.__grid[w][height-1-h]== Token.EMPTY:
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
        listDic['currentPlayer'] = str(self.player.value)
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
        if self.__joined == False:
            self.__player1ID = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
            listDic['gameID'] = self.__gameID
            listDic['playerID'] = str(self.__player1ID)
            self.__joined = True
        else:
            listDic['gameID'] = 0
            listDic['playerID'] = 0

        return jsonify(listDic)

    def isPlayer(self, testPlayerID):
        if testPlayerID == self.__player0ID or testPlayerID == self.__player1ID :
            return True
        else:
            return False

    def isPlayer0(self, testPlayerID):
        if testPlayerID == self.__player0ID:
            return True
        else:
            return False

    def isPlayer1(self, testPlayerID):
        if testPlayerID == self.__player1ID:
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

    def getPlayer0Emoji(self):
        return self.__emojiP0

    def getPlayer1Emoji(self):
        return self.__emojiP1

    def getPlayersQuit(self):
        return self.__player0Quit and self.__player1Quit

    def text(self):
        self.__time = time.time()
        txt = ""
        for h in range(0,height):
            for w in range(0,width):
                if self.__grid[w][height-1-h] == Token.PLAYER0:
                    txt = txt+"0"
                elif self.__grid[w][height-1-h] == Token.PLAYER1:
                    txt = txt+"1"
                elif self.__grid[w][height-1-h] == Token.WIN:
                    txt = txt+"2"
                elif self.__grid[w][height-1-h] == Token.EMPTY:
                    txt = txt+"x"

            txt = txt + "\n"
        return txt

    def print(self):
        print(self.text())

    def printEmoji(self):
        self.__time = time.time()
        print(self.emojiText())

    def createSvgBoard(self):
        dwg = svgwrite.Drawing(storePath+'svgBoard.svg', profile='tiny', size =(radiusSvgCircle*width*2,radiusSvgCircle*height*2))

        for w in range(0,width):
            for h in range(0,height):
                color = "grey"
                if self.__grid[w][h] == Token.PLAYER0:
                    color = svgwrite.utils.rgb(237,83,56)
                elif self.__grid[w][h] == Token.PLAYER1:
                    color = svgwrite.utils.rgb(237,255,28)
                elif self.__grid[w][h] == Token.WIN:
                    if self.isWin() == 0:
                        color = svgwrite.utils.rgb(206,43,14)
                    elif self.isWin() == 1:
                        color = svgwrite.utils.rgb(184,196,56)

                dwg.add(dwg.circle((radiusSvgCircle*2*w+radiusSvgCircle,radiusSvgCircle*2*(height-1-h)+radiusSvgCircle),r=radiusSvgCircle,fill=color))

        dwg.save()
        cairosvg.svg2png(url=storePath+'svgBoard.svg', write_to=storePath+'svgBoard.png')

    #AI PART
    def move(self,x):
        board = Game(other=self)
        for y in range(height):
            if board.__grid[x][y] == board.empty:
                board.__grid[x][y] = board.player
                break
        board.player,board.opponent = board.opponent,board.player
        return board

    def __heuristic(self):
        return self.__heuristic_score(self.player)-self.__heuristic_score(self.opponent)

    def __heuristic_score(self, player):
        lines = self.__winlines(player)
        winpositions = self.__winpositions(lines,player)
        score = 0
        for x in range(width):
            for y in range(height-1,0,-1):
                win = winpositions.get("{0},{1}".format(x,y),False)
                below = winpositions.get("{0},{1}".format(x,y-1),False)
                if win and below:
                    score+=height-y*100
        for line in lines:
            pieces = 0
            heights = []
            for x,y in line:
                if self.__grid[x][y] == player:
                    pieces = pieces + 1
                elif self.__grid[x][y] == self.empty:
                    heights.append(y)
            heightscore = height - int(sum(heights) / float(len(heights)))
            score=score+pieces*heightscore
        return score

    def __winpositions(self, lines, player):
        lines = self.__winlines(player)
        winpositions = {}
        for line in lines:
            pieces = 0
            empty = None
            for x,y in line:
                if self.__grid[x][y] == player:
                    pieces = pieces + 1
                elif self.__grid[x][y] == self.empty:
                    if not empty == None:
                        break
                    empty = (x,y)
            if pieces==3:
                winpositions["{0},{1}".format(x,y)]=True
        return winpositions

    def __winlines(self, player):
        lines = []
        # horizontal
        for y in range(height):
            winning = []
            for x in range(width):
                if self.__grid[x][y] == player or self.__grid[x][y] == self.empty:
                    winning.append((x,y))
                    if len(winning) >= 4:
                        lines.append(winning[-4:])
                else:
                    winning = []
        # vertical
        for x in range(width):
            winning = []
            for y in range(height):
                if self.__grid[x][y] == player or self.__grid[x][y] == self.empty:
                    winning.append((x,y))
                    if len(winning) >= 4:
                        lines.append(winning[-4:])
                else:
                    winning = []
        # diagonal
        winning = []
        for cx in range(width-1):
            sx,sy = max(cx-2,0),abs(min(cx-2,0))
            winning = []
            for cy in range(height):
                x,y = sx+cy,sy+cy
                if x<0 or y<0 or x>=width or y>=height:
                    continue
                if self.__grid[x][y] == player or self.__grid[x][y] == self.empty:
                    winning.append((x,y))
                    if len(winning) >= 4:
                        lines.append(winning[-4:])
                else:
                    winning = []
        # other diagonal
        winning = []
        for cx in range(width-1):
            sx,sy = width-1-max(cx-2,0),abs(min(cx-2,0))
            winning = []
            for cy in range(height):
                x,y = sx-cy,sy+cy
                if x<0 or y<0 or x>=width or y>=height:
                    continue
                if self.__grid[x][y] == player or self.__grid[x][y] == self.empty:
                    winning.append((x,y))
                    if len(winning) >= 4:
                        lines.append(winning[-4:])
                else:
                    winning = []
        # return
        return lines

    def __iterative_deepening(self,think):
        g = (3,None)
        start = time.time()
        for d in range(1,10):
            g = self.__mtdf(g, d)
            print(time.time()-start>think)
            if time.time()-start>think:
                print("break")
                break
        return g;

    def __mtdf(self, g, d):
        upperBound = +1000
        lowerBound = -1000
        best = g
        while lowerBound < upperBound:
            if g[0] == lowerBound:
                beta = g[0]+1
            else:
                beta = g[0]
            g = self.__minimax(True, d, beta-1, beta)
            if g[1]!=None:
                best = g
            if g[0] < beta:
                upperBound = g[0]
            else:
                lowerBound = g[0]
        return best

    def __minimax(self, player, depth, alpha, beta):
        lower = Game.nodes.get(str(self)+str(depth)+'lower',None)
        upper = Game.nodes.get(str(self)+str(depth)+'upper',None)
        if lower != None:
            if lower >= beta:
                return (lower,None)
            alpha = max(alpha,lower)
        if upper != None:
            if upper <= alpha:
                return (upper,None)
            beta = max(beta,upper)
        if self.won():
            if player:
                return (-999,None)
            else:
                return (+999,None)
        elif self.tied():
            return (0,None)
        elif depth==0:
            return (self.__heuristic(),None)
        elif player:
            best = (alpha,None)
            for x in range(width):
                if self.__grid[x][height-1]==self.empty:
                    value = self.move(x).__minimax(not player,depth-1,best[0],beta)[0]
                    if value>best[0]:
                        best = value,x
                    if value>beta:
                        break
        else:
            best = (beta,None)
            for x in range(width):
                if self.__grid[x][height-1]==self.empty:
                    value = self.move(x).__minimax(not player,depth-1,alpha,best[0])[0]
                    if value<best[0]:
                        best = value,x
                    if alpha>value:
                        break
        if best[0] <= alpha:
            Game.nodes[str(self)+str(depth)+"upper"] = best[0]
            Game.nodes[self.__mirror()+str(depth)+"upper"] = best[0]
        elif best[0] >= beta:
            Game.nodes[str(self)+str(depth)+"lower"] = best[0]
            Game.nodes[self.__mirror()+str(depth)+"lower"] = best[0]
        return best

    def best(self):
        return self.__iterative_deepening(2)[1]

    def tied(self):
        for x in range(width):
                for y in range(height):
                    if self.__grid[x][y]==self.empty:
                        return False
        return True

    def won(self):
        # horizontal
        for y in range(height):
            winning = []
            for x in range(width):
                if self.__grid[x][y] == self.opponent:
                    winning.append((x,y))
                    if len(winning) == 4:
                        return winning
                else:
                    winning = []
        # vertical
        for x in range(width):
            winning = []
            for y in range(height):
                if self.__grid[x][y] == self.opponent:
                    winning.append((x,y))
                    if len(winning) == 4:
                        return winning
                else:
                    winning = []
        # diagonal
        winning = []
        for cx in range(width-1):
            sx,sy = max(cx-2,0),abs(min(cx-2,0))
            winning = []
            for cy in range(height):
                x,y = sx+cy,sy+cy
                if x<0 or y<0 or x>=width or y>=height:
                    continue
                if self.__grid[x][y] == self.opponent:
                    winning.append((x,y))
                    if len(winning) == 4:
                        return winning
                else:
                    winning = []
        # other diagonal
        winning = []
        for cx in range(width-1):
            sx,sy = width-1-max(cx-2,0),abs(min(cx-2,0))
            winning = []
            for cy in range(height):
                x,y = sx-cy,sy+cy
                if x<0 or y<0 or x>=width or y>=height:
                    continue
                if self.__grid[x][y] == self.opponent:
                    winning.append((x,y))
                    if len(winning) == 4:
                        return winning
                else:
                    winning = []
        # default
        return None

    def __mirror(self):
        string = ''
        for y in range(height):
            for x in range(width):
                string+=' '+self.__grid[width-1-x][height-1-y].name
            string+="\n"
        return string

    def __str__(self):
        string = ''
        for y in range(height):
            for x in range(width):
                string+=' '+self.__grid[x][height-1-y].name
            string+="\n"
        return string




