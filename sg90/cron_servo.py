#!/usr/bin/env python3.8

#https://www.digikey.com/en/maker/blogs/2021/how-to-control-servo-motors-with-a-raspberry-pi
#https://gist.github.com/LeonardoGentile/7a5330e6bc55860feee5d0dd79e7965d
#https://github.com/dodopontocom/diario_itatiba_robo/blob/44594b8a93497f9797781c74959ad1ab75fc3b9a/scripts/functions.sh

from gpiozero import Servo
from time import sleep
import subprocess
import sys

if len(sys.argv) > 3:
    high = float(sys.argv[1])
    telegram_token = str(sys.argv[2])
    telegram_id = str(sys.argv[3])
else:
    print("\n\nok, sayonnara\n\n")
    exit()

telegram_url = "https://api.telegram.org/bot{}/sendMessage -d chat_id={} -d text=".format(telegram_token, telegram_id)
servo = Servo(18)
servo.max()
sleep(2)

try:
    while True:
        temp = float(subprocess.getoutput('vcgencmd measure_temp | sed "s/[^0-9.]//g"'))
        if ( temp >= high):
            message = "(Attention) Temperature = "
            message += str(temp)
            subprocess.getoutput('curl -s -X POST {}"{}"'.format(telegram_url, message))
            subprocess.getoutput('notify-send "{}"'.format(message))
            servo.min()
            sleep(0.5)
            servo.max()
            sleep(0.5)
    
        #elif(temp < high):
        #    message = "Temperature = "
        #    message += str(temp)
        #    subprocess.getoutput('curl -s -X POST {}"{}"'.format(telegram_url, message))
        #    subprocess.getoutput('notify-send "{}"'.format(message))
        #    servo.min()
        #    sleep(5)
        #    servo.max()
        #    sleep(5)
        #    #servo.close()
except KeyboardInterrupt:
    print("\n\nok, sayonnara\n\n")
    servo.min()
    servo.close()