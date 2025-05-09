
import utils as ut
import art_utils as aut

import random
from ufoLib2 import Font
from ufoLib2.objects import Glyph
import subprocess
import os
import math

# === Configuration ===
GLYPH_SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:!?()[]{}@#$%&*-_+=<>/\\|"
FONT_NAME = "CircleFont"
OUTPUT_OTF = "outputs/circlefont.otf"
UFO_PATH = "outputs/circlefont.ufo"

configs, font = ut.setup(FONT_NAME, OUTPUT_OTF, UFO_PATH)

# === Generate Glyphs with Unicode values ===
for char in GLYPH_SET:
    glyph = ut.setup_glyph(char, configs)

    pen = glyph.getPen()
    aut.create_multi_circle_glyph(pen, char, configs, num_circles=3)
    aut.create_random_stroked_lines_glyph(pen, char, configs, num_lines=4)
    font.addGlyph(glyph)

font = ut.make_req_glyphs(font, configs)
ut.make_save_font(font, configs)
