# PyGameTextRenderTester
This program essentially tests whether or not texts in various languages are being rendered correctly by pygame.

## How does this work?
Essentially, this renders the same text-on-a-solid-background `png` using `pygame` and `gimp` using the exact same font, color, font-size, dimensions, etc, and checks the similarity of the rendered `png`s using perceptual hash function (allowing for a slight dissimilarity threshold).

## Usage:
`$ ./main.py`

## Dependencies:
This mostly uses the standard python library modules but there are a few other modules/libraries and fonts that are required:
1. `GIMP` (also `gimp-python`, if it is not installed with GIMP)
2. `pillow` (`pip install pillow`)
3. `imagehash` (`pip install ImageHash`)
4. `pygame` (`pip install pygame`), obviously.

## words.json:
To check the rendering of other languages/scripts, all one needs to do is to add the words to `words.json` file. The file is simple and the syntax is:
```json
[	
	{
		"script": "<SCRIPT - 'Devanagari', 'Latin', etc.>",
		"font": "<Font to render the words with. Should be pre-installed>",
		"words": [
			"WORD1",
			"WORD2",
                        "WORDS CAN EVEN HAVE SPACES"
			]
	}
]
```

## settings.py:
This file specifies the image dimensions, text size, text colour, background colour, etc.
