import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Display():
    def __init__(self, SDI, RCLK, SRCLK, LCO, RCO):
        GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(LCO, GPIO.OUT, initial=GPIO.HIGH )
        GPIO.setup(RCO, GPIO.OUT, initial=GPIO.HIGH)
        self.SDI = SDI
        self.RCLK = RCLK
        self.SRCLK = SRCLK
        self.LCO = LCO
        self.RCO = RCO
        self.segmentMap1 = {'F':0b1, 'E':0b10, 'L':0b100, 'M':0b1000, 'N':0b10000, 'G2': 0b100000, 'D':0b1000000, 'C': 0b10000000}
        self.segmentMap2 = {'H':0b1, 'J':0b10, 'K':0b100, 'G1':0b1000, 'A':0b10000, 'B':0b100000}
    
    def hc595_shift(self, dat):
        for bit in range(0, 8):	
            GPIO.output(self.SDI, 0x80 & (dat << bit)) # send one bit at a time
            GPIO.output(self.SRCLK, GPIO.HIGH) # high part of hi-low pair to signal the IC to store current bit to shift register
            time.sleep(0.001)
            GPIO.output(self.SRCLK, GPIO.LOW) # low part of hi-low pair to signal the IC to store current bit to shift register
        GPIO.output(self.RCLK, GPIO.HIGH) # high part of hi-low pair to signal the IC to shift the data from the shift register to the data register
        time.sleep(0.001)
        GPIO.output(self.RCLK, GPIO.LOW) # low part of the hi-low pair.  Results in the value being displayed on the segment display

    def show(self):
        # if i in range(0, 100):
        #     if i <= 9:
        #         self.hc595_shift(self.numCode[i])
        #         self.hc595_shift(0x0)
        #     else:
        #         self.hc595_shift(self.numCode[int(i%10)])
        #         self.hc595_shift(self.numCode[int(i/10)])
        # else:
        #     # error occurred
        #     self.hc595_shift(0x79)
        #     self.hc595_shift(0x79)
        #     raise ValueError('Not a whole number between 0-99')
        self.hc595_shift(0b1000000)
        self.hc595_shift(0b0)
        GPIO.output(self.RCO, GPIO.LOW) # closes circuit, access to ground for the right digit
        GPIO.output(self.LCO, GPIO.LOW)
    
    def clear(self):
        # self.hc595_shift(0x0)
        # self.hc595_shift(0x0)
        GPIO.output(self.RCO, GPIO.HIGH) # breaks circuit, no ground for the right digit.
        GPIO.output(self.LCO, GPIO.HIGH)

d = Display(23, 24, 25, 4, 5)
d.show()
s = input("Press 'enter' key to end.")
GPIO.cleanup()
