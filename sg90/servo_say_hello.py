#!/usr/bin/env python3.8

import RPi.GPIO as GPIO
from time import sleep
import subprocess
import sys


#Configurações iniciais do Servo
servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setwarnings(False)
p = GPIO.PWM(servoPIN, 50)
p.start(2.5)

p.ChangeDutyCycle(12)
sleep(2)
p.ChangeDutyCycle(2.5)
sleep(2)
p.ChangeDutyCycle(12)

p.stop()
GPIO.cleanup()