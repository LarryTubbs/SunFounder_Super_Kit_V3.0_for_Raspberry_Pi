
# bit map of the wiring of the two 74HC595 ICs to the dual alpha-numeric display
segmentMap1 = {'H':0b1, 'J':0b10, 'K':0b100, 'G1':0b1000, 'A':0b10000, 'B':0b100000}
segmentMap2 = {'F':0b1, 'E':0b10, 'L':0b100, 'M':0b1000, 'N':0b10000, 'G2': 0b100000, 'D':0b1000000, 'C': 0b10000000}

# a definition of the font for the alpha-numeric display using the wiring map above
# letters
vocabulary = {}
vocabulary['A'] = ( segmentMap1['A'] | segmentMap1['B'] | segmentMap1['G1'], segmentMap2['E'] | segmentMap2['F'] | segmentMap2['C'] | segmentMap2['G2'] )
vocabulary['B'] = ( segmentMap1['A'] | segmentMap1['B'] | segmentMap1['J'] , segmentMap2['C'] | segmentMap2['D'] | segmentMap2['M'] | segmentMap2['G2'] )
vocabulary['C'] = ( segmentMap1['A'] , segmentMap2['E'] | segmentMap2['D'] | segmentMap2['F'] )
vocabulary['D'] = ( segmentMap1['A'] | segmentMap1['B'] | segmentMap1['J'] , segmentMap2['C'] | segmentMap2['D'] | segmentMap2['M'] )
vocabulary['E'] = ( segmentMap1['A'] | segmentMap1['G1'] , segmentMap2['E'] | segmentMap2['D'] | segmentMap2['F'] )
vocabulary['F'] = ( segmentMap1['A'] | segmentMap1['G1'] , segmentMap2['E'] | segmentMap2['F'] )
vocabulary['G'] = ( segmentMap1['A'] , segmentMap2['E'] | segmentMap2['D'] | segmentMap2['F'] | segmentMap2['C'] | segmentMap2['G2'] )
vocabulary['H'] = ( segmentMap1['B'] | segmentMap1['G1'], segmentMap2['E'] | segmentMap2['F'] | segmentMap2['C'] | segmentMap2['G2'] )
vocabulary['I'] = ( segmentMap1['A'] | segmentMap1['J'], segmentMap2['D'] | segmentMap2['M'] )
vocabulary['J'] = ( segmentMap1['B'] , segmentMap2['C'] | segmentMap2['D'] )
vocabulary['K'] = ( segmentMap1['G1'] | segmentMap1['K'] , segmentMap2['F'] | segmentMap2['E'] | segmentMap2['N'] )
# vocabulary['K'] = ( segmentMap1['J'] | segmentMap1['K'] , segmentMap2['M'] | segmentMap2['N'] )
vocabulary['L'] = ( 0, segmentMap2['E'] | segmentMap2['D'] | segmentMap2['F'] )
vocabulary['M'] = ( segmentMap1['H'] | segmentMap1['K'] | segmentMap1['B'] , segmentMap2['F'] | segmentMap2['C'] | segmentMap2['E'] )
vocabulary['N'] = ( segmentMap1['H'] | segmentMap1['B'] , segmentMap2['F'] | segmentMap2['C'] | segmentMap2['E'] | segmentMap2['N'])
vocabulary['O'] = ( segmentMap1['A'] | segmentMap1['B'] , segmentMap2['E'] | segmentMap2['D'] | segmentMap2['F'] | segmentMap2['C'] )
vocabulary['P'] = ( segmentMap1['A'] | segmentMap1['B'] | segmentMap1['G1'], segmentMap2['E'] | segmentMap2['F'] | segmentMap2['G2'] )
vocabulary['Q'] = ( segmentMap1['A'] | segmentMap1['B'] , segmentMap2['E'] | segmentMap2['D'] | segmentMap2['F'] | segmentMap2['C'] | segmentMap2['N'] )
vocabulary['R'] = ( segmentMap1['A'] | segmentMap1['B'] | segmentMap1['G1'], segmentMap2['E'] | segmentMap2['F'] | segmentMap2['G2'] | segmentMap2['N'] )
vocabulary['S'] = ( segmentMap1['A'] | segmentMap1['G1'], segmentMap2['F'] | segmentMap2['G2'] | segmentMap2['C'] | segmentMap2['D'] )
vocabulary['T'] = ( segmentMap1['A'] | segmentMap1['J'], segmentMap2['M'] )
vocabulary['U'] = ( segmentMap1['B'] , segmentMap2['E'] | segmentMap2['D'] | segmentMap2['F'] | segmentMap2['C'] )
vocabulary['V'] = ( segmentMap1['B'] | segmentMap1['H'] , segmentMap2['N'] | segmentMap2['C'] )
vocabulary['W'] = ( segmentMap1['B'], segmentMap2['F'] | segmentMap2['E'] | segmentMap2['L'] | segmentMap2['N'] | segmentMap2['C'] )
vocabulary['X'] = ( segmentMap1['K'] | segmentMap1['H'] , segmentMap2['N'] | segmentMap2['L'] )
vocabulary['Y'] = ( segmentMap1['K'] | segmentMap1['H'] , segmentMap2['M'] )
vocabulary['Z'] = ( segmentMap1['A'] | segmentMap1['K'] , segmentMap2['D'] | segmentMap2['L'] )

# numbers
vocabulary['0'] = ( segmentMap1['A'] | segmentMap1['B'] | segmentMap1['K'] , segmentMap2['E'] | segmentMap2['D'] | segmentMap2['F'] | segmentMap2['C'] | segmentMap2['L'] )
vocabulary['1'] = ( segmentMap1['B'] , segmentMap2['C'] )
vocabulary['2'] = ( segmentMap1['A'] | segmentMap1['B'] | segmentMap1['G1'] , segmentMap2['E'] | segmentMap2['D'] | segmentMap2['G2'] )
vocabulary['3'] = ( segmentMap1['A'] | segmentMap1['B'] , segmentMap2['C'] | segmentMap2['D'] | segmentMap2['G2'] )
vocabulary['4'] = ( segmentMap1['B'] | segmentMap1['G1'], segmentMap2['F'] | segmentMap2['C'] | segmentMap2['G2'] )
vocabulary['5'] = ( segmentMap1['A'] | segmentMap1['G1'], segmentMap2['F'] | segmentMap2['G2'] | segmentMap2['C'] | segmentMap2['D'] )
vocabulary['6'] = ( segmentMap1['A'] | segmentMap1['G1'], segmentMap2['F'] | segmentMap2['G2'] | segmentMap2['C'] | segmentMap2['D'] | segmentMap2['E'] )
vocabulary['7'] = ( segmentMap1['A'] | segmentMap1['K'] , segmentMap2['L'])
vocabulary['8'] = ( segmentMap1['A'] | segmentMap1['B'] |  segmentMap1['G1'], segmentMap2['F'] | segmentMap2['G2'] | segmentMap2['C'] | segmentMap2['D'] | segmentMap2['E'] )
vocabulary['9'] = ( segmentMap1['A'] | segmentMap1['B'] |  segmentMap1['G1'], segmentMap2['F'] | segmentMap2['G2'] | segmentMap2['C'] | segmentMap2['D'] )

