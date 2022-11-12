
import os, sys, re, time, math
import tqdm, pick
import numpy as np
import bitarray

from PIL import Image
from colorama import Fore, Back, Style
from colorama import init as coloramaInit
from os.path import join as joinPath
from tqdm import tqdm

from functions import *
from methods import *


def main(*args):
	testPath = joinPath("..", "test")
	hideTextInImage(
		os.path.abspath(joinPath(testPath, "inputImage.png")),
		os.path.abspath(joinPath(testPath, "outputImage.png")),
		os.path.abspath(joinPath(testPath, "inputText.txt"))
	)

if __name__ == "__main__":
	main(*sys.argv[1:])

