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

import numpy as np
import sys


def four(fill):

	if (len(fill) != 4):
		print("Error: this LFSR only accepts 4 bit fills")
		sys.exit(1)

	L = 4;          	# num of bits, or shift registers
	N = pow(2,L) - 1;	# num of codes, also sequence repeat length in bits

	# chipping sequence comes out the lefts side of LFSR (zero bit)
	seq = np.zeros((N), dtype = np.int)
	
	# loop (aka clock) for one sequence length
	for i in range(N):
		seq[i] = fill[0]

		# 1 + x3 + x4
		#newfill = [fill[1], fill[2], fill[3], (fill[3] ^ fill[0])]

		# 1 + x + x4
		newfill = [fill[1], fill[2], fill[3], (fill[1] ^ fill[0])]
		
		fill = newfill
		
	return seq


if __name__ == "__main__":
	binary = list(map(int,sys.argv[1]))
	print('')
	print('Input:  ',binary)
	print('Output: ',four(binary))