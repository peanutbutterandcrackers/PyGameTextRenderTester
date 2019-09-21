import atexit
import subprocess, shutil

from time import sleep

PLUGIN='pythonfu_gimp_text_renderer.py'

# If this module is being called from the context of a package, then
# show_init_progress; else: let the user choose
_isPartOfAPackage = __package__ not in ['', None]

def init(show_init_progress):
	global GIMP_PLUGIN_DIR

	HOME_DIR=shutil.os.path.expanduser('~')
	MODULE_PATH=shutil.os.path.dirname(__file__)
	PLUGIN_PATH=shutil.os.path.join(MODULE_PATH, PLUGIN)

	GIMP_DIRECTORY_LOOKUP_CMD='(python-fu-eval RUN-NONINTERACTIVE "print gimp.directory")'
	P = subprocess.Popen(['gimp-console', '--no-data', '--batch', GIMP_DIRECTORY_LOOKUP_CMD, '--batch', '(gimp-quit 0)'],
                                             stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)

	if show_init_progress:
		print()
		progress_marker = '.'
		progress_str = ''
		while P.poll() == None:
			if len(progress_str) > 4:
				progress_str = progress_str.replace(progress_marker, ' ')
				print('Initializing GIMP renderer{}\r'.format(progress_str), end='', flush=True)
				progress_str = ''
			print('Initializing GIMP renderer{}\r'.format(progress_str), end='', flush=True)
			progress_str += progress_marker
			sleep(0.5)
		print()

	GIMP_DIRECTORY = P.stdout.read(-1).decode().strip()

	GIMP_PLUGIN_DIR=shutil.os.path.join(HOME_DIR, GIMP_DIRECTORY, 'plug-ins')

	shutil.copy2(PLUGIN_PATH, GIMP_PLUGIN_DIR)
	shutil.os.chmod(shutil.os.path.join(GIMP_PLUGIN_DIR, PLUGIN), 0o755)

def stop():
	shutil.os.remove(shutil.os.path.join(GIMP_PLUGIN_DIR, PLUGIN))

def render(text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight):
	GIMP_RENDER_CMD = '(python-fu-gimp-text-renderer RUN-NONINTERACTIVE "{}" {} "{}" "{}" "{}" {} {} "{}")'.format(
                              text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight, shutil.os.getcwd())
	subprocess.call(['gimp-console', '--no-data', '--batch', GIMP_RENDER_CMD, '--batch', '(gimp-quit 0)']
                                   , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __package__ not in ['', None]:
	init(show_init_progress=_isPartOfAPackage)
	atexit.register(stop)
