
import os
import numpy as np

from bitarray import bitarray
from PIL import Image
from tqdm import tqdm

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
	inputImage = loadImage(inputImagePath)
	width, height = inputImage.size
	pixels = image2Array(inputImage)
	# hide text in image
	bitsLen = len(bits)
	textInd = 0
	for y in range(height):
		for x in range(width):
			# modify least significant bits
			pixel = pixels[y][x]
			r = setBit(bits[textInd % bitsLen], pixel[0]); textInd += 1
			g = setBit(bits[textInd % bitsLen], pixel[1]); textInd += 1
			b = setBit(bits[textInd % bitsLen], pixel[2]); textInd += 1
			pixels[y][x] = (r, g, b)
	# save image from array
	outputImage = array2Image(pixels)
	saveImage(outputImagePath, outputImage, show=True)
	