import time, datetime 

import RPi.GPIO as GPIO 

import telepot 

from telepot.loop import MessageLoop 

led1 = 17 

led2 = 27 

led3 = 22 

buzzer = 23 

now = datetime.datetime.now() 

GPIO.setmode(GPIO.BCM) 

GPIO.setwarnings(False) 

#MYLED 

GPIO.setup(led1, GPIO.OUT) 

GPIO.output(led1, 0) #Off initially 

GPIO.setup(led2, GPIO.OUT) 

GPIO.output(led2, 0) #Off initially 

GPIO.setup(led3, GPIO.OUT) 

GPIO.output(led3, 0) #Off initially 

GPIO.setup(buzzer, GPIO.OUT) 

GPIO.output(buzzer, 0) #Off initially 

 

def action(msg): 

   chat_id = msg['chat']['id'] 

   command = msg['text'] 

   print ('Received: %s' % command) 

   if 'on' in command: 

       message = "Turned on " 

       if 'led1' in command: 

           message = message + "led1 " 

           GPIO.output(led1, 1) 

 

       if 'led2' in command: 

           message = message + "led2 " 

           GPIO.output(led2, 1) 

 

       if 'led3' in command: 

           message = message + "led3 " 

           GPIO.output(led3, 1) 

       if 'buzzer' in command: 

           message = message + "buzzer " 

           GPIO.output(buzzer, 1) 

 

       if 'all' in command: 

           message = message + "all " 

           GPIO.output(led1, 1) 

           GPIO.output(led2, 1) 

           GPIO.output(led3, 1) 

           GPIO.output(buzzer, 1) 

       message = message + "light(s)" 

       telegram_bot.sendMessage (chat_id, message) 

 

   if 'off' in command: 

       message = "Turned off " 

       if 'led1' in command: 

           message = message + "led1 " 

           GPIO.output(led1, 0) 

       if 'led2' in command: 

           message = message + "led2 " 

           GPIO.output(led2, 0) 

       if 'led3' in command: 

           message = message + "led3 " 

           GPIO.output(led3, 0) 

       if 'buzzer' in command: 

           message = message + "buzzer " 

 

           GPIO.output(buzzer, 0) 

       if 'all' in command: 

           message = message + "all " 

           GPIO.output(led1, 0) 

           GPIO.output(led2, 0) 

           GPIO.output(led3, 0) 

           GPIO.output(buzzer, 0) 

       message = message + "light(s)" 

       telegram_bot.sendMessage (chat_id, message) 

 

telegram_bot = telepot.Bot('6565701289:AAF-zmPrM5GYC3I-4GtmshVMfVPizCyZ6vA') 

print (telegram_bot.getMe()) 

MessageLoop(telegram_bot, action).run_as_thread() 

print ('Code Unnati Home automation is Up and Running....') 

 

while 1: 

   time.sleep(10) 

