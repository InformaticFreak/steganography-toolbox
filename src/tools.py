
import os
import numpy as np

from bitarray import bitarray
from PIL import Image
from tqdm import tqdm

from functions import *


"""
hide functions
"""

def hideBitsInImage(image:Image.Image, bits:bitarray, *, repeat:bool=True, pos:int="least", progressBar:tqdm=True, **kwargs_pbar) -> Image.Image:
	# check types
	if type(image) is not Image.Image:
		raise TypeError(f"image={type(image)} must be of type Image.Image")
	if type(bits) is not bitarray:
		raise TypeError(f"bits={type(bits)} must be of type bitarray")
	if type(repeat) is not bool:
		raise TypeError(f"repeat={type(repeat)} must be of type bool")
	if type(pos) not in (int, str):
		raise TypeError(f"pos={type(pos)} must be of type int as specific str")
	if type(progressBar) not in (tqdm, bool):
		raise TypeError(f"progressBar={type(progressBar)} must be of type tqdm or bool")
	# convert image to array
	width, height = image.size
	pixels = image2Array(image)
	# set progress bar behavior
	if type(progressBar) is bool:
		if progressBar:
			# setup progress bar
			pbar = tqdm(total=width*height, unit="px", **kwargs_pbar)
			# progress bar updater functions
			pbarUpdate = lambda x=1: pbar.update(x)
		else:
			pbarUpdate = lambda _=_: _
	elif type(progressBar) is tqdm:
		pbarUpdate = lambda x=1: progressBar.update(x)
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
			r = setBit(bits[bitsInd % bitsLen], pixel[0], pos=pos); bitsInd += 1
			g = setBit(bits[bitsInd % bitsLen], pixel[1], pos=pos); bitsInd += 1
			b = setBit(bits[bitsInd % bitsLen], pixel[2], pos=pos); bitsInd += 1
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

def hideFileInImage(inputImagePath:str, outputImagePath:str, inputFilePath:str, *, repeat:bool=True, pos:int="least", **kwargs_save) -> bool:
	# check types
	if type(inputImagePath) is not str:
		raise TypeError(f"inputImagePath={type(inputImagePath)} must be of type str")
	if type(outputImagePath) is not str:
		raise TypeError(f"outputImagePath={type(outputImagePath)} must be of type str")
	if type(inputFilePath) is not str:
		raise TypeError(f"inputFilePath={type(inputFilePath)} must be of type str")
	if type(repeat) is not bool:
		raise TypeError(f"repeat={type(repeat)} must be of type bool")
	if type(pos) not in (int, str):
		raise TypeError(f"pos={type(pos)} must be of type int as specific str")
	# load image
	inputImage = loadImage(inputImagePath)
	width, height = inputImage.size
	# convert file to bitarray
	bits = file2BitArray(inputFilePath)
	# hide bitarray in image
	outputImage = hideBitsInImage(inputImage, bits, repeat=repeat, pos=pos, desc="Progress", unit_scale=True, colour="#ffb900")
	# save image
	error = saveImage(outputImagePath, outputImage, **kwargs_save)
	# return if saving was successful
	return not error

def seekBitsInImage(image:Image.Image, *, pos:int="least", lenght:int=None, progressBar:tqdm=True, **kwargs_pbar) -> bitarray:
	# check types
	if type(image) is not Image.Image:
		raise TypeError(f"image={type(image)} must be of type Image.Image")
	if type(lenght) not in (int, type(None)):
		raise TypeError(f"lenght={type(lenght)} must be of type int or None")
	if type(progressBar) not in (tqdm, bool):
		raise TypeError(f"progressBar={type(progressBar)} must be of type tqdm or bool")
	# load image to array
	width, height = image.size
	pixels = image2Array(image)
	# check values
	if not 0 <= lenght <= width*height:
		raise ValueError(f"{lenght=} must be between 0 and {width*height} (width x height of image)")
	# set lenght to pixel count if not set
	if lenght is None:
		lenght = width * height
	# set progress bar behavior
	if type(progressBar) is bool:
		if progressBar:
			# setup progress bar
			pbar = tqdm(total=width*height, unit="px", **kwargs_pbar)
			# progress bar updater functions
			pbarUpdate = lambda x=1: pbar.update(x)
		else:
			pbarUpdate = lambda _=_: _ 
	elif type(progressBar) is tqdm:
		pbarUpdate = lambda x=1: progressBar.update(x)
	# seek bits from image
	bits = bitarray()
	bitsInd = 0
	BREAK = False
	for y in range(height):
		for x in range(width):
			# break if end of bits reached and repeat is False
			if bitsInd >= lenght:
				BREAK = True
				break
			# get least significant bits
			pixel = pixels[y][x]
			bits.append(getBit(pixel[0], pos=pos))
			bits.append(getBit(pixel[1], pos=pos))
			bits.append(getBit(pixel[2], pos=pos))
			pbarUpdate()
			bitsInd += 1
		# break if inner loop breaks
		if BREAK:
			break
	# close progress bar
	if type(progressBar) is bool and progressBar:
		pbar.close()
	# return bits as bitarray
	return bits

def seekFileInImage(inputImagePath:str, outputFilePath:str, *, pos:int="least", lenght:int=None) -> bool:
	# check types
	if type(inputImagePath) is not str:
		raise TypeError(f"inputImagePath={type(inputImagePath)} must be of type str")
	if type(outputFilePath) is not str:
		raise TypeError(f"outputFilePath={type(outputFilePath)} must be of type str")
	if type(pos) not in (int, str):
		raise TypeError(f"pos={type(pos)} must be of type int or a specific str")
	if type(lenght) not in (int, type(None)):
		raise TypeError(f"lenght={type(lenght)} must be of type int or None")
	# load image
	inputImage = loadImage(inputImagePath)
	width, height = inputImage.size
	# set lenght to pixel count if not set
	if lenght is None:
		lenght = width * height
	# seek bitarray from image and save in file
	bits = seekBitsInImage(inputImage, pos=pos, lenght=lenght, desc="Progress", unit_scale=True, colour="#ffb900")
	error = bitArray2File(outputFilePath, bits)
	# return if saving was successful
	return not error
