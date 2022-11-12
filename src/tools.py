
import os
import numpy as np

from bitarray import bitarray
from PIL import Image
from tqdm import tqdm

from functions import *


"""
hide functions
"""

def hideBitsInImage(image:Image.Image, bits:bitarray, *, repeat:bool=True, progressBar:tqdm=True) -> Image.Image:
	# check types
	if type(image) is not Image.Image:
		raise TypeError(f"image={type(image)} must be of type Image.Image")
	if type(bits) is not bitarray:
		raise TypeError(f"bits={type(bits)} must be of type bitarray")
	if type(repeat) is not bool:
		raise TypeError(f"repeat={type(repeat)} must be of type bool")
	if type(progressBar) not in (tqdm, bool):
		raise TypeError(f"progressBar={type(progressBar)} must be of type tqdm or bool")
	# convert image to array
	width, height = image.size
	pixels = image2Array(image)
	# set progress bar behavior
	if type(progressBar) is bool:
		if progressBar:
			# setup progress bar
			pbar = tqdm(
				total = width * height,
				desc = "Progress",
				unit = "px",
				unit_scale = True,
				colour = "#ffb900"
			)
			# progress bar updater functions
			pbarUpdate = lambda: pbar.update(1)
		else:
			pbarUpdate = lambda: None
	elif type(progressBar) is tqdm:
		pbarUpdate = lambda: progressBar.update(1)
	# get bits lenght
	bitsLen = len(bits)
	bitsInd = 0
	# hide file in image
	BREAK = False
	for y in range(height):
		for x in range(width):
			# break if end of bits reached and repeat is False
			if not repeat and bitsInd >= bitsLen:
				pbar.total = bitsInd // 3
				BREAK = True
				break
			# modify least significant bits
			pixel = pixels[y][x]
			r = setBit(bits[bitsInd % bitsLen], pixel[0]); bitsInd += 1
			g = setBit(bits[bitsInd % bitsLen], pixel[1]); bitsInd += 1
			b = setBit(bits[bitsInd % bitsLen], pixel[2]); bitsInd += 1
			pixels[y][x] = (r, g, b)
			pbarUpdate()
		# break if inner loop breaks
		if BREAK:
			break
	# close progress bar
	if type(progressBar) is bool and progressBar:
		pbar.close()
	# return array as image
	return array2Image(pixels)

def hideFileInImage(inputImagePath:str, outputImagePath:str, inputFilePath:str, *, repeat:bool=True, **kwargs_save) -> bool:
	# check types
	if type(inputImagePath) is not str:
		raise TypeError(f"inputImagePath={type(inputImagePath)} must be of type str")
	if type(outputImagePath) is not str:
		raise TypeError(f"outputImagePath={type(outputImagePath)} must be of type str")
	if type(inputFilePath) is not str:
		raise TypeError(f"inputFilePath={type(inputFilePath)} must be of type str")
	if type(repeat) is not bool:
		raise TypeError(f"repeat={type(repeat)} must be of type bool")
	# load image to array
	inputImage = loadImage(inputImagePath)
	width, height = inputImage.size
	# setup progress bar
	pbar = tqdm(
		total = width * height,
		desc = "Progress",
		unit = "px",
		unit_scale = True,
		colour = "#ffb900"
	)
	# convert file to bitarray
	bits = file2BitArray(inputFilePath)
	# hide bitarray in image
	outputImage = hideBitsInImage(inputImage, bits, repeat=repeat, progressBar=pbar)
	# close progress bar
	pbar.close()
	# save image
	error = saveImage(outputImagePath, outputImage, **kwargs_save)
	# return if saving was successful
	return not error

def seekFileInImage(inputImagePath:str, outputFilePath:str) -> bool:
	# check types
	if type(inputImagePath) is not str:
		raise TypeError(f"inputImagePath={type(inputImagePath)} must be of type str")
	if type(outputFilePath) is not str:
		raise TypeError(f"outputFilePath={type(outputFilePath)} must be of type str")
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
	# seek file from image
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
	# save bitarray in file
	error = bitArray2File(outputFilePath, bits)
	# return if saving was successful
	return not error
