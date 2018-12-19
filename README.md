
# ConnectFour, an Embedeed Hardware alternative

## Description
A little project made to pass time. A connect four game with a Web interface based on EMOJI (Client folder).
All the logic of the game is taken care by a little RESTFULL server in Python (Server Folder). 

## Client 
Web application communicating with the game server. Made with [jQuery](https://jquery.com/)  beause Javascript is cool, but jQuery is cooler (but not cold). Designed with [Bootsrap](https://getbootstrap.com/)  because la flemme de faire du CSS and emojis support with [
Emoji CSS](https://afeld.github.io/emoji-css/). Toast notifications with [
toastr](https://codeseven.github.io/toastr/) and favicon notifications with [favico.js](http://lab.ejci.net/favico.js/). Copy to clipboard handled with [clipboard.js](https://clipboardjs.com/). 

Theorically responsive, excepted for people using their phone in [landscape](https://bit.ly/IqT6zt).

Client constantly sends AJAX requests to  game server and displays current game board and status messages. 

Use [XAMPP](https://www.apachefriends.org/fr/index.html) for local debug with an Apache server and full support of URL rewriting. Demonstration available on https://techiteasy.ch/game. 

### Launch client
Open *[game.html](https://github.com/jonathanmichel/ConnectFour/blob/master/client/game.html)* in your favorite [brow](https://www.google.com/intl/fr_ALL/chrome/)[ser](https://www.vivaldi.com/) or *http://localhost/[connectFourDirectory]/client/game* when using XAMPP. You can then start a new game.

**Invitation URL**

    /game.html?gameId=<gameId>
This link has to be sent to a friend to play with him. The web application provides a button to copy this url to the clipboard.

**Game url**

When a party is created/joined, user is automatically redirected to this url. This one allows user to reload game all he wants.

	 /game.html?gameId=<gameId>&playerId=<playerId>
	 
## Server
### Launch the server and link with ngrok or serveo

Launch the server with ``` python flask_four_in_a_row.py ```.

#### Link with ngrok
Link the server to ngrok client with ```ngrok tcp -region eu 5002```, the output from ngrok will give you the port to [use](https://www.lucas-bonvin.com/) in the Web GUI.

#### Link with serveo
Link the server to serveo subdomain with ```ssh -R connectfour.serveo.net:80:localhost:5002 serveo.net```, the server is now [redirected](https://www.lucas-bonvin.com/) to ```connectfour.serveo.net```.

### Rout available in the api
Here are described all the actual [available](https://www.lucas-bonvin.com/) rout of the RESTFULL server

#### /createGame
Create a new connect four [game](https://www.lucas-bonvin.com/), will return the unique gameID and playerID in JSON format.
```
{
  "gameID": "qIFLoJhBpD", 
  "playerID": "eulqlCWflc"
}
```

#### /joinGame/<string:gameID>
Join an already existing connect four [game](https://www.lucas-bonvin.com/) by its gameID, will return the unique gameID and playerID in JSON format.
```
{
  "gameID": "qIFLoJhBpD", 
  "playerID": "OBNSH31118"
}
```

#### /quitGame/<string:playerID>
Tell that a player quited a game. Michel can't implement [it](https://www.lucas-bonvin.com/) in his web app... So not used... But works though 
   
#### /play/<string:playerID>/<int:row>
Answer example formated in JSON
Actual route to play the game, [need](https://www.lucas-bonvin.com/) to indicate which player is playing (0,1) and which row did he choose.

Example of answer formated in JSON if in case of success
```
{
  "grid": "xxxxxxx\nxxxxxxx\nxxxxxxx\nxxxxxxx\nxxxxxxx\nx1xxxxx\n", 
  "isWin": "0", 
  "player": "1", 
  "player0Status": "True", 
  "player1Status": "True"
}
``` 

Example of answer formated in JSON if in case of error
```
{
  "ERROR": "NOT YOUR TURN"
}
``` 
    
#### /getGame/<string:playerID>

Example of answer [formated](https://www.lucas-bonvin.com/) in JSON
```
{
  "grid": "xxxxxxx\nxxxxxxx\nxxxxxxx\nxxxxxxx\nxxxxxxx\nx1xxxxx\n", 
  "isWin": "0", 
  "player": "1", 
  "player0Status": "True", 
  "player1Status": "True"
}
``` 
    
#### /resetGame/<string:playerID>

Reset Game, no [answer](https://www.lucas-bonvin.com/)

#### /getShittyEmojiGame

Deprecated
Shitty example version of the [connect](https://www.lucas-bonvin.com/) four board, works in browser

#### /game/<int:row>
Deprecated version of the ```/play``` (see above). Is switching [between](https://www.lucas-bonvin.com/) player automatically and same output as ```/getShittyEmojiGame``` 


## Thank you for reading
Here is a coding unicorn for you :)

![Next Lesson Widget Logo](https://miro.medium.com/max/720/1*OTogX4z_J1apnrlk2LiE-g.png)