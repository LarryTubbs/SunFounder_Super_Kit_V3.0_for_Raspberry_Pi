import threading
import time
import sys

import RPi.GPIO as GPIO

from enigma.machine import Machine

GPIO.setmode(GPIO.BCM)

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
        display.show(m3.r.position)

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
                display.show(m3.r.position)
                print (m3)
            if stopAllThreads == True:
                return
            time.sleep(0.01)

class Display():
    def __init__(self, SDI, RCLK, SRCLK):
        GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)
        self.SDI = SDI
        self.RCLK = RCLK
        self.SRCLK = SRCLK
        self.numCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
    
    def hc595_shift(self, dat):
        for bit in range(0, 8):	
            GPIO.output(self.SDI, 0x80 & (dat << bit)) # send one bit at a time
            GPIO.output(self.SRCLK, GPIO.HIGH) # high part of hi-low pair to signal the IC to store current bit to shift register
            time.sleep(0.001)
            GPIO.output(self.SRCLK, GPIO.LOW) # low part of hi-low pair to signal the IC to store current bit to shift register
        GPIO.output(self.RCLK, GPIO.HIGH) # high part of hi-low pair to signal the IC to shift the data from the shift register to the data register
        time.sleep(0.001)
        GPIO.output(self.RCLK, GPIO.LOW) # low part of the hi-low pair.  Results in the value being displayed on the segment display

    def show(self, i):
        if i in range(0, 100):
            if i <= 9:
                self.hc595_shift(self.numCode[i])
                self.hc595_shift(0x0)
            else:
                self.hc595_shift(self.numCode[int(i%10)])
                self.hc595_shift(self.numCode[int(i/10)])
        else:
            # error occurred
            self.hc595_shift(0x79)
            self.hc595_shift(0x79)
            raise ValueError('Not a whole number between 0-99')
    
def main():
    global m3
    global stopAllThreads
    global display

    stopAllThreads = False
    
    m3 = Machine("M3", "B", "III", "II", "I", [("A", "B"), ("C", "D")])
    display = Display(23, 24, 25)
    rotary = Rotary(17, 18)
    while True:
        name = input('Enter "Q" to quit.')

        if name.upper() == ('Q'):
            stopAllThreads = True
            rotary.join() 
            destroy()
            sys.exit()


def destroy():
    # Release resource
    GPIO.cleanup()  

# If run this script directly, do:
if __name__ == '__main__':
    try:
        main()
    # When 'Ctrl+C' is pressed, the child program 
    # destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()