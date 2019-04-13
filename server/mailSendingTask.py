import json
import requests
import SendMail
from datetime import datetime

def sendMail():
    url = "http://vps.techiteasy.ch:5002/getDataFromGamesCounterReset"
    response = requests.get(url)
    parsed = json.loads(response.text)
    mypath = '/home/lucblender/ConnectFour/server/ConnectFourStats/'

    with open(mypath+datetime.today().strftime('%d-%m-%Y')+'.json','w+') as file:
        file.write(str(json.dumps(parsed, indent=4, sort_keys=True, ensure_ascii=False)))
    SendMail.sendMail("ConnectFour EveryDayStats from: "+ datetime.today().strftime('%d.%m.%Y'),json.dumps(parsed, indent=4, sort_keys=True, ensure_ascii=False))