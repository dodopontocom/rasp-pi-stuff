#!/usr/bin/env python3.8

#https://www.digikey.com/en/maker/blogs/2021/how-to-control-servo-motors-with-a-raspberry-pi
#https://gist.github.com/LeonardoGentile/7a5330e6bc55860feee5d0dd79e7965d
#https://github.com/dodopontocom/diario_itatiba_robo/blob/44594b8a93497f9797781c74959ad1ab75fc3b9a/scripts/functions.sh

from gpiozero import Servo
from time import sleep
import subprocess
import sys


if len(sys.argv) > 1:
    high = float(sys.argv[1])
    print(high)
else:
    high = 60
    too_high = 80

subprocess.getoutput('notify-send "Starting Temperature Program!!!"')

servo = Servo(17)

try:
    while (float(subprocess.getoutput('vcgencmd measure_temp | sed "s/[^0-9.]//g"')) >= high):
        print("Current temperature: " + subprocess.getoutput('vcgencmd measure_temp | sed "s/[^0-9.]//g"'))
        #message = subprocess.getoutput('vcgencmd measure_temp | sed "s/[^0-9.]//g"')
        subprocess.getoutput('curl -s -X POST https://api.telegram.org/bot407633103:AAGpijjc8Vo7ScaGPda20DmDnlN0CRBPmek/sendMessage -d chat_id=11504381 -d text="Temperature is very High!!!"')
        subprocess.getoutput('notify-send "Temperature is very High!!!"')
        servo.min()
        sleep(0.5)
        servo.max()
        sleep(0.5)
except KeyboardInterrupt:
    servo.close()
    print("\nProgram stopped!")

if(float(subprocess.getoutput('vcgencmd measure_temp | sed "s/[^0-9.]//g"')) < high):
    print("Temperature is OK!!!")
    subprocess.getoutput('curl -s -X POST https://api.telegram.org/bot407633103:AAGpijjc8Vo7ScaGPda20DmDnlN0CRBPmek/sendMessage -d chat_id=11504381 -d text="Temperature is OK !!!"')
    #servo.min()
    #sleep(5)
    #servo.max()
    #sleep(5)

    servo.close()
    print("\nClosing Program!")

#servo.value = -1
#servo.value = 0
#servo.value = 1
