#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from sys import version_info

if version_info.major == 3:
    raw_input = input

# Set up pins
SDI   = 23
RCLK  = 24
SRCLK = 25

# Define a segment code from 0 to F in Hexadecimal
# Commen cathode
segCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71]
numCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
# Commen anode
# segCode = [0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0x88,0x83,0xc6,0xa1,0x86,0x8e]

def print_msg():
    print ("========================================")
    print ("|         Segment with 74HC595         |")
    print ("|    ------------------------------    |")
    print ("|         SDI connect to GPIO23        |")
    print ("|         RCLK connect to GPIO24       |")
    print ("|        SRCLK connect to GPIO25       |")
    print ("|                                      |")
    print ("|     Control segment with 74HC595     |")
    print ("|                                      |")
    print ("|                            SunFounder|")
    print ("========================================")
    print ("Program is running...")
    print ("Please press Ctrl+C to end the program..")
    raw_input ("Press Enter to begin\n")

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)

# Shift the data to 74HC595
def hc595_shift(dat):
    for bit in range(0, 8):	
        GPIO.output(SDI, 0x80 & (dat << bit)) # send one bit at a time
        GPIO.output(SRCLK, GPIO.HIGH) # high part of hi-low pair to signal the IC to store current bit to shift register
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW) # low part of hi-low pair to signal the IC to store current bit to shift register
    GPIO.output(RCLK, GPIO.HIGH) # high part of hi-low pair to signal the IC to shift the data from the shift register to the data register
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW) # low part of the hi-low pair.  Results in the value being displayed on the segment display

def sendNumToDisplay(i):
    if i in range(0, 100):
        if i <= 9:
            hc595_shift(numCode[i])
            hc595_shift(0x0)
        else:
            hc595_shift(numCode[int(i%10)])
            hc595_shift(numCode[int(i/10)])
    else:
        # error occurred
        hc595_shift(0x79)
        hc595_shift(0x79)
        raise ValueError('Not a whole number between 0-99')


def main():
    print_msg()
    while True:
        iStr = input("Please enter a whole number from 0-99: ")
        try:
            i = int(iStr)
            sendNumToDisplay(i)
        except ValueError as e:
            print("'" + iStr + "' isn't a whole number from 0-99.  Please try again.")

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()
