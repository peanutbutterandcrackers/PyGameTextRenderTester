#!/usr/bin/env python3

import glob, json, os, sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'

import settings
from renderers import renderer
from pygametextrendertester import imagesAreSimilar

def main():

	rgb2hex = lambda rgb : "#{0:02x}{1:02x}{2:02x}".format(*rgb)

	textsize = settings.TEXT_SIZE
	textcolor = settings.TEXT_COLOR
	imgwidth = settings.IMAGE_WIDTH
	imgheight = settings.IMAGE_HEIGHT
	backgroundcolor = settings.BACKGROUND_COLOR
	DISSIMILARITY_THRESHOLD = settings.DISSIMILARITY_THRESHOLD
	HASH_SIZE = settings.HASH_SIZE
	HIGHFREQ_FACTOR = settings.HIGHFREQ_FACTOR

	_file = open('text.json')
	json_data = json.load(_file)

	for data in json_data:
		font = data['font']
		print("\nTesting {} script:".format(data['script']))
		for text in data['text']:
			print("Currently testing: '{}'".format(text))
			renderer.render('pygame', text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight)
			pygame_render = max(glob.glob('*'), key=os.path.getctime) 
			renderer.render('gimp', text, textsize, rgb2hex(textcolor), font, rgb2hex(backgroundcolor), imgwidth, imgheight)
			gimp_render = max(glob.glob('*'), key=os.path.getctime)
			if not imagesAreSimilar(pygame_render, gimp_render, DISSIMILARITY_THRESHOLD, HASH_SIZE, HIGHFREQ_FACTOR):
				print("...\nFAILURE!!!\nDISSIMILAR RENDERS:'{}' and '{}'".format(pygame_render, gimp_render))
				print("TEXT: {}".format(text))
				print("EXITING.")
				sys.exit(1)
		print("Successfully rendered {} script".format(data['script']))

	print("All tests passed successfully!")

if __name__ == '__main__':
	main()
