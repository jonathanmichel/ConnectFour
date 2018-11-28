# ConnectFour, an Embedeed Hardware alternative

## Description
A little project made to pass time. A connect four game with a Web emoji based on EMOJI (Client folder).
All the logic of the game is taken care by a little RESTFULL server in Python (Server Folder). 

## Client 

## Server
### Launch the server and link with ngrok

Launch the server with ``` python flask_four_in_a_row.py ```.
Link the server to ngrok client with ```ngrok tcp -region eu 5002```, the output from ngrok will give you the port to use in the Web GUI.


### Rout available in the api
Here are described all the actual available rout of the RESTFULL server

#### /game/<int:row>
Deprecated version of the ```/play``` (see below). Is switching between player automatically and same output as ```/getShittyEmojiGame``` 
   
#### /play/<int:player>/<int:row>
Answer example formated in JSON
Actual route to play the game, need to indicate which player is playing (0,1) and which row did he choose.

Example of answer formated in JSON if in case of success
```
{
  "grid": "xxxxxxx\nxxxxxxx\nxxxxxxx\nxxxxxxx\nxxxxxxx\nxxxxxxx\n", 
  "isWin": "0", 
  "player": "0"
}
``` 

Example of answer formated in JSON if in case of error
```
{
  "ERROR": "NOT YOUR TURN"
}
``` 
    
#### /getShittyEmojiGame

Shitty example version of the connect four board, works in browser

#### /getGame

Example of answer formated in JSON
```
{
  "grid": "xxxxxxx\nxxxxxxx\nxxxxxxx\nxxxxxxx\nxxxxxxx\nxxxxxxx\n", 
  "isWin": "0", 
  "player": "0"
}
``` 
    
#### 'resetGame

Reset Game, no answer