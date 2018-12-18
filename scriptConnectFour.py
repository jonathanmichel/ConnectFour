from os import system as s
from time import sleep

sleep(10)

s("autossh -M 0 -R connectfour.serveo.net:80:localhost:5002 serveo.net & autossh -M 0 -R connectfourssh:22:localhost:22 serveo.net & exit 0")

sleep(10)

s("sudo python3 /home/pi/ConnectFour/server/flask_four_in_a_row.py")
