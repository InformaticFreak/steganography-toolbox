
import os
import numpy as np

from bitarray import bitarray
from PIL import Image
from tqdm import tqdm

from functions import *


"""
hide functions
"""

def hideFileInImage(inputImagePath:str, outputImagePath:str, inputFilePath:str, *, repeat:bool=True, bitPattern:list[int]=["least"], colorPattern:list[list[int]]=[("r","g","b")], **kwargs_save) -> bool:
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
	if type(colorPattern) is not list:
		raise TypeError(f"colorPattern={type(colorPattern)} must be of type list")
	# check values
	if len(bitPattern) < 1:
		raise ValueError(f"{bitPattern=} must contain at least one element")
	if len(colorPattern) < 1:
		raise ValueError(f"{colorPattern=} must contain at least one element")
	# check inner types
	for bitPosInd, bitPos in enumerate(bitPattern):
		if type(bitPos) not in (int, str):
			raise TypeError(f"bitPattern[{bitPosInd}]={type(bitPattern[bitPosInd])} must be of type int or a specific str")
	channelLiterals = {"r": 0, "g": 1, "b": 2}
	for colPxInd, colPx in enumerate(colorPattern):
		if type(colPx) is not list:
			raise TypeError(f"colorPattern[{colPxInd}]={type(colorPattern[colPxInd])} must be of type list")
		# check inner values
		if not (1 <= len(colPx) <= 3):
			raise ValueError(f"colorPattern[{colPxInd}]={colorPattern[colPxInd]} must contain between 1 and 3 elements")
		for colChnInd, colChn in enumerate(colPx):
			# check inner values
			if type(colChn) is str:
				colValInteger = channelLiterals.get(colChn)
				if colValInteger is None:
					raise ValueError(f"colorPattern[{colPxInd}][{colChnInd}]={colorPattern[colPxInd][colChnInd]} must be 'r', 'g' or 'b' if str")
				else:
					colorPattern[colPxInd][colChnInd] = colValInteger
			elif type(colChn) is int:
				if not (0 <= colChn <= 2):
					raise ValueError(f"colorPattern[{colPxInd}][{colChnInd}]={colorPattern[colPxInd][colChnInd]} must be between 0 and 2 if int")
			# check inner type
			else:
				raise TypeError(f"colorPattern[{colPxInd}][{colChnInd}]={type(colorPattern[colPxInd][colChnInd])} must be of type int or specific str")
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
		colour = "#FFB900"
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
				pbar.total = y * width + x
				BREAK = True
				break
			# modify bits according to the given bit and color channel patterns
			pixel = pixels[y][x]
			newPixel = list(pixel)
			for channel in colorPattern[bitsInd % colorPatternLen]:
				newPixel[channel] = setBit(bits[bitsInd % bitsLen], pixel[channel], pos=bitPattern[bitsInd % bitPatternLen])
				bitsInd += 1
			pixels[y][x] = tuple(newPixel)
			# update counters
			pbarUpdate()
		# break if inner loop breaks
		if BREAK:
			break
	# close progress bar
	pbar.colour = "#8CE10B"
	pbar.close()
	# save image
	outputImage = array2Image(pixels)
	error = saveImage(outputImagePath, outputImage, **kwargs_save)
	# return if saving was successful
	return not error

"""
seek functions
"""

def seekFileInImage(inputImagePath:str, outputFilePath:str, *, bitPattern:list[int]=["least"], colorPattern:list[list[int]]=[("r","g","b")], lenght:int=None) -> bool:
	# check types
	if type(inputImagePath) is not str:
		raise TypeError(f"inputImagePath={type(inputImagePath)} must be of type str")
	if type(outputFilePath) is not str:
		raise TypeError(f"outputFilePath={type(outputFilePath)} must be of type str")
	if type(bitPattern) not in (list, tuple):
		raise TypeError(f"bitPattern={type(bitPattern)} must be of type list")
	if type(colorPattern) is not list:
		raise TypeError(f"colorPattern={type(colorPattern)} must be of type list")
	if type(lenght) not in (int, type(None)):
		raise TypeError(f"lenght={type(lenght)} must be of type int or None")
	# check values
	if len(bitPattern) < 1:
		raise ValueError(f"{bitPattern=} must contain at least one element")
	if len(colorPattern) < 1:
		raise ValueError(f"{colorPattern=} must contain at least one element")
	# check inner types
	for bitPosInd, bitPos in enumerate(bitPattern):
		if type(bitPos) not in (int, str):
			raise TypeError(f"bitPattern[{bitPosInd}]={type(bitPattern[bitPosInd])} must be of type int or a specific str")
	channelLiterals = {"r": 0, "g": 1, "b": 2}
	for colPxInd, colPx in enumerate(colorPattern):
		if type(colPx) is not list:
			raise TypeError(f"colorPattern[{colPxInd}]={type(colorPattern[colPxInd])} must be of type list")
		# check inner values
		if not (1 <= len(colPx) <= 3):
			raise ValueError(f"colorPattern[{colPxInd}]={colorPattern[colPxInd]} must contain between 1 and 3 elements")
		for colValInd, colVal in enumerate(colPx):
			# check inner values
			if type(colVal) is str:
				colValInteger = channelLiterals.get(colVal)
				if colValInteger is None:
					raise ValueError(f"colorPattern[{colPxInd}][{colValInd}]={colorPattern[colPxInd][colValInd]} must be 'r', 'g' or 'b' if str")
				else:
					colorPattern[colPxInd][colValInd] = colValInteger
			elif type(colVal) is int:
				if not (0 <= colVal <= 2):
					raise ValueError(f"colorPattern[{colPxInd}][{colValInd}]={colorPattern[colPxInd][colValInd]} must be between 0 and 2 if int")
			# check inner type
			else:
				raise TypeError(f"colorPattern[{colPxInd}][{colValInd}]={type(colorPattern[colPxInd][colValInd])} must be of type int or specific str")
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
		colour = "#FFB900"
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
				pbar.total = y * width + x
				BREAK = True
				break
			# get bits according to the given bit and color channel patterns
			pixel = pixels[y][x]
			for channel in colorPattern[bitsInd % colorPatternLen]:
				bits.append(getBit(pixel[channel], pos=bitPattern[bitsInd % bitPatternLen]))
				bitsInd += 1
			# update counters
			pbarUpdate()
		# break if inner loop breaks
		if BREAK:
			break
	# close progress bar
	pbar.colour = "#8CE10B"
	pbar.close()
	# save seeked bits
	error = bitArray2File(outputFilePath, bits)
	# return if saving was successful
	return not error
