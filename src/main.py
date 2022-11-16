
import os, sys, re

from PIL import UnidentifiedImageError
from pick import pick
from os.path import join as joinPath
from colorama import init as coloramaInit

from tools import *
from functions import *


def advancedOptions_for_setPatterns() -> tuple[list,list]:
	title = "Advanced options:"
	options = [
		"Set bit position pattern",  # 0
		"Set color channel pattern"  # 1
	]
	selected = pick(options, title, multiselect=True)
	selected_advOpt = { index: option for option, index in selected }
	if len(selected) > 0:
		print(f"{Fore.BLUE}{title}{Fore.RESET}\n{Fore.RESET}-", "\n- ".join([ option.lower() for option, _ in selected ]))
	else:
		print(f"{Fore.BLUE}{title}{Fore.RESET}{Style.DIM} --")
	
	# advanced options: set bit position pattern
	if selected_advOpt.get(0):
		pattern = re.compile(r"[0-7]|most|least")
		text = ""
		bitPatternList = []
		while len(bitPatternList) < 1:
			text = input(f"{Fore.BLUE}Bit pattern: {Fore.RESET}")
			bitPatternList = pattern.findall(text.lower())
		bitPatternList = [ (int(el) if el.isdigit() else el) for el in bitPatternList ]
	else:
		bitPatternList =  ["least"]
	
	# advanced options: set color channel pattern
	if selected_advOpt.get(1):
		pattern = re.compile(r"[0-2]|r|g|b")
		text = ""
		colorPatternList = []
		while len(colorPatternList) < 1:
			text = input(f"{Fore.BLUE}Color channel pattern: {Fore.RESET}")
			colorPatternList = pattern.findall(text.lower())
		colorPatternList = [ (int(el) if el.isdigit() else el) for el in colorPatternList ]
	else:
		colorPatternList =  ["r", "g", "b"]
	
	# return option results
	return bitPatternList, colorPatternList


def main(*args, **kwargs):
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
		# select: options
		title = "Options:"
		options = [
			"Use text input from console",     # 0
			"Show output image after saving",  # 1
			"Repeat input file in image",      # 2
			"Get lenght of hidden bits"        # 3
		]
		selected = pick(options, title, multiselect=True)
		selected_advOpt = { index: option for option, index in selected }
		if len(selected) > 0:
			print(f"{Fore.BLUE}{title}{Fore.RESET}\n{Fore.RESET}-", "\n- ".join([ option.lower() for option, _ in selected ]))
		else:
			print(f"{Fore.BLUE}{title}{Fore.RESET}{Style.DIM} --")
		
		# options: read multiline text from console input
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
		
		# select: advanced options
		bitPatternList, colorPatternList = advancedOptions_for_setPatterns()
		
		# get valid file paths without " or '
		inputFormatter = lambda prompt: input(f"{Fore.BLUE}{prompt}:\t{Fore.RESET}").replace('"', '').replace("'", "")
		while not os.path.isfile((inputImagePath := inputFormatter("Input image path"))): pass
		while not os.access(os.path.dirname((outputImagePath := inputFormatter("Output image path"))), os.W_OK): pass
		if not selected_advOpt.get(0):
			while not os.path.isfile((inputImagePath := inputFormatter("Input file path"))): pass
		else:
			inputFilePath = consoleInputPath
		
		# option: get lenght of hidden bits
		if selected_advOpt.get(3):
			lenght = len(file2BitArray(inputFilePath))
			print(f"{Fore.CYAN}Lenght of hidden bits: {Fore.RESET}{lenght}")
		
		# hide file in image
		error = hideFileInImage(
			inputImagePath,
			outputImagePath,
			inputFilePath,
			# options: show, repeat, bitPattern, colorPattern
			show = bool(selected_advOpt.get(1)),
			repeat = bool(selected_advOpt.get(2)),
			bitPattern = bitPatternList,
			colorPattern = colorPatternList
		)
		print(f"{Fore.RED}file could not be saved" if error else f"{Fore.GREEN}file saved")
	
	# action: seek
	elif option == "Seek":
		# select: options
		title = "Options:"
		options = [
			"Show extracted file (image / text)",   # 0
			"Set lenght of hidden bits"             # 1
		]
		selected = pick(options, title, multiselect=True)
		selected_advOpt = { index: option for option, index in selected }
		if len(selected) > 0:
			print(f"{Fore.BLUE}{title}{Fore.RESET}\n{Fore.RESET}-", "\n- ".join([ option.lower() for option, _ in selected ]))
		else:
			print(f"{Fore.BLUE}{title}{Fore.RESET}{Style.DIM} --")
		
		# options: set lenght of hidden bits
		if selected_advOpt.get(1):
			while not (lenghtInput := input(f"{Fore.BLUE}Lenght of hidden bits: {Fore.RESET}")).isdigit():
				pass
			lenght = int(lenghtInput)
		else:
			lenght = None

		# select: advanced options
		bitPatternList, colorPatternList = advancedOptions_for_setPatterns()
		
		# get valid file paths without " or '
		inputFormatter = lambda prompt: input(f"{Fore.BLUE}{prompt}:\t{Fore.RESET}").replace('"', '').replace("'", "")
		while not os.path.isfile((inputImagePath := inputFormatter("Input image path"))): pass
		while not os.access(os.path.dirname((outputFilePath := inputFormatter("Output file path"))), os.W_OK): pass
		
		# seek file in image
		error = seekFileInImage(
			inputImagePath,
			outputFilePath,
			# options: bitPattern, colorPattern, lenght
			bitPattern = bitPatternList,
			colorPattern = colorPatternList,
			lenght = lenght
		)
		print(f"{Fore.RED}file could not be saved" if error else f"{Fore.GREEN}file saved")
		
		# options: show extracted file
		if selected_advOpt.get(0):
			# try for text
			try:
				with open(outputFilePath, "r", encoding="utf-8") as fobj:
					extractedText = fobj.read( lenght//8 if lenght else 100 )
				print(f"{Fore.CYAN}Extracted Text:\n{Fore.RESET}{extractedText}...")
			except UnicodeDecodeError:
				print(f"{Fore.RED}can't open as text file")
			except Exception as exc:
				raise exc
			# try for image
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
