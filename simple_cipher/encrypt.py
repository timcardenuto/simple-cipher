#! /usr/bin/env python

#------------------------------------------------------------------------------
# MIT License
#
# Copyright (C) 2017  Tim Cardenuto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# For questions contact the originator at timcardenuto@gmail.com
#------------------------------------------------------------------------------

from __future__ import print_function
import numpy as np
import sys
import convert
import lfsr


def encrypt(cleartext):
	# convert ascii characters to decimal 
	decimal_ascii = convert.ASCIIToDecimal(cleartext)
	
	# encrypt word with shift based on 'key' between 1 and 25 shifts
	key = 3
	shifted_decimal = convert.shiftRightDecimalASCII(decimal_ascii,key)

	# convert decimal value to binary
	binary = convert.DecimalASCIIToBinary(shifted_decimal)

	# XOR binary with 4th order polynomial PRN
	fill = [1, 0, 1, 0]
	seq = lfsr.four(fill)
	binary_xor = np.zeros(len(binary), dtype = np.int)
	j=0
	for index, bit in enumerate(binary):
		#print(index)
		binary_xor[index] = (bit ^ seq[j])
		if(j < (len(seq)-1)):
			j = j + 1
		else:
			j = 0

	# convert binary to hex
	encrypted_hex = convert.BinaryToHex(binary_xor)
	# python 2 has stupid L character on each value (for long type)
	if (sys.version_info < (3,0)):
		for index, char in enumerate(encrypted_hex):
			encrypted_hex[index] = encrypted_hex[index][:-1]
	print("Encrypted: ", str(''.join(encrypted_hex)))

	
if __name__ == "__main__":
	#cleartext = 'ROSEBUD'   # should produce 'FA41086EF9153F'
	text = []
	for i in range(1,len(sys.argv)):
		text.append(list(sys.argv[i]))
	cleartext = [item for sublist in text for item in sublist]
	
	print("ClearText: ", cleartext)
	encrypt(cleartext)
