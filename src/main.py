
import os, sys

from PIL import UnidentifiedImageError
from pick import pick
from os.path import join as joinPath
from os.path import abspath
from colorama import init as coloramaInit

from tools import *
from functions import *


def main(*args):
	# generate title as ascii art
	ascii_art = generateTitle()
	print("\n", "\n".join(ascii_art), "\n")
	
	# select: action
	title = "Hide or Seek?"
	options = ["Hide", "Seek"]
	option, index = pick(options, title)
	print(f"{Fore.BLUE}{title} {Fore.RESET}{option}")
	
	# action: hide
	if option == "Hide":
		# select: advanced options
		title = "Advanced options:"
		options = [
			"Console input as input file",          # 0
			"Show output image after saving",       # 1
			"Repeat input file in image",           # 2
			"Select position of manipulated bits",  # 3
			"Get lenght of hidden bits"             # 4
		]
		selected = pick(options, title, multiselect=True)
		selected_advOpt = { index: option for option, index in selected }
		if len(selected) > 0:
			print(f"{Fore.BLUE}{title}{Fore.RESET}\n{Fore.RESET}-", "\n- ".join([ option.lower() for option, _ in selected ]))
		else:
			print(f"{Fore.BLUE}{title}{Fore.RESET}{Style.DIM} --")
		
		# advanced options: read multiline text from console input
		if selected_advOpt.get(0):
			print(Fore.BLUE+"Multiline input: ")
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
			title = "Position of manipulated bits:"
			options = [
				"0 (most significant bit)",
				"1", "2", "3", "4", "5", "6",
				"7 (least significant bit)"
			]
			optionRating = { label: color for label, color in zip(options, [ *([Fore.RED]*3), *([Fore.YELLOW]*3), *([Fore.GREEN]*3) ]) }
			option, index = pick(options, title)
			print(f"{Fore.BLUE}{title} {Fore.RESET}{optionRating.get(option)}{option}")
			pos = int(option[0])
		else:
			pos = "least"
		
		# get file paths without " or '
		inputImagePath  = abspath(input(f"{Fore.BLUE}Input image path:\t{Fore.RESET}").replace('"', '').replace("'", ""))
		outputImagePath = abspath(input(f"{Fore.BLUE}Output image path:\t{Fore.RESET}").replace('"', '').replace("'", ""))
		if not selected_advOpt.get(0):
			inputFilePath = abspath(input(f"{Fore.BLUE}Input file path:\t{Fore.RESET}").replace('"', '').replace("'", ""))
		else:
			inputFilePath = consoleInputPath
		
		# advanced option: get lenght of hidden bits
		if selected_advOpt.get(4):
			lenght = len(file2BitArray(inputFilePath))
			print(f"{Fore.CYAN}Lenght of hidden bits: {Fore.RESET}{lenght}")
		
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
		print(f"{Fore.RED}file could not be saved" if error else f"{Fore.GREEN}file saved")
	
	# action: seek
	elif option == "Seek":
		# select: advanced options
		title = "Advanced options:"
		options = [
			"Show extracted file (img / txt)",      # 0
			"Select position of manipulated bits",  # 1
			"Set lenght of hidden bits"             # 2
		]
		selected = pick(options, title, multiselect=True)
		selected_advOpt = { index: option for option, index in selected }
		if len(selected) > 0:
			print(f"{Fore.BLUE}{title}{Fore.RESET}\n{Fore.RESET}-", "\n- ".join([ option.lower() for option, _ in selected ]))
		else:
			print(f"{Fore.BLUE}{title}{Fore.RESET}{Style.DIM} --")
		
		# advanced options: select position of manipulated bits
		if selected_advOpt.get(1):
			title = "Position of manipulated bits:"
			options = [
				"0 (most significant bit)",
				"1", "2", "3", "4", "5", "6",
				"7 (least significant bit)"
			]
			optionRating = { label: color for label, color in zip(options, [ *([Fore.RED]*3), *([Fore.YELLOW]*3), *([Fore.GREEN]*3) ]) }
			option, index = pick(options, title)
			print(f"{Fore.BLUE}{title} {Fore.RESET}{optionRating.get(option)}{option}")
			pos = int(option[0])
		else:
			pos = "least"
		
		# advanced options: set lenght of hidden bits
		if selected_advOpt.get(2):
			while not (lenghtInput := input(f"{Fore.BLUE}Lenght of hidden bits: {Fore.RESET}")).isdigit():
				pass
			lenght = int(lenghtInput)
		else:
			lenght = None
		
		# get file paths without " or '
		inputImagePath = abspath(input(f"{Fore.BLUE}Input image path:\t{Fore.RESET}").replace('"', '').replace("'", ""))
		outputFilePath = abspath(input(f"{Fore.BLUE}Output file path:\t{Fore.RESET}").replace('"', '').replace("'", ""))

		# seek file in image
		error = seekFileInImage(
			inputImagePath,
			outputFilePath,
			# advanced options: pos, lenght
			pos = pos,
			lenght = lenght
		)
		print(f"{Fore.RED}file could not be saved" if error else f"{Fore.GREEN}file saved")
		
		# advanced options: show extracted file
		if selected_advOpt.get(0):
			# try for txt
			try:
				with open(outputFilePath, "r", encoding="utf-8") as fobj:
					extractedText = fobj.read( min(lenght // 8, 100) )
				print(f"{Fore.CYAN}Extracted Text:\n{Fore.RESET}{extractedText}")
			except UnicodeDecodeError:
				print(f"{Fore.RED}can't open as text file")
			except Exception as exc:
				raise exc
			# try for img
			try:
				extractedImage = loadImage(outputFilePath)
				extractedImage.show()
			except UnidentifiedImageError:
				print(f"{Fore.RED}can't open as image file")
			except Exception as exc:
				raise exc

if __name__ == "__main__":
	coloramaInit(autoreset=True)
	main(*sys.argv[1:])
