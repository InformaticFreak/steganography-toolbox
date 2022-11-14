
import os, string
import numpy as np

from random import randint
from os.path import abspath
from bitarray import bitarray
from PIL import Image
from colorama import Fore, Back, Style


"""
file <-> bitarray functions
"""

def file2BitArray(path:str) -> bitarray:
	# check types
	if type(path) is not str:
		raise TypeError(f"={type(path)} must be of type str")
	# return bitarray of file
	bitArray = bitarray()
	with open(path, "rb") as fobj:
		bitArray.fromfile(fobj)
	return bitArray

def bitArray2File(path:str, bitArray:bitarray) -> bool:
	# check types
	if type(path) is not str:
		raise TypeError(f"path={type(path)} must be of type str")
	if type(bitArray) is not bitarray:
		raise TypeError(f"bitArray={type(bitArray)} must be of type bitarray")
	# try to save file
	try:
		with open(path, "wb") as fobj:
			bitArray.tofile(fobj)
		error = False
	except OSError:
		error = True
	except Exception as exc:
		raise exc
	# return if saving was successful
	return not error

def setBit(bit:bool, bits:int, *, pos:int="least", bigEndian:bool=True) -> int:
	# check types
	if type(bit) not in (bool, int):
		raise TypeError(f"bit={type(bit)} must be of type bool or int")
	if type(bits) not in (int, np.uint8):
		raise TypeError(f"bits={type(bits)} must be of type int")
	if type(pos) not in (int, str):
		raise TypeError(f"pos={type(pos)} must be of type int or a specific str")
	if type(bigEndian) is not bool:
		raise TypeError(f"bigEndian={type(bigEndian)} must be of type bool")
	# check values
	if type(bit) is int:
		if not (0 <= bit <= 1):
			raise ValueError(f"{bit=} must be 0 or 1 if int")
	if not (0 <= bits <= 255):
		raise ValueError(f"{bits=} must be between 0 and 255")
	posLiterals = {
		("least", True ): -1,
		("most" , True ):  0,
		("least", False):  0,
		("most" , False): -1
	}
	if type(pos) is str:
		posInteger = posLiterals.get((pos, bigEndian))
		if posInteger is None:
			raise ValueError(f"{pos=} must be 'least' or 'most' if str")
		pos = posInteger
	elif type(pos) is int:
		if not (0 <= pos <= 7) and not (-8 <= pos <= -1):
			raise ValueError(f"{pos=} must be between 0 and 7 or between -8 and -1")
	# set bit; TODO: use bit-shifting
	bitsStr = f"{bits:0>8b}"
	bitsList = [ char for char in bitsStr ]
	bitsList[pos] = str(int(bit))
	# return bits as int
	return int("".join(bitsList), 2)

def getBit(bits:int, *, pos:int="least", bigEndian:bool=True) -> bool:
	# check types
	if type(bits) not in (int, np.uint8):
		raise TypeError(f"bits={type(bits)} must be of type int")
	if type(pos) not in (int, str):
		raise TypeError(f"pos={type(pos)} must be of type int or a specific str")
	if type(bigEndian) is not bool:
		raise TypeError(f"bigEndian={type(bigEndian)} must be of type bool")
	# check values
	posLiterals = {
		("least", True ): -1,
		("most" , True ):  0,
		("least", False):  0,
		("most" , False): -1
	}
	if type(pos) is str:
		posInteger = posLiterals.get((pos, bigEndian))
		if posInteger is None:
			raise ValueError(f"{pos=} must be 'least' or 'most' if str")
		pos = posInteger
	elif type(pos) is int:
		if not (0 <= pos <= 7) and not (-8 <= pos <= -1):
			raise ValueError(f"{pos=} must be between 0 and 7 or between -8 and -1")
	# get bit; TODO: use bit-shifting
	bitsString = f"{bits:0>8b}"
	bit = bool(int(bitsString[pos]))
	# return bit as bool
	return bit

"""
image <-> array functions
"""

def image2Array(image:Image.Image) -> np.ndarray:
	# check types
	if type(image) is not Image.Image:
		raise TypeError(f"image={type(image)} must be of type Image.Image")
	# return image as array
	imageArray = np.array(image)
	return imageArray

def array2Image(imageArray:np.ndarray) -> Image.Image:
	# check types
	if type(imageArray) is not np.ndarray:
		raise TypeError(f"imageArray={type(imageArray)} must be of type numpy.array")
	# return image object
	return Image.fromarray(imageArray)

def saveImage(path:str, image:Image.Image, *, show:bool=False) -> bool:
	# check types
	if type(path) is not str:
		raise TypeError(f"path={type(path)} must be of type str")
	if type(image) is not Image.Image:
		raise TypeError(f"image={type(image)} must be of type Image.Image")
	if type(show) is not bool:
		raise TypeError(f"show={type(show)} must be of type bool")
	# try to save image
	try:
		image = image.convert("RGB")
		image.save(abspath(path))
		error = False
	except OSError:
		error = True
	except Exception as exc:
		raise exc
	# optional: show image
	if show:
		image.show()
	# return if saving was successful
	return not error

def loadImage(path:str) -> Image:
	# check types
	if type(path) is not str:
		raise TypeError(f"path={type(path)} must be of type str")
	# return image object
	image = Image.open(path)
	image = image.convert("RGB")
	return image

"""
styling functions
"""

def generateTitle(*, width:int=80, height:int=5) -> list[str]:
	# check types
	if type(width) is not int:
		raise TypeError(f"width={type(width)} must be of type int")
	if type(height) is not int:
		raise TypeError(f"height={type(height)} must be of type int")
	# styled title
	titleText = "  Steganography  Toolbox  "
	titleLen = len(titleText)
	title = Style.NORMAL+Fore.GREEN + titleText + Fore.RESET+Style.DIM
	# check values
	if width < titleLen:
		raise ValueError(f"{width=} must be greater than {titleLen-1}")
	if height < 1:
		raise ValueError(f"{height=} must be greater than 0")
	# possibile letters, including density
	letters = string.ascii_lowercase + string.ascii_uppercase + string.punctuation + string.digits + 100*" "
	lettersLen = len(letters)
	# possibile colors, including density
	colorsDark = [Fore.BLACK, Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW]
	colorsLight = [Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX]
	colorsReset = [Fore.RESET for _ in range(20) ]
	colors = [ *colorsDark, *colorsLight, *colorsReset ]
	colorsLen = len(colors)
	# position for title
	titleLineInd = height // 2
	titleCharInd = (width - titleLen) // 2
	# generate lines
	lines = []
	for lineInd in range(height):
		line = Style.DIM
		for charInd in range(width):
			# write title
			if lineInd == titleLineInd and charInd == titleCharInd:
				line += title
			elif lineInd == titleLineInd and titleCharInd <= charInd <= titleCharInd + titleLen:
				continue
			# write random characters and colors
			else:
				line += colors[ randint(0, colorsLen-1) ]
				line += letters[ randint(0, lettersLen-1) ]
		lines.append(line)
	# return generated ascii art
	return lines
