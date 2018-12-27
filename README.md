
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

### Prerequisites

The server and server launch automatisation script are made with python, python 3 is needed and since some library are used, pip3 is also needed.
```
sudo apt-get install python3
sudo apt-get install python3-pip
```

The python dependency are flask (rest server) and emoji(old GUI but keep it for nostalgia) and matplotlib (statistics plot of the game).
```
sudo pip3 install flask
sudo pip3 install emoji
sudo pip3 install matplotlib
```

If you want to test your server on the web and not only in local, you can use ngrok or serveo, the use of those are described above. To install ngrok follow the instruction here: https://ngrok.com/download. 

For using serveo, you only need ssh! No other installation needed. In our case, autossh is used to auto-reconnect to ssh if the connection is aborted.

```
sudo apt-get install autossh
```

The server has a code that is ment to be called every day: [mailSendingTask.py](https://github.com/jonathanmichel/ConnectFour/blob/master/server/mailSendingTask.py)
For this purpose, you have to configure your email smpt parameter. To do so, you have to create a file ```/con/mailConf.json``` containing some authentication data. An empty example is here: [/conf/mailConf-Empty.json](https://github.com/jonathanmichel/ConnectFour/blob/master/server/conf/mailConf-Empyt.json)

### Launch the server and link with ngrok or serveo

Launch the server with ``` python flask_four_in_a_row.py ```.

#### Link with ngrok
Link the server to ngrok client with ```ngrok tcp -region eu 5002```, the output from ngrok will give you the port to [use](https://www.lucas-bonvin.com/) in the Web GUI.

#### Link with serveo
Link the server to serveo subdomain with ```ssh -R myCustomSubdomain.serveo.net:80:localhost:5002 serveo.net```, the server is now [redirected](https://www.lucas-bonvin.com/) to ```myCustomSubdomain.serveo.net```. 

#### Full automatisation with kindly provided script
In the server directory you can find a python script [scriptConnectFour.py](https://github.com/jonathanmichel/ConnectFour/blob/master/server/scriptConnectFour.py). This script is usefull if you want to put the server on a micro-computer like for example a raspberry pi.

This script will
- do 2 serveo binding
    - first one for the localhost:5002 (where the server will be running)
    - second for the localhost:22 (yes it's for using ssh, amazing)
- do a ngrok binding also for ssh buuuuuuut, this one is used mostly to use sftp (since we already have ssh with serveo but I still haven't found how to use it with sftp...)
    - also the script will call the ngrok api to get the url port where its redirected
    - and with this info, it will save it in a little file (path on top of [scriptConnectFour.py](https://github.com/jonathanmichel/ConnectFour/blob/master/server/scriptConnectFour.py)) so you can find it easily :sunglasses:

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
  "currentPlayer": "0", 
  "grid": "xxxxxxx\nx02xxxx\nx02xxxx\nx02xxxx\nx12xxxx\nx001xxx\n", 
  "id": "1", 
  "isWin": "1", 
  "player0Emoji": "em-butterfly", 
  "player0Status": true, 
  "player1Emoji": "em-bulb", 
  "player1Status": true
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
  "currentPlayer": "0", 
  "grid": "xxxxxxx\nx02xxxx\nx02xxxx\nx02xxxx\nx12xxxx\nx001xxx\n", 
  "id": "1", 
  "isWin": "1", 
  "player0Emoji": "em-butterfly", 
  "player0Status": true, 
  "player1Emoji": "em-bulb", 
  "player1Status": true
}
``` 

#### /setEmoji/<string:playerID>/<string:emojiCssRef>

You can change the emoji of the player defined by its playerID and give the new Emoji you want to use by its ref in emojiCssRef defined by [Emoji CSS](https://afeld.github.io/emoji-css/).
    
#### /resetGame/<string:playerID>

Reset Game, no [answer](https://www.lucas-bonvin.com/)

#### /getDataFromGames
I love statistics, so I added statistics! You can have data about the current online game, some overall statistics and statistics about today's game! Yeah I know pretty awesome!
```
{
	"gameIdList": {
		"InP4o0YjGP": {
			"isWin": 0,
			"numberOfGame": 2,
			"player0Status": true,
			"player1Status": true,
			"playersID": ["Xk4RqxPgfX",
			"6llSrCv95M"]
		},
		"LjDUIkiDe7": {
			"isWin": -1,
			"numberOfGame": 1,
			"player0Status": true,
			"player1Status": false,
			"playersID": ["No9FDm3UJB",
			""]
		}
	},
	"gameKilled": 19,
	"gameKilledToday": 2,
	"gameKilledWithoutJoin": 12,
	"gameKilledWithoutJoinToday": 1,
	"gameSinceStartup": 21,
	"gameToday": 4,
	"meanPlayedGame": 0.8421052631578947,
	"meanPlayedGameToday": 2.0,
	"offlinePlayer": 1,
	"onlineGame": 2,
	"onlinePlayer": 3,
	"severOnline": "2018-12-26 18:22:37.716929",
	"severStart": "2018-12-26 23:07:34.627688"
}
```
    
#### /getDataFromGamesCounterReset
It is completly similar to ```/getDataFromGames```, will return the same outputs, **but this one is ment to be call everyday to reset all the day related statistics.**  

	
#### /getGraph/gameSessionPlayed
I told you, I like statistics, but what is better than just statistics? Graphs with statistics!
the gameSessionPlayed graph give you the mean of played session overall, the mean of played session today and the amount of game session played for all online game.

![gameSessionPlayed](https://static1.squarespace.com/static/5aca3b7ab10598283d220390/5afd7122575d1f528bda5053/5c25407870a6ad01642e5387/1545945210269/gameSessionPlayed.png?format=1500w) 
    
#### /getGraph/graphStatistic
The software store everyday the output of ```/getDataFromGames``` and so, with ``` /getGraph/graphStatistic ```, you can have a graph of some of those statistics in function of the time.

![graphStatistic](https://static1.squarespace.com/static/5aca3b7ab10598283d220390/5afd7122575d1f528bda5053/5c2540750ebbe8593a086aca/1545945209458/graphStatistic.png?format=2500w) 

#### /getShittyEmojiGame

Deprecated
Shitty example version of the [connect](https://www.lucas-bonvin.com/) four board, works in browser, example of the UI just below

![First UI](https://static1.squarespace.com/static/5aca3b7ab10598283d220390/5afd7122575d1f528bda5053/5c1b5a451ae6cf51a5dcdce9/1545296456474/firstUI.PNG) First UI, never forget :heart:

#### /game/<int:row>
Deprecated version of the ```/play``` (see above). Is switching [between](https://www.lucas-bonvin.com/) player automatically and same output as ```/getShittyEmojiGame``` 


## Thank you for reading
Here is a coding unicorn for you :)

![It's a unicorn coding](https://miro.medium.com/max/720/1*OTogX4z_J1apnrlk2LiE-g.png)