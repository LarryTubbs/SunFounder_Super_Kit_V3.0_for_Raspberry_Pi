import time

import RPi.GPIO as GPIO
import font

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
        
    def hc595_shift(self, dat):
        for bit in range(0, 8):	
            GPIO.output(self.SDI, 0x80 & (dat << bit)) # send one bit at a time
            GPIO.output(self.SRCLK, GPIO.HIGH) # high part of hi-low pair to signal the IC to store current bit to shift register
            time.sleep(0.001)
            GPIO.output(self.SRCLK, GPIO.LOW) # low part of hi-low pair to signal the IC to store current bit to shift register
        GPIO.output(self.RCLK, GPIO.HIGH) # high part of hi-low pair to signal the IC to shift the data from the shift register to the data register
        time.sleep(0.001)
        GPIO.output(self.RCLK, GPIO.LOW) # low part of the hi-low pair.  Results in the value being displayed on the segment display

    def show(self, c):
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
        self.hc595_shift(font.vocabulary[c][0])
        self.hc595_shift(font.vocabulary[c][1])
        GPIO.output(self.RCO, GPIO.LOW) # closes circuit, access to ground for the right digit
        # GPIO.output(self.LCO, GPIO.LOW)
    
    def clear(self):
        # self.hc595_shift(0x0)
        # self.hc595_shift(0x0)
        GPIO.output(self.RCO, GPIO.HIGH) # breaks circuit, no ground for the right digit.
        # GPIO.output(self.LCO, GPIO.HIGH)

def destroy():
	GPIO.cleanup()

def main():
    d = Display(23, 24, 25, 4, 5)
    while True:
        s = input("Please type a letter to display and press 'enter: ")
        try:
            d.show(s.upper())
        except:
            print("I don't know how to display '" + s + "'.  Please try another letter.")
    

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		destroy()
    
