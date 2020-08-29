import threading
import time
import sys

import RPi.GPIO as GPIO

from enigma.machine import Machine
import enigma.globe

import font

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

class Rotary(threading.Thread):
    def __init__(self, RoAPin, RoBPin):
        threading.Thread.__init__(self)
        self.RoAPin = RoAPin
        self.RoBPin = RoBPin
        
        GPIO.setup(self.RoAPin, GPIO.IN)
        GPIO.setup(self.RoBPin, GPIO.IN)
        self.deamon = True
        self.start()

    def run(self):
        global m3
        global stopAllThreads
        global display

        print(m3)
        display.show(enigma.globe.plaintext[m3.r.position])

        while True:
            Last_RoB_Status = 0
            Current_RoB_Status = 0

            flag = 0
            Last_RoB_Status = GPIO.input(self.RoBPin)
            # When RoAPin level changes
            while(not GPIO.input(self.RoAPin)):
                Current_RoB_Status = GPIO.input(self.RoBPin)
                flag = 1
            if flag == 1:
                # Reset flag
                flag = 0
                if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
                    m3.r.rotateUp()
                if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
                    m3.r.rotateDown()
                display.show(enigma.globe.plaintext[m3.r.position])
                print (m3)
            if stopAllThreads == True:
                return
            time.sleep(0.005)

# class Display():
### For numeric displays (pair of 7 segments - refactored out to 14 segment alpha-numerics)
#     def __init__(self, SDI, RCLK, SRCLK):
#         GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)
#         GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)
#         GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)
#         self.SDI = SDI
#         self.RCLK = RCLK
#         self.SRCLK = SRCLK
#         self.numCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
    
#     def hc595_shift(self, dat):
#         for bit in range(0, 8):	
#             GPIO.output(self.SDI, 0x80 & (dat << bit)) # send one bit at a time
#             GPIO.output(self.SRCLK, GPIO.HIGH) # high part of hi-low pair to signal the IC to store current bit to shift register
#             time.sleep(0.001)
#             GPIO.output(self.SRCLK, GPIO.LOW) # low part of hi-low pair to signal the IC to store current bit to shift register
#         GPIO.output(self.RCLK, GPIO.HIGH) # high part of hi-low pair to signal the IC to shift the data from the shift register to the data register
#         time.sleep(0.001)
#         GPIO.output(self.RCLK, GPIO.LOW) # low part of the hi-low pair.  Results in the value being displayed on the segment display

#     def show(self, i):
#         if i in range(0, 100):
#             if i <= 9:
#                 self.hc595_shift(self.numCode[i])
#                 self.hc595_shift(0x0)
#             else:
#                 self.hc595_shift(self.numCode[int(i%10)])
#                 self.hc595_shift(self.numCode[int(i/10)])
#         else:
#             # error occurred
#             self.hc595_shift(0x79)
#             self.hc595_shift(0x79)
#             raise ValueError('Not a whole number between 0-99')
    
#     def clear(self):
#         self.hc595_shift(0x0)
#         self.hc595_shift(0x0)

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
        self.hc595_shift(font.vocabulary[c][0])
        self.hc595_shift(font.vocabulary[c][1])
        GPIO.output(self.RCO, GPIO.LOW) # closes circuit, access to ground for the right digit
        # GPIO.output(self.LCO, GPIO.LOW)
    
    def clear(self):
        GPIO.output(self.RCO, GPIO.HIGH) # breaks circuit, no ground for the right digit.
        GPIO.output(self.LCO, GPIO.HIGH)

def main(lb):
    global m3
    global stopAllThreads
    global display

    stopAllThreads = False
    
    m3 = Machine("M3", "B", "III", "II", "I", [("A", "B"), ("C", "D")])
    display = Display(23, 24, 25, 4, 5)
    rotary = Rotary(17, 18)
    while True:
        name = input('Enter text to encode.  Enter "-" to quit.')

        if name.upper() == ('-'):
            stopAllThreads = True
            rotary.join() 
            display.clear()
            destroy(lb)
            sys.exit()
        
        for c in name:
            cypherText = m3.evaluate(c)
            display.show(enigma.globe.plaintext[m3.r.position])
            lb.show(cypherText)
            print(cypherText)
            time.sleep(0.5)
        lb.clear()
        print(m3)


def destroy(lb=None):
    # clear the lampboard
    if lb is not None:
        lb.clear()
        
    # Release resource
    GPIO.cleanup()  

# If run this script directly, do:
if __name__ == '__main__':
    lb = Lampboard(6, 13, 19)

    try:
        main(lb)
    # When 'Ctrl+C' is pressed, the child program 
    # destroy() will be  executed.
    except KeyboardInterrupt:
        destroy(lb)