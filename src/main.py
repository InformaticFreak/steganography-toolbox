
import os, sys
import string

from random import randint
from PIL import UnidentifiedImageError
from pick import pick
from os.path import join as joinPath
from os.path import abspath
from colorama import Fore, Back, Style
from colorama import init as coloramaInit

from tools import *
from functions import *


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


def main(*args):
	# generate title as ascii art
	ascii_art = generateTitle(width=50, height=3)
	print("\n".join(ascii_art))
	
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
			"Console input as input file",          # 0
			"Show output image after saving",       # 1
			"Repeat input file in image",           # 2
			"Select position of manipulated bits",  # 3
			"Get lenght of hidden bits",            # 4
			"Save config"                           # 5
		]
		selected = pick(options, title, multiselect=True)
		selected_advOpt = { index: option for option, index in selected }
		print(title, "\n- ".join([ option.lower() for option, _ in selected ]))
		
		# advanced options: read multiline text from console input
		if selected_advOpt.get(0):
			print("Multiline input: ")
			inputList = []
			while (text := input()) != "EOF":
				inputList.append(text)
			inputList.append("\n")
		# write input to temp file
		consoleInputPath = joinPath("..", "tmp", "consoleInput.txt")
		with open(consoleInputPath, "w+", encoding="utf-8") as fobj:
			fobj.write("\n".join(inputList))
		
		# advanced options: select position of manipulated bits
		if selected_advOpt.get(3):
			title = "Position of manipulated bits"
			options = [
				"0 (most significant bit)",
				"1", "2", "3", "4", "5", "6",
				"7 (least significant bit)"
			]
			option, index = pick(options, title)
			print(f"{title} {option}")
			pos = int(option[0])
		else:
			pos = "least"
		
		# get file paths without " or '
		inputImagePath  = abspath(input("Input image path:\t").replace('"', '').replace("'", ""))
		outputImagePath = abspath(input("Output image path:\t").replace('"', '').replace("'", ""))
		if not selected_advOpt.get(0):
			inputFilePath = abspath(input("Input file path:\t").replace('"', '').replace("'", ""))
		else:
			inputFilePath = consoleInputPath
		
		# advanced option: get lenght of hidden bits
		if selected_advOpt.get(4):
			lenght = len(file2BitArray(inputFilePath))
			print(f"Lenght of hidden bits: {lenght}")
		
		# hide file in image
		error = hideFileInImage(
			inputImagePath,
			outputImagePath,
			inputFilePath,
			# advanced options: show, repeat, pos
			show = bool(selected_advOpt.get(1)),
			repeat = bool(selected_advOpt.get(2)),
			pos = pos
		)
		print(Fore.RED+"error occured" if error else Fore.GREEN+"file saved")
	
	# action: seek
	elif option == "Seek":
		# select: advanced options
		title = "Advanced options:"
		options = [
			"Show extracted file (img / txt)",      # 0
			"Select position of manipulated bits",  # 1
			"Set lenght of hidden bits",            # 2
			"Save config"                           # 3
		]
		selected = pick(options, title, multiselect=True)
		selected_advOpt = { index: option for option, index in selected }
		print(title, "\n- ".join([ option.lower() for option, _ in selected ]))
		
		# advanced options: select position of manipulated bits
		if selected_advOpt.get(1):
			title = "Position of manipulated bits"
			options = [
				"0 (most significant bit)",
				"1", "2", "3", "4", "5", "6",
				"7 (least significant bit)"
			]
			option, index = pick(options, title)
			print(f"{title} {option}")
			pos = int(option[0])
		else:
			pos = "least"
		
		# advanced options: set lenght of hidden bits
		if selected_advOpt.get(2):
			while not (lenghtInput := input("Lenght of hidden bits: ")).isdigit():
				pass
			lenght = int(lenghtInput)
		else:
			lenght = None
		
		# get file paths without " or '
		inputImagePath = abspath(input("Input image path:\t").replace('"', '').replace("'", ""))
		outputFilePath = abspath(input("Output file path:\t").replace('"', '').replace("'", ""))

		# seek file in image
		error = seekFileInImage(
			inputImagePath,
			outputFilePath,
			# advanced options: pos, lenght
			pos = pos,
			lenght = lenght
		)
		print(Fore.RED+"error occured" if error else Fore.GREEN+"file saved")
		
		# advanced options: show extracted file
		if selected_advOpt.get(0):
			# try for txt
			try:
				with open(outputFilePath, "r", encoding="utf-8") as fobj:
					extractedText = fobj.read( min(lenght // 8, 100) )
				print(f"Extracted Text:\n{extractedText}")
			except UnicodeDecodeError:
				print("can't open as text file")
			except Exception as exc:
				raise exc
			# try for img
			try:
				extractedImage = loadImage(outputFilePath)
				extractedImage.show()
			except UnidentifiedImageError:
				print("can't open as image file")
			except Exception as exc:
				raise exc

if __name__ == "__main__":
	coloramaInit(autoreset=True)
	main(*sys.argv[1:])

