def render_PyGame(text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight):
	import pygame, time

	pygame.init()
	DISPLAYSURF = pygame.display.set_mode((imgwidth, imgheight))

	fontObj = pygame.font.SysFont(font, textsize)
	textSurfaceObj = fontObj.render(text, True, textcolor)
	textRectObj = textSurfaceObj.get_rect()
	textRectObj.center = (imgwidth//2, imgheight//2)

	DISPLAYSURF.fill(backgroundcolor)
	DISPLAYSURF.blit(textSurfaceObj, textRectObj)
	outputfilename = 'pygame_rendering_{}.png'.format(time.time())
	pygame.image.save(DISPLAYSURF, outputfilename)
	pygame.quit()

	return outputfilename

def render_GIMP_init():
	import shutil
	# TODO: Make sure this works for versions of gimp other than 2.10 as well
	PLUGIN='gimp_render_text_image.py'
	HOME_DIR=shutil.os.path.expanduser('~')
	GIMP_PLUGIN_DIR=shutil.os.path.join(HOME_DIR, '.config/GIMP/2.10/plug-ins')
	shutil.copy2(PLUGIN, GIMP_PLUGIN_DIR)
	shutil.os.chmod(shutil.os.path.join(GIMP_PLUGIN_DIR, PLUGIN), 0o755)

def render_GIMP(text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight):
	import subprocess, shutil
	gimp_render_cmd = '(python-fu-render-text-pygame-test RUN-NONINTERACTIVE "{}" {} "{}" "{}" "{}" {} {} "{}")'.format(
				text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight, shutil.os.getcwd())
	return_value = subprocess.call(['gimp-console', '--batch', gimp_render_cmd, '--batch', '(gimp-quit 0)'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	assert return_value == 0, "Something went wrong"
