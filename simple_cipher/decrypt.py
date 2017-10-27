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
import enchant
import re
import sys
import convert
import lfsr


def decrypt(taps, ciphertext):
	#print("Taps being used: ", taps)
	#print("Encryped text: ", ciphertext)

	# convert received hex values to binary
	binary = convert.HexToBinary(ciphertext)
	#print(binary)

	# 'un' XOR the binary with 4th order polynomial PRN
	# SEARCHFOR what is polynomial?
	order = taps[0]
	taps.pop(0)				# remove the first (highest order) tap, the way we do LFSR below you don't XOR that one
	# SEARCHFOR what is initial fill?
	fills = lfsr.generateFills(4)	# set possible fills for LFSR based on polynomial size
	#print(fills)
	# SEARCHFOR which shift position is XOR'd?

	for z in range(fills.shape[0]):
		fill = fills[z,:]
		seq = lfsr.generic(order, taps, fill) # set LFSR based on polynomial size
		#print(seq)
		#seq = lfsr.four(fill)
		binary_unxor = np.zeros(len(binary), dtype = np.int)
		j=0
		for index, bit in enumerate(binary):
			binary_unxor[index] = (bit ^ seq[j])
			if(j < (len(seq)-1)):
				j = j + 1
			else:
				j = 0

		# convert binary to decimal values
		decimal_ascii = convert.BinaryToDecimalASCII(binary_unxor)
		#print(decimal_ascii)

		# check that a majority of the values are actually alphabet letters, if not assume this is not the correct LFSR fill/taps
		nonalphalimit = 0.3  	# Set limit for acceptable percentage of non-alphabetic characters
		# np.where gives an array of index's for values from the original array that meet the test
		numalpha = len(np.where((decimal_ascii > 64) & (decimal_ascii < 91))[0]) + len(np.where((decimal_ascii > 96) & (decimal_ascii < 123))[0])
		if (numalpha < len(decimal_ascii)*(1-nonalphalimit)):
			#print(numalpha, ' < ', len(decimal_ascii)*(1-nonalphalimit))
			continue
		#print(numalpha, ' > ', len(decimal_ascii)*(1-nonalphalimit))

		# undo character shift encryption using 'key' of between 1 and 26 shifts
		# SEARCHFOR what is shift key?
		# SEARCHFOR how do we know when we're done without a human checking?
		alphabetSize = 26		# Set alphabet size based on language (changing languages could likely change all the stuff above)
		for key in range(alphabetSize):
			shifted_decimal = convert.shiftLeftDecimalASCII(decimal_ascii,key)

			# if above is successful, should produce an English word
			decrypted_char = convert.DecimalToASCII(shifted_decimal)

			# If you get some possible words check against dictionary / english grammer ...
			d = enchant.Dict("en_US")
			decrypted_str = ''.join(decrypted_char)
			#decrypted_split = decrypted_str.split(' ')
			temp_split = re.split('[!;@#$%^&*()?., ]',decrypted_str)
			decrypted_split = list(filter(None, temp_split))
			check = False
			for word in decrypted_split:
				#print(word, " = ", d.check(word))
				if (len(word) > 1 and d.check(word)):
					check = True
					print("English word found: ", word)

			if (check):
				print("Possible decrypted msg:  ", ''.join(decrypted_char))
				print("Initial register fill: ",fill)
				print("Alphabet shift key: ", key)
				print('')



if __name__ == "__main__":
	# polynomial = 1 + x + x4
	# initial fill = [1 0 1 0]
	# shift key = 3
	#ciphertext = 'fa41086ef9153f'; # should produce 'ROSEBUD'
	text = []
	for i in range(1,len(sys.argv)):
		text.append(list(sys.argv[i]))
	ciphertext = [item for sublist in text for item in sublist]
	taps = [4, 1, 0]	# TODO create a tap generator function based on highest order

	print('')
	print("CipherText: ", ciphertext)
	decrypt(taps, ciphertext)
