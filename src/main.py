
import os, sys
import numpy as np

from pick import pick
from tqdm import tqdm
from os.path import join as joinPath
from os.path import abspath
from colorama import Fore, Back, Style
from colorama import init as coloramaInit

from tools import *


def main(*args):
	# select: action
	title = "Hide or Seek?"
	options = ["Hide", "Seek"]
	option, index = pick(options, title)
	
	# action: hide
	if option == "Hide":
		# select: advanced options
		title = "Advanced options:"
		options = [
			"Show output image after saving",
			"Repeat input file in image"
		]
		selected = pick(options, title, multiselect=True)
		selected = { option.split(" ")[0].lower() for option, _ in selected }
		
		# get file paths without " or '
		inputImagePath  = input("Input image path:  ").replace('"', '').replace("'", "")
		outputImagePath = input("Output image path: ").replace('"', '').replace("'", "")
		inputFilePath   = input("Input file path:   ").replace('"', '').replace("'", "")
		
		# hide file
		error = hideFileInImage(
			abspath(inputImagePath),
			abspath(outputImagePath),
			abspath(inputFilePath),
			# advanced options: show, repeat
			show = "show" in selected,
			repeat = "repeat" in selected
		)
		print(Fore.RED+"error occured" if error else Fore.GREEN+"file saved")
	
	# action: seek
	elif option == "Seek":
		# get file paths without " or '
		inputImagePath = input("Input image path: ").replace('"', '').replace("'", "")
		outputFilePath = input("Output file path: ").replace('"', '').replace("'", "")

		# seek file
		error = seekFileInImage(
			abspath(inputImagePath),
			abspath(outputFilePath)
		)
		print(Fore.RED+"error occured" if error else Fore.GREEN+"file saved")


if __name__ == "__main__":
	coloramaInit(autoreset=True)
	main(*sys.argv[1:])

