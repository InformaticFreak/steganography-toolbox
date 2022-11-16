
import os
import numpy as np

from bitarray import bitarray
from PIL import Image
from tqdm import tqdm

from functions import *


"""
hide functions
"""

def hideFileInImage(inputImagePath:str, outputImagePath:str, inputFilePath:str, *, repeat:bool=True, bitPattern:list[int]=["least"], colorPattern:list[int]=["r","g","b"], **kwargs_save) -> bool:
	# check types
	if type(inputImagePath) is not str:
		raise TypeError(f"inputImagePath={type(inputImagePath)} must be of type str")
	if type(outputImagePath) is not str:
		raise TypeError(f"outputImagePath={type(outputImagePath)} must be of type str")
	if type(inputFilePath) is not str:
		raise TypeError(f"inputFilePath={type(inputFilePath)} must be of type str")
	if type(repeat) is not bool:
		raise TypeError(f"repeat={type(repeat)} must be of type bool")
	if type(bitPattern) not in (list, tuple):
		raise TypeError(f"bitPattern={type(bitPattern)} must be of type list")
	if type(colorPattern) not in (list, tuple):
		raise TypeError(f"colorPattern={type(colorPattern)} must be of type list")
	# check values
	if len(bitPattern) < 1:
		raise ValueError(f"{bitPattern=} must contain at least one element")
	if len(colorPattern) < 1:
		raise ValueError(f"{colorPattern=} must contain at least one element")
	# check inner types
	for ind, el in enumerate(bitPattern):
		if type(el) not in (int, str):
			raise ValueError(f"bitPattern[{ind}]={type(bitPattern[ind])} must be of type int or a specific str")
	for ind, el in enumerate(colorPattern):
		if type(el) not in (int, str):
			raise ValueError(f"colorPattern[{ind}]={type(colorPattern[ind])} must be of type int or a specific str")
	# load image to array
	inputImage = loadImage(inputImagePath)
	width, height = inputImage.size
	pixels = image2Array(inputImage)
	# convert file to bitarray
	bits = file2BitArray(inputFilePath)
	# setup progress bar
	pbar = tqdm(
		total = width * height,
		unit = "px",
		desc = "Progress",
		unit_scale = True,
		colour = "#ffb900"
	)
	pbarUpdate = lambda x=1: pbar.update(x)
	# get bits lenght
	bitsLen = len(bits)
	bitsInd = 0
	# get patterns lenght
	bitPatternLen = len(bitPattern)
	colorPatternLen = len(colorPattern)
	# hide file in input image
	BREAK = False
	for y in range(height):
		for x in range(width):
			# break if end of bits reached and repeat is False
			if not repeat and bitsInd >= bitsLen:
				pbar.total = bitsInd // 3
				BREAK = True
				break
			# modify bits
			pixel = pixels[y][x]
			r = setBit(bits[bitsInd % bitsLen], pixel[0], pos=bitPattern[bitsInd % bitPatternLen]); bitsInd += 1
			g = setBit(bits[bitsInd % bitsLen], pixel[1], pos=bitPattern[bitsInd % bitPatternLen]); bitsInd += 1
			b = setBit(bits[bitsInd % bitsLen], pixel[2], pos=bitPattern[bitsInd % bitPatternLen]); bitsInd += 1
			pixels[y][x] = (r, g, b)
			# update counters
			pbarUpdate()
		# break if inner loop breaks
		if BREAK:
			break
	# close progress bar
	pbar.colour = "#8ce10b"
	pbar.close()
	# save image
	outputImage = array2Image(pixels)
	error = saveImage(outputImagePath, outputImage, **kwargs_save)
	# return if saving was successful
	return not error

"""
seek functions
"""

def seekFileInImage(inputImagePath:str, outputFilePath:str, *, bitPattern:list[int]=["least"], colorPattern:list[int]=["r","g","b"], lenght:int=None) -> bool:
	# check types
	if type(inputImagePath) is not str:
		raise TypeError(f"inputImagePath={type(inputImagePath)} must be of type str")
	if type(outputFilePath) is not str:
		raise TypeError(f"outputFilePath={type(outputFilePath)} must be of type str")
	if type(bitPattern) not in (list, tuple):
		raise TypeError(f"bitPattern={type(bitPattern)} must be of type list")
	if type(colorPattern) not in (list, tuple):
		raise TypeError(f"colorPattern={type(colorPattern)} must be of type list")
	if type(lenght) not in (int, type(None)):
		raise TypeError(f"lenght={type(lenght)} must be of type int or None")
	# check values
	if len(bitPattern) < 1:
		raise ValueError(f"{bitPattern=} must contain at least one element")
	if len(colorPattern) < 1:
		raise ValueError(f"{colorPattern=} must contain at least one element")
	# check inner types
	for ind, el in enumerate(bitPattern):
		if type(el) not in (int, str):
			raise ValueError(f"bitPattern[{ind}]={type(bitPattern[ind])} must be of type int or a specific str")
	for ind, el in enumerate(colorPattern):
		if type(el) not in (int, str):
			raise ValueError(f"colorPattern[{ind}]={type(colorPattern[ind])} must be of type int or a specific str")
	# load image
	inputImage = loadImage(inputImagePath)
	width, height = inputImage.size
	pixels = image2Array(inputImage)
	# check values
	if lenght is not None:
		if not (0 <= lenght <= width*height):
			raise ValueError(f"{lenght=} must be between 0 and {width*height=}")
	else:
		lenght = width * height
	# setup progress bar
	pbar = tqdm(
		total = width * height,
		unit = "px",
		desc = "Progress",
		unit_scale = True,
		colour = "#ffb900"
	)
	pbarUpdate = lambda x=1: pbar.update(x)
	# get patterns lenght
	bitPatternLen = len(bitPattern)
	colorPatternLen = len(colorPattern)
	# seek bits from input image
	bits = bitarray()
	bitsInd = 0
	BREAK = False
	for y in range(height):
		for x in range(width):
			# break if end of bits reached and repeat is False
			if bitsInd >= lenght:
				pbar.total = bitsInd // 3
				BREAK = True
				break
			# get bits
			pixel = pixels[y][x]
			bits.append(getBit(pixel[0], pos=bitPattern[bitsInd % bitPatternLen])); bitsInd += 1
			bits.append(getBit(pixel[1], pos=bitPattern[bitsInd % bitPatternLen])); bitsInd += 1
			bits.append(getBit(pixel[2], pos=bitPattern[bitsInd % bitPatternLen])); bitsInd += 1
			# update counters
			pbarUpdate()
		# break if inner loop breaks
		if BREAK:
			break
	# close progress bar
	pbar.colour = "#8ce10b"
	pbar.close()
	# save seeked bits
	error = bitArray2File(outputFilePath, bits)
	# return if saving was successful
	return not error
