import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from os.path import basename
import json
import os

import GraphManager

confFileName = "/home/lucblender/ConnectFour/server/conf/mailConf.json"

def sendMail(subject, message):

    if os.path.isfile(confFileName) == True:
        with open(confFileName, "rb") as fil:
            mailConf = fil.read()
            mailConf = json.loads(mailConf)
        try:
            EMAIL = mailConf.get('email')
            PASSWORD = mailConf.get('password')
            SMTPHOST = mailConf.get('smtpHost')
            SMTPPORT = mailConf.get('smtpPort')
        except:
            print('mail configuration file not well formated')
            return 0

    else:
        print("No mail configuration file found, path sould be: "+confFileName)
        return 0

    GraphManager.graphStatistic()

    # set up the SMTP server
    s = smtplib.SMTP(host=SMTPHOST, port=SMTPPORT)
    s.starttls()
    s.login(EMAIL, PASSWORD)

    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    message = message

    # Prints out the message body for our sake
    print(message)

    # setup the parameters of the message
    msg['From']=EMAIL
    msg['To']= "lucasbonvin@hotmail.com"#, michel.jonath96@gmail.com"
    msg['Subject']=subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    f = "/home/lucblender/ConnectFour/server/graphStatistic.png"
    with open(f, "rb") as fil:
        part = MIMEApplication(fil.read(),Name=basename(f))
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
    msg.attach(part)


    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()
