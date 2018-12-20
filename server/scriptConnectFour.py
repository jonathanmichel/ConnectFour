from os import system as s
from time import sleep
import subprocess
import json
import os

ngrokSftpIP = "/home/pi/ConnectFour/ngrokSftpIP"

sleep(10)

s("autossh -M 0 -R connectfour.serveo.net:80:localhost:5002 serveo.net & autossh -M 0 -R connectfourssh:22:localhost:22 serveo.net & exit 0")

sleep(10)

s("sudo python3 /home/pi/ConnectFour/server/flask_four_in_a_row.py &")

s("/home/pi/ngrok tcp -region eu 22 > /dev/null &")
try:
    sleep(5)
    requestOutput = subprocess.check_output("curl http://localhost:4040/api/tunnels", shell=True)
    requestOutput = requestOutput.decode("utf-8")
    requestOutputJson = json.loads(requestOutput)
    url = requestOutputJson.get("tunnels")[0].get("public_url")
    url = url.replace("tcp", "sftp")
    with open(ngrokSftpIP, "w") as f: 
        f.write(url) 
except:
    print("error")






