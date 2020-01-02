#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from sys import version_info
from . import morsecode as morse

if version_info.major == 3:
	raw_input = input


# Set #17 as buzzer pin
BeepPin = 17

def print_message():
	print ("========================================")
	print ("|                 Beep                 |")
	print ("|    ------------------------------    |")
	print ("|        Buzzer connect to GPIO17      |")
	print ("|                                      |")
	print ("|            Make Buzzer beep          |")
	print ("|                                      |")
	print ("|                            SunFounder|")
	print ("======================================\n")
	print ("Program is running...")
	print ("Please press Ctrl+C to end the program...")
	raw_input ("Press Enter to begin\n")

def setup():
	# Set the GPIO modes to BCM Numbering
	GPIO.setmode(GPIO.BCM)
	# Set LedPin's mode to output, 
	# and initial level to High(3.3v)
	GPIO.setup(BeepPin, GPIO.OUT, initial=GPIO.HIGH)

def dit():
	print (".", end="")
	GPIO.output(BeepPin, GPIO.LOW)
	time.sleep(0.1)
	GPIO.output(BeepPin, GPIO.HIGH)
	time.sleep(0.1)
	
def dah():
	print ("-", end="")
	GPIO.output(BeepPin, GPIO.LOW)
	time.sleep(0.1)
	GPIO.output(BeepPin, GPIO.HIGH)
	time.sleep(0.1)

def main():
	print_message()
	while True:
		msg = input("Enter message to send via morse code: ")
		for c in msg.upper():
			if c == ".":
				dit()
			elif c == "-":
				dah()
			elif c == " ":
				print(c, end='')

def destroy():
	# Turn off buzzer
	GPIO.output(BeepPin, GPIO.HIGH)
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