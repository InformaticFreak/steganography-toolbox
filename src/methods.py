
import os
import numpy as np
from bitarray import bitarray

from PIL import Image

from functions import *


"""
hide functions
"""

def hideTextInImage(inputImagePath:str, outputImagePath:str, inputTextPath:str) -> bool:
	# check types
	if type(inputImagePath) is not str:
		raise TypeError(f"inputImagePath={type(inputImagePath)} must be of type str")
	if type(outputImagePath) is not str:
		raise TypeError(f"outputImagePath={type(outputImagePath)} must be of type str")
	if type(inputTextPath) is not str:
		raise TypeError(f"inputTextPath={type(inputTextPath)} must be of type str")
	# convert text to bitarray
	bits = file2BitArray(inputTextPath)
	# load image to array
	image = loadImage(inputImagePath)
	width, height = image.size
	pixels = image2Array(image=image)
	# hide text in image
	bitsLen = len(bits)
	textInd = 0
	for y in range(height):
		for x in range(width):
			# modify least significant bits
			pixel = pixels[x][y]
			r = setBit(bits[textInd % bitsLen], pixel[0]); textInd += 1
			g = setBit(bits[textInd % bitsLen], pixel[1]); textInd += 1
			b = setBit(bits[textInd % bitsLen], pixel[2]); textInd += 1
			pixels[x][y] = (r, g, b)
	# save image
	saveImage(os.path.abspath("../out.png"), imageArray=pixels, show=True)
	