import time
import sys

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Plugboard():
    def __init__(self, SDI, RCLK, SRCLK, in_pins):
        GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)
        self.IN_PINS = in_pins
        for pin in self.IN_PINS:
            GPIO.setup(self.IN_PINS[pin], GPIO.IN, GPIO.PUD_DOWN)    
        self.SDI = SDI
        self.RCLK = RCLK
        self.SRCLK = SRCLK
        self.segmentMap1 = {'Q': 0b10, 'W': 0b100, 'E': 0b1000, 'A': 0b10000, 'S': 0b100000, '0': 0b0}
        self.segmentMap2 = {'0': 0b0}
        self.segmentMap3 = {'0': 0b0}
        self.segmentMap4 = {'0': 0b0}
        self.alphabet = "QWEAS"
        self.clear()
        
    def clear(self):
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

    def retrieve(self):
        pairs = []
        for c in self.alphabet:
            # print(f'Turning on output pin "{c}"')
            self.hc595_shift(self.segmentMap1[c])
            # print('Reading all input pins')
            for pin in self.IN_PINS:
                value = GPIO.input(self.IN_PINS[pin])
                if value == True:
                    pairs.append((c , pin ))
                # print(f"    {pin} = {value}")
        return pairs
        
        
def destroy(plugboard=None):
    if plugboard is not None:
        plugboard.clear()
    GPIO.cleanup()
    sys.exit()
    

def main(pb):    
    while True:
        # show the plugboard mappings
        print(pb.retrieve())
        input('Enter any key to rescan the plugboard, press "CTRL+C" to exit: ')
    destroy(pb)

if __name__ == '__main__':
    in_pins = {"Q": 20, "W": 21, "E": 14, "A": 15, "S": 11}
    pb = Plugboard(26, 12, 16, in_pins)

    try:
        main(pb)
    except KeyboardInterrupt:
        destroy(pb)
    

