import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Lampboard():
    def __init__(self, SDI, RCLK, SRCLK):
        GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)
        self.SDI = SDI
        self.RCLK = RCLK
        self.SRCLK = SRCLK
        self.segmentMap1 = {'W': 0b1, 'Q': 0b10, 'E': 0b100, 'R': 0b1000, 'T': 0b10000, 'Z': 0b100000, 'U': 0b1000000, 'I': 0b10000000, '0': 0b0}
        self.segmentMap2 = {'O': 0b1, 'A': 0b10, 'S': 0b100, 'D': 0b1000, 'F': 0b10000, 'G': 0b100000, 'H': 0b1000000, 'J': 0b10000000, '0': 0b0}
        self.segmentMap3 = {'K': 0b1, 'P': 0b10, 'Y': 0b100, 'X': 0b1000, 'C': 0b10000, 'V': 0b100000, 'B': 0b1000000, 'N': 0b10000000, '0': 0b0}
        self.segmentMap4 = {'M': 0b1, 'L': 0b10, '0': 0b0}
        self.clear()
        
    def clear(self):
        self.hc595_shift(self.segmentMap4['0'])
        self.hc595_shift(self.segmentMap3['0'])
        self.hc595_shift(self.segmentMap2['0'])
        self.hc595_shift(self.segmentMap1['0'])
    
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
        c = c.upper()
        if c in self.segmentMap4:
            self.hc595_shift(self.segmentMap4[c])
        else:
            self.hc595_shift(self.segmentMap4['0'])
        if c in self.segmentMap3:
            self.hc595_shift(self.segmentMap3[c])
        else:
            self.hc595_shift(self.segmentMap3['0'])
        if c in self.segmentMap2:
            self.hc595_shift(self.segmentMap2[c])
        else:
            self.hc595_shift(self.segmentMap2['0'])
        if c in self.segmentMap1:
            self.hc595_shift(self.segmentMap1[c])
        else:
            self.hc595_shift(self.segmentMap1['0'])
        
def destroy(lampboard=None):
    if lampboard is not None:
        lampboard.clear()
    GPIO.cleanup()
    

def main(lb):    
    while True:
        c = input('Please enter a character to display on the lampboard: ')
        lb.show(c)
    destroy(lb)

if __name__ == '__main__':
    lb = Lampboard(6, 13, 19)

    try:
        main(lb)
    except KeyboardInterrupt:
        destroy(lb)
    

