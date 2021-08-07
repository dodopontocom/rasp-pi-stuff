#!/usr/bin/env python3.8

from gpiozero import AngularServo
s = AngularServo(14, min_angle=-42, max_angle=44)
s.angle = 0.0
print(s.angle)
s.angle = 15
print(s.angle)

s.value = 15
