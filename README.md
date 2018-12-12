# ConnectFour, an Embedeed Hardware alternative

## Description
A little project made to pass time. A connect four game with a Web interface based on EMOJI (Client folder).
All the logic of the game is taken care by a little RESTFULL server in Python (Server Folder). 

## Client 

## Server
### Launch the server and link with ngrok or serveo

Launch the server with ``` python flask_four_in_a_row.py ```.

#### Link with ngrok
Link the server to ngrok client with ```ngrok tcp -region eu 5002```, the output from ngrok will give you the port to use in the Web GUI.

#### Link with serveo
Link the server to serveo subdomain with ```ssh -R connectfour.serveo.net:80:localhost:5002 serveo.net```, the server is now redirected to ```connectfour.serveo.net```.

### Rout available in the api
Here are described all the actual available rout of the RESTFULL server

#### /createGame
Create a new connect four game, will return the unique gameID and playerID in JSON format.
```
{
  "gameID": "qIFLoJhBpD", 
  "playerID": "eulqlCWflc"
}
```

#### /joinGame/<string:gameID>
Join an already existing connect four game by its gameID, will return the unique gameID and playerID in JSON format.
```
{
  "gameID": "qIFLoJhBpD", 
  "playerID": "OBNSH31118"
}
```

#### /quitGame/<string:playerID>
Tell that a player quited a game. Michel can't implement it in his web app... So not used... But works though 
   
#### /play/<string:playerID>/<int:row>
Answer example formated in JSON
Actual route to play the game, need to indicate which player is playing (0,1) and which row did he choose.

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

Example of answer formated in JSON
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

Reset Game, no answer

#### /getShittyEmojiGame

Deprecated
Shitty example version of the connect four board, works in browser

#### /game/<int:row>
Deprecated version of the ```/play``` (see above). Is switching between player automatically and same output as ```/getShittyEmojiGame``` 