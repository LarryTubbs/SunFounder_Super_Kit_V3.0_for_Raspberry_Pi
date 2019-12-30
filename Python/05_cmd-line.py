import sys

for (i, value) in enumerate(sys.argv):
        if i > 0:
            x = int(value, 16)
            print("arg: %d %s " % (i, hex(x)))

