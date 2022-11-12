
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
	print(f"{title} {option}")
	
	# action: hide
	if option == "Hide":
		# select: advanced options
		title = "Advanced options:"
		options = [
			"Console input as input file",
			"Show output image after saving",
			"Repeat input file in image",
		]
		selected = pick(options, title, multiselect=True)
		selected = [ option.split(" ")[0].lower() for option, _ in selected ]
		print(f"{title} {', '.join(selected)}")
		
		# read multiline text from console input
		if "console" in selected:
			print("Multiline input: ")
			inputList = []
			text = ""
			while text != "EOF":
				text = input()
				inputList.append(text)
			inputList.append("\n")
		# write input to temp file
		consoleInputPath = joinPath("..", "tmp", "consoleInput.txt")
		with open(consoleInputPath, "w+", encoding="utf-8") as fobj:
			fobj.write("\n".join(inputList))
		
		# get file paths without " or '
		inputImagePath = input("Input image path:  ").replace('"', '').replace("'", "")
		outputImagePath = input("Output image path: ").replace('"', '').replace("'", "")
		# 
		if "console" not in selected:
			inputFilePath = input("Input file path:   ").replace('"', '').replace("'", "")
		else:
			inputFilePath = consoleInputPath
		
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

