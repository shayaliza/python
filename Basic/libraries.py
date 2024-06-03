import math

math.floor(4.6) #towards negative infinity
math.trunc(4.6) #towards zero

2+1j #complex number

(2+1j) * 3 #check the result of this comples number
0o20 #octal literal number base to the 10
0xFF #hex number base to the 10
0b1010 #binary literals number base to the 10

oct(64)
hex(64)
bin(64)

int('64', 8) #converts to octal 
int('64', 2) #converts to binary 

x = 1
x << 2 #left shift by 2 bits

import random
random.random()
random.randint(1, 10) #btw 1 and 10
random.choice([1, 2, 3, 4, 5])
random.shuffle([1, 2, 3, 4, 5])

import os
os.getcwd()
os.chdir('C:\\')
os.listdir()
os.mkdir('spam')
os.rmdir('spam')

import sys
sys.path
sys.argv

import time
time.time()

import datetime
datetime.datetime.now()

0.1 + 0.1 + 0.1 - 0.3

from decimal import Decimal
Decimal('0.1') + Decimal('0.1') + Decimal('0.1') - Decimal('0.3')

from fractions import Fraction
Fraction('0.1') + Fraction('0.1') + Fraction('0.1') - Fraction('0.3')

setone = {1, 2, 3, 4, 5}
settwo = {4, 5, 6, 7, 8}
setone | settwo #union
setone & settwo #intersection
setone - settwo #difference
setone ^ settwo #symmetric difference 

True is 1 #check in memory if the space is same