#!/usr/bin/env python2

from gimpfu import *
from time import time
from os import getcwd

def create_text_layer(drawable, text_color, text_string, font, font_size, draw_on=None):
	# foreground color is used to fill the foreground layer
	if tuple(pdb.gimp_context_get_foreground()) != tuple((i*255 for i in text_color)):
		gimp.set_foreground(text_color)
	text_layer = pdb.gimp_text_fontname(drawable, draw_on, 0, 0, text_string, 10, True, font_size, PIXELS, font)
	return text_layer

def create_background_layer(drawable, bg_color, make_transparent=False):
	# Background color is used to fill the background layer
	if tuple(pdb.gimp_context_get_background()) != tuple((i*255 for i in bg_color)):
		gimp.set_background(bg_color)
	background_layer = pdb.gimp_layer_new(drawable, drawable.width, drawable.height, RGBA_IMAGE, "backdrop", 100.0, LAYER_MODE_NORMAL)
	pdb.gimp_image_insert_layer(drawable, background_layer, None, pdb.gimp_image_get_layers(drawable)[0]) # backdrop always goes at the bottom
	if not make_transparent:
		pdb.gimp_drawable_fill(background_layer, FILL_BACKGROUND)
	return background_layer

def render_text(text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight, workdir):
	img = gimp.Image(imgwidth, imgheight, RGB)

	text_layer = create_text_layer(img, textcolor, text, font, textsize)
	background = create_background_layer(img, backgroundcolor)
	text_layer_center = (text_layer.width//2, text_layer.height//2)
	image_center = (pdb.gimp_image_width(img)//2, pdb.gimp_image_height(img)//2)
	pdb.gimp_layer_set_offsets(text_layer, image_center[0]-text_layer_center[0], image_center[1]-text_layer_center[1])
	merged_layer = pdb.gimp_image_merge_down(img, text_layer, CLIP_TO_IMAGE)

	filename = '{}/gimp_rendering_{}.png'.format(workdir, time())
	pdb.gimp_file_save(img, merged_layer, filename, '?')

register(
	"python_fu_render_text_pygame_test",
	"Pygame Test Text Render",
	"A plugin to generate text to compare with pygame font renderings",
	"Prafulla Giri", "Prafulla Giri", "2019",
	"RenderText",
	"",
	[
		(PF_TEXT, "text", "Text", ""),
		(PF_SPINNER, "textsize", "Font Size", 50, (1, 3000, 1)),
		(PF_COLOR, "textcolor", "Text Color", (1.0, 1.0, 1.0)),
		(PF_FONT, "font", "Font-Face", "Sans"),
		(PF_COLOR, "backgroundcolor", "Background Color", (0.0, 0.0, 0.0)),
		(PF_INT, "imgwidth", "Image Width", 400),
		(PF_INT, "imgheight", "Image Height", 300),
		(PF_TEXT, "workdir", "Work Dir", "{}".format(getcwd()))
	],
	[],
	render_text,
	menu="<Image>/Filters/Custom"
)

main()
