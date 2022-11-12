
import os
import numpy as np

from bitarray import bitarray
from PIL import Image
from tqdm import tqdm

from functions import *


"""
hide functions
"""

def hideTextInImage(inputImagePath:str, outputImagePath:str, inputTextPath:str, *, repeat:bool=True, **kwargs_save) -> bool:
	# check types
	if type(inputImagePath) is not str:
		raise TypeError(f"inputImagePath={type(inputImagePath)} must be of type str")
	if type(outputImagePath) is not str:
		raise TypeError(f"outputImagePath={type(outputImagePath)} must be of type str")
	if type(inputTextPath) is not str:
		raise TypeError(f"inputTextPath={type(inputTextPath)} must be of type str")
	if type(repeat) is not bool:
		raise TypeError(f"repeat={type(repeat)} must be of type repeat")
	# load image to array
	inputImage = loadImage(inputImagePath)
	width, height = inputImage.size
	pixels = image2Array(inputImage)
	# setup progress bar
	pbar = tqdm(
		total = width * height,
		desc = "Progress",
		unit = "px",
		unit_scale = True,
		colour = "#ffb900"
	)
	# convert text to bitarray
	bits = file2BitArray(inputTextPath)
	# hide text in image
	bitsLen = len(bits)
	textInd = 0
	BREAK = False
	for y in range(height):
		for x in range(width):
			# break if end of bits reached and repeat is False
			if not repeat and textInd >= bitsLen:
				pbar.total = textInd // 3
				BREAK = True
				break
			# modify least significant bits
			pixel = pixels[y][x]
			r = setBit(bits[textInd % bitsLen], pixel[0]); textInd += 1
			g = setBit(bits[textInd % bitsLen], pixel[1]); textInd += 1
			b = setBit(bits[textInd % bitsLen], pixel[2]); textInd += 1
			pixels[y][x] = (r, g, b)
			pbar.update(1)
		# break if inner loop breaks
		if BREAK:
			break
	# close progress bar
	pbar.close()
	# save array as image
	outputImage = array2Image(pixels)
	error = saveImage(outputImagePath, outputImage, **kwargs_save)
	# return if saving was successful
	return not error

def seekTextInImage(inputImagePath:str, outputTextPath:str) -> bool:
	# check types
	if type(inputImagePath) is not str:
		raise TypeError(f"inputImagePath={type(inputImagePath)} must be of type str")
	if type(outputTextPath) is not str:
		raise TypeError(f"outputTextPath={type(outputTextPath)} must be of type str")
	# load image to array
	inputImage = loadImage(inputImagePath)
	width, height = inputImage.size
	pixels = image2Array(inputImage)
	# setup progress bar
	pbar = tqdm(
		total = width * height,
		desc = "Progress",
		unit = "px",
		unit_scale = True,
		colour = "#ffb900"
	)
	# seek text from image
	bits = bitarray()
	for y in range(height):
		for x in range(width):
			# get least significant bits
			pixel = pixels[y][x]
			bits.append(getBit(pixel[0]))
			bits.append(getBit(pixel[1]))
			bits.append(getBit(pixel[2]))
			pbar.update(1)
	# close progress bar
	pbar.close()
	# save bitarray as text in file
	error = bitArray2File(outputTextPath, bits)
	# return if saving was successful
	return not error
