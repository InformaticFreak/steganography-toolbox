
import os, sys, re, time, math
import tqdm, pick
import numpy as np
import bitarray

from PIL import Image
from colorama import Fore, Back, Style
from colorama import init as coloramaInit
from os.path import join as joinPath

from functions import *


def main(*args):
	bitsIn = 255
	bitsOut = setBit(False, bitsIn, pos=1, bigEndian=True)
	print(f"{bitsIn=:b} {bitsOut=:b}")

	bitsGet = getBit(bitsOut, pos=1, bigEndian=True)
	print(f"{bitsGet=:b}")

if __name__ == "__main__":
	main(*sys.argv[1:])

