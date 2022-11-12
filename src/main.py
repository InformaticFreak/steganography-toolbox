
import os, sys
import numpy as np

from os.path import join as joinPath
from os.path import abspath
from colorama import Fore, Back, Style
from colorama import init as coloramaInit

from functions import *
from methods import *


def main(*args):
	testPath = joinPath("..", "test")
	
	# hide
	error = hideTextInImage(
		abspath(joinPath(testPath, "inputImage.png")),
		abspath(joinPath(testPath, "outputImage.png")),
		abspath(joinPath(testPath, "inputText.txt")),
		repeat = False,
		show = False # show after saving image
	)
	print(Fore.RED+"error occured" if error else Fore.GREEN+"file saved")
	
	# seek
	error = seekTextInImage(
		abspath(joinPath(testPath, "outputImage.png")),
		abspath(joinPath(testPath, "outputText.txt"))
	)
	print(Fore.RED+"error occured" if error else Fore.GREEN+"file saved")


if __name__ == "__main__":
	coloramaInit(autoreset=True)
	main(*sys.argv[1:])

