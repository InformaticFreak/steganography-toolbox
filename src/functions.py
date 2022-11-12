
import os
import numpy as np

from os.path import abspath
from bitarray import bitarray
from PIL import Image
from tqdm import tqdm

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
		raise TypeError(f"pos={type(pos)} must be of type int as specific str")
	if type(bigEndian) is not bool:
		raise TypeError(f"bigEndian={type(bigEndian)} must be of type bool")
	# check values
	elif type(bit) is int:
		if not (0 <= bit <= 1):
			raise ValueError(f"{bit=} must be 0 or 1 if int")
	bitsLen = len(f"{bits:b}")
	if bitsLen < 1:
		raise ValueError(f"{bits=:b} must have at least one digit")
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
		if not (0 <= pos <= bitsLen-1) and not (-bitsLen <= pos <= -1):
			raise ValueError(f"{pos=} must be between 0 and {bitsLen-1} or between {-bitsLen} and -1")
	# set bit; TODO: use bit-shifting
	bitsList = [ char for char in f"{bits:b}" ]
	bitsList[pos] = str(int(bit))
	# return bits as int
	return int("".join(bitsList), 2)

def getBit(bits:int, *, pos:int="least", bigEndian:bool=True) -> bool:
	# check types
	if type(bits) not in (int, np.uint8):
		raise TypeError(f"bits={type(bits)} must be of type int")
	if type(pos) not in (int, str):
		raise TypeError(f"pos={type(pos)} must be of type int as specific str")
	if type(bigEndian) is not bool:
		raise TypeError(f"bigEndian={type(bigEndian)} must be of type bool")
	# check values
	bitsLen = len(f"{bits:b}")
	if bitsLen < 1:
		raise ValueError(f"{bits=:b} must have at least one digit")
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
		if not (0 <= pos <= bitsLen-1) and not (-bitsLen <= pos <= -1):
			raise ValueError(f"{pos=} must be between 0 and {bitsLen-1} or between {-bitsLen} and -1")
	# get bit; TODO: use bit-shifting
	bitsString = f"{bits:b}"
	# return bit at given position as bool
	return bool(int(bitsString[pos]))

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
	return Image.open(path).convert("RGB")
