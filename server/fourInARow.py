from enum import Enum
import emoji

class Token(Enum):
    EMPTY = 0
    RED = 1
    YELLOW = 2
    
width, height = 6, 7

class Game():

    def __init__(self, player):
        self.__player = player
        self.__grid = [[Token.EMPTY for x in range(width)] for y in range(height)] 
        
    def reset(self):
        self.__grid = [[Token.EMPTY for x in range(width)] for y in range(height)] 
        
    def getGrid(self):
        return self.__grid
    
    def setToken(self, line):
        if self.__player == 0:
            token = Token.RED
        else:
            token = Token.YELLOW
        
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
           
    # return 1 if success
    # return 2 if not your turn
    # return 3 if not in grid
    # return 4 if line full
    # return 5 player not 0 or 1
    # return 6 player 0 win
    # return 7 player 1 win
    
    def setPlayToken(self, player, line):    
        if player != self.__player:
            return "2"
        if player > 1 or player < 0:
            return "5"
        
        if self.__player == 0:
            token = Token.RED
        else:
            token = Token.YELLOW
        
        if line > width or line < 0:
            return "3"
        else:
            for w in range(0,height-1):
                if self.__grid[line][w] == Token.EMPTY:
                    self.__grid[line][w] = token
                    if self.__player == 0:
                        self.__player = 1
                    else:
                        self.__player = 0
                    if self.isWin() == Token.RED:
                        return "6"
                    if self.isWin() == Token.YELLOW:
                        return "7"
                    return "1"
            return "4"
            
            
    def isWin(self):
    
        for row in range(0,3):
            for col in range(0,6):
                if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row+1][col] and self.__grid[row][col] == self.__grid[row+2][col] and self.__grid[row][col] == self.__grid[row+3][col]:
                       return self.__grid[row][col]
                       
        for row in range(0,7):
            for col in range(0,4):
                if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row][col+1] and self.__grid[row][col] == self.__grid[row][col+2] and self.__grid[row][col] == self.__grid[row][col+3]:
                       return self.__grid[row][col]
                   
        for row in range(0,3):
            for col in range(0,4):
                if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row+1][col+1] and self.__grid[row][col] == self.__grid[row+2][col+2] and self.__grid[row][col] == self.__grid[row+3][col+3]:
                       return self.__grid[row][col]

        for row in range(3,6):
            for col in range(0,4):
                if self.__grid[row][col] != Token.EMPTY and self.__grid[row][col] == self.__grid[row-1][col+1] and self.__grid[row][col] == self.__grid[row-2][col+2] and self.__grid[row][col] == self.__grid[row-3][col+3]:
                       return self.__grid[row][col]
        return 0
            
    def emojiText(self):
        txt = '<table style="width:100%">'
        for w in range(0,width):
            txt = txt + "<tr>"
            for h in range(0,height):
                txt = txt + "<td>"
                if self.__grid[h][width-1-w] == Token.RED:
                    txt = txt+emoji.emojize(':thumbs_up:')
                elif self.__grid[h][width-1-w] == Token.YELLOW:
                    txt = txt+emoji.emojize(':scissors:')
                elif self.__grid[h][width-1-w] == Token.EMPTY:
                    txt = txt+emoji.emojize(':white_large_square:')
            
                txt = txt + "</td>"
            txt = txt + "</th>"
        txt = txt + "</table>"
        return txt        
        
    def text(self):
        txt = ""
        for w in range(0,width):
            for h in range(0,height):
                if self.__grid[h][width-1-w] == Token.RED:
                    txt = txt+"1"
                elif self.__grid[h][width-1-w] == Token.YELLOW:
                    txt = txt+"0"
                elif self.__grid[h][width-1-w] == Token.EMPTY:
                    txt = txt+"x"
            
            txt = txt + "\n"
        return txt
        
    def print(self):
        print(self.text())
        
    def printEmoji(self):
        print(self.emojiText())
    
        
        
        
