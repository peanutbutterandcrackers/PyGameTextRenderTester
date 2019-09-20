from renderers.gimp import gimp_renderer
from renderers.pygame import pygame_renderer

from pygame.font import match_font

def render(engine, text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight):
	"""Render a PNG using the given 'engine', based on the given parameters.
       'engine' can be either 'gimp' or 'pygame'.
    """
	if match_font(font) == None:
		raise FileNotFoundError("The specified font '{}' could not be found.".format(font))

	renderer = eval('{}_renderer'.format(engine.lower()))
	renderer.render(text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight)
