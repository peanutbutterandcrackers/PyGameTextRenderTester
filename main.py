#!/usr/bin/env python3
import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "True"

def rgb2hex(rgb):
	if len(rgb) == 3:
		r, g, b = rgb
	elif len(rgb) == 4:
		r, g, b, a = rgb
	return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)

def imagesAreSimilar(Image1, Image2, DISSIMILARITY_THRESHOLD=0):
	"""Return a boolean as to whether or not two supplied images are similar
	based on the DISSIMILARITY_THRESHOLD (default: 0) supllied.
	"""
	from PIL import Image
	import imagehash

	Image1_Hash = imagehash.phash(Image.open(Image1), hash_size=16, highfreq_factor=8)
	Image2_Hash = imagehash.phash(Image.open(Image2), hash_size=16, highfreq_factor=8)
	Dissimilarity = Image1_Hash - Image2_Hash

	if Dissimilarity <= DISSIMILARITY_THRESHOLD:
		return True
	else:
		return False

def render(engine, text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight):
	"""Render a PNG using the given 'engine', based on the given parameters.
	   'engine' can be either 'gimp' or 'pygame'.
	"""
	import renderers
	engine = engine.lower()
	if engine == 'pygame':
		renderers.render_PyGame(text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight)
	elif engine == 'gimp':
		renderers.render_GIMP(text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight)
	else:
		pass

def renderer_init(engine):
	"""Initialize the rendering engine"""
	import renderers
	if engine == 'gimp':
		renderers.render_GIMP_init()

def main():
	import json
	import settings
	import os, glob

	textsize = settings.TEXT_SIZE
	textcolor = settings.TEXT_COLOR
	imgwidth = settings.DISPLAYSURF_WIDTH
	imgheight = settings.DISPLAYSURF_HEIGHT
	backgroundcolor = settings.BACKGROUND_COLOR

	_file = open('text.json')
	json_data = json.load(_file)

	renderer_init('gimp')

	for data in json_data:
		font = data['font']
		for text in data['text']:
			print("Currently testing: '{}'".format(text))
			render('pygame', text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight)
			pygame_render = max(glob.glob('*'), key=os.path.getctime) 
			render('gimp', text, textsize, rgb2hex(textcolor), font, rgb2hex(backgroundcolor), imgwidth, imgheight)
			gimp_render = max(glob.glob('*'), key=os.path.getctime)
			if not imagesAreSimilar(pygame_render, gimp_render, DISSIMILARITY_THRESHOLD=5):
				print("Dissimilar Renderings: '{}' and '{}'".format(pygame_render, gimp_render))
				print("Text: {}".format(text))
				sys.exit(1)
		print("Successfully rendered {} script".format(data['script']))
	
	print("All tests passed successfully!")

if __name__ == '__main__':
	main()
