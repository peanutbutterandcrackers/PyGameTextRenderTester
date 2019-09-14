import subprocess, shutil

PLUGIN='pythonfu_gimp_text_renderer.py'

def init():

	HOME_DIR=shutil.os.path.expanduser('~')
	MODULE_PATH=shutil.os.path.dirname(__file__)
	PLUGIN_PATH=shutil.os.path.join(MODULE_PATH, PLUGIN)

	GIMP_DIRECTORY_LOOKUP_CMD='(python-fu-eval RUN-NONINTERACTIVE "print gimp.directory")'
	GIMP_DIRECTORY = subprocess.check_output(['gimp-console', '--no-data', '--batch', GIMP_DIRECTORY_LOOKUP_CMD, '--batch', '(gimp-quit 0)'],
                                             stderr=subprocess.DEVNULL).decode().strip()
	GIMP_PLUGIN_DIR=shutil.os.path.join(HOME_DIR, GIMP_DIRECTORY, 'plug-ins')

	shutil.copy2(PLUGIN_PATH, GIMP_PLUGIN_DIR)
	shutil.os.chmod(shutil.os.path.join(GIMP_PLUGIN_DIR, PLUGIN), 0o755)

def render(text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight):
	GIMP_RENDER_CMD = '(python-fu-gimp-text-renderer RUN-NONINTERACTIVE "{}" {} "{}" "{}" "{}" {} {} "{}")'.format(
                              text, textsize, textcolor, font, backgroundcolor, imgwidth, imgheight, shutil.os.getcwd())
	return_value = subprocess.call(['gimp-console', '--no-data', '--batch', GIMP_RENDER_CMD, '--batch', '(gimp-quit 0)']
                                   , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	assert return_value == 0, "Something went wrong"

init()
