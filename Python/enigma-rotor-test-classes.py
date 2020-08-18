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

        print(m3)

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
                print (m3)
            if stopAllThreads == True:
                return
            time.sleep(0.01)
    
def main():
    global m3
    global stopAllThreads

    stopAllThreads = False
    
    m3 = Machine("M3", "B", "III", "II", "I", [("A", "B"), ("C", "D")])
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