#!/usr/bin/env python

'''
Control a LED from Raspberry Pi
Refer to led-blink.png for circuit
Author: Sudar - http://hardwarefun.com
License: BEERWARE ;)
'''
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

try:
	while True:
		GPIO.output(11, GPIO.HIGH)
		time.sleep(3)
		GPIO.output(11, GPIO.LOW)
		time.sleep(1)
finally:
    GPIO.cleanup()
