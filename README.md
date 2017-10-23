# simple-cipher

Python module with very basic encipher/decipher function based on a 4th order Linear Feedback Shift Register (LFSR). This is a toy example for research purposes, do NOT use this to actually encrypt data, it is not secure whatsoever. 

To install with pip:

    $ git clone https://github.com/timcardenuto/simple-cipher
    $ cd simple-cipher
    $ pip install .

To encrypt a message:

    $ python
    >>> import simple_cipher as sc
    >>> sc.encrypt.encrypt('Hello World!')
    Encrypted:  e47b3149ce6e22e8845a854f

To decrypt a message:

    $ python
    >>> import simple_cipher as sc
    >>> sc.decrypt.decrypt('e47b3149ce6e22e8845a854f')
    Hello  = True
    World  = True

    Possible decrypted msg:   Hello World!
    Initial register fill:  [1 0 1 0]
    Alphabet shift key:  3

You'll see printouts like above for possible words - this is because the decrypt function does not assume knowledge of the initial LFSR fill or alphabetic shift key (see Ceasar Cipher to understand how that works). It attempts a brute force try for each fill and uses the enchant dictionary to check different split strings for English words. If it sees valid words, it will report a possible solution. Obviously a human would have to validate the results at some point, but this helps knock down the number of outputs you have to check.

You can also run it directly without installing like this:

    $ cd simple-cipher/simple_cipher
    $ python encrypt.py "Hello World!"
    Encrypted:  e47b3149ce6e22e8845a854f
    
    $ python decrypt.py e47b3149ce6e22e8845a854f
    Hello  = True
    World  = True

    Possible decrypted msg:   Hello World!
    Initial register fill:  [1 0 1 0]
    Alphabet shift key:  3
