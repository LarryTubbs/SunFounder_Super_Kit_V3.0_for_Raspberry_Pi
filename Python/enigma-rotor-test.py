#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from sys import version_info

from enigma.machine import Machine

if version_info.major == 3:
	raw_input = input

# Set up pins
# Rotary A Pin
RoAPin = 17
# Rotary B Pin
RoBPin = 18
# Rotary Switch Pin
RoSPin = 27

def print_message():
	global m3
	print ("Program is running...")
	print ("Please press Ctrl+C to end the program...")
	raw_input ("Press Enter to begin\n")
	print(m3)
	

def setup():
	global m3
	global Last_RoB_Status, Current_RoB_Status
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RoAPin, GPIO.IN)
	GPIO.setup(RoBPin, GPIO.IN)
	GPIO.setup(RoSPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
	# Set up a falling edge detect to callback clear
	GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear)

	# Set up a m3 enigma machine as a global variable
	Last_RoB_Status = 0
	Current_RoB_Status = 0
	m3 = Machine("M3", "B", "III", "II", "I", [("A", "B"), ("C", "D")])
	

# Define a function to deal with rotary encoder
def rotaryDeal():
	global m3
	global Last_RoB_Status, Current_RoB_Status

	flag = 0
	Last_RoB_Status = GPIO.input(RoBPin)
	# When RoAPin level changes
	while(not GPIO.input(RoAPin)):
		Current_RoB_Status = GPIO.input(RoBPin)
		flag = 1
	if flag == 1:
		# Reset flag
		flag = 0
		if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
			m3.r.rotateUp()
		if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
			m3.r.rotateDown()
		print (m3)

# Define a callback function on switch, to clean "counter"
def clear(ev=None):
	global m3
	m3.r.position = 1
	print(m3)

def main():
	print_message()
	while True:
		rotaryDeal()

def destroy():
	# Release resource
	GPIO.cleanup()  

# If run this script directly, do:
if __name__ == '__main__':
	setup()
	try:
		main()
	# When 'Ctrl+C' is pressed, the child program 
	# destroy() will be  executed.
	except KeyboardInterrupt:
		destroy()