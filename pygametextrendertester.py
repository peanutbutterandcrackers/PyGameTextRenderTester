import imagehash
from PIL import Image

def imagesAreSimilar(Image1, Image2, DISSIMILARITY_THRESHOLD=0):
	"""Return a boolean as to whether or not two supplied images are similar
	based on the DISSIMILARITY_THRESHOLD (default: 0) supllied.
	"""

	Image1_Hash = imagehash.phash(Image.open(Image1), hash_size=16, highfreq_factor=8)
	Image2_Hash = imagehash.phash(Image.open(Image2), hash_size=16, highfreq_factor=8)
	Dissimilarity = Image1_Hash - Image2_Hash

	if Dissimilarity <= DISSIMILARITY_THRESHOLD:
		return True
	else:
		return False
