from renderers.gimp import gimp_renderer
from renderers.pygame import pygame_renderer

def render(engine, text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight):
	"""Render a PNG using the given 'engine', based on the given parameters.
       'engine' can be either 'gimp' or 'pygame'.
    """
	renderer = eval('{}_renderer'.format(engine.lower()))
	renderer.render(text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight)
