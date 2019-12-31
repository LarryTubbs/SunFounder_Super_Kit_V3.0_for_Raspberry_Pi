#!/usr/bin/env python3

# imports
from sys import version_info
import time

if version_info.major == 3:
	raw_input = input

def setup():
    print('setting up')

def main():
    print('in main')
    while True:
        time.sleep(1)

def destroy():
    print('cleaning up')

# If run this script directly, do:
if __name__ == '__main__':
	setup()
	try:
		main()
	# When 'Ctrl+C' is pressed, the child program 
	# destroy() will be  executed.
	except KeyboardInterrupt:
		destroy()
