import pygame, time

def render(text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight):
	pygame.font.init()
	MAINSURF = pygame.Surface((imgwidth, imgheight))
	MAINSURF.fill(backgroundcolor)

	useAntialiasing = True
	fontObj = pygame.font.SysFont(font, textsize)
	textSurfaceObj = fontObj.render(text, useAntialiasing, textcolor)
	textRectObj = textSurfaceObj.get_rect()
	destination = (imgwidth//2 - textRectObj.width//2, imgheight//2 - textRectObj.height//2)
	MAINSURF.blit(textSurfaceObj, destination)

	outputfilename = 'pygame_rendering_{}.png'.format(time.time())
	pygame.image.save(MAINSURF, outputfilename)
	pygame.quit()

	return outputfilename
