# pip3 install telepot
import time, datetime 

import telepot 

from telepot.loop import MessageLoop 

from grovepi import * 

led = 2 #connect led grovepi module on D2 

now = datetime.datetime.now() 

#LED White 

pinMode(led,"OUTPUT") 

time.sleep(1) 

digitalWrite(led,0) #Off initially 

 

def action(msg): 

    chat_id = msg['chat']['id'] 

    command = msg['text'] 

    print ('Received: %s' % command) 

    if 'on' in command: 

        message = "Turned on " 

        if 'led' in command: 

            message = message + "led " 

            digitalWrite(led,1) 

 

        if 'all' in command: 

            message = message + "all " 

            digitalWrite(led,1) 

 

        message = message + "light(s)" 

        telegram_bot.sendMessage (chat_id, message) 

 

 

 

    if 'off' in command: 

        message = "Turned off " 

        if 'led' in command: 

            message = message + "led " 

            digitalWrite(led,0) 

         

        if 'all' in command: 

            message = message + "all " 

            digitalWrite(led,0) 

            

        message = message + "light(s)" 

        telegram_bot.sendMessage (chat_id, message) 

 

telegram_bot = telepot.Bot('6348232837:AAFdpKqwUkxmNnMi1ApBYwO54toVCPn0y6U') #use telegram access key API from telegram app of mobile 

print (telegram_bot.getMe()) 

MessageLoop(telegram_bot, action).run_as_thread() 

print ('Up and Running....') 

 

while 1: 

    time.sleep(10) 

  