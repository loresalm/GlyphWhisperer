import imageio.v2 as iio
import numpy as np
from skimage import measure
import utils as ut
import os

# ================= CONFIG =================
FONT_NAME = "BitmapFont"
OUTPUT_OTF = "outputs/section_test.otf"
UFO_PATH = "outputs/section_test.ufo"
GLYPH_SET = "ABCDEFGHIJKLMNOPQRSTUVW"
OUT_DIR = "outputs/glyphgen/best"

# ==========================================


def draw_glyph_from_bitmap(pen, png_path, configs):
    img = iio.imread(png_path, mode="L") < 128
    contours = measure.find_contours(img, 0.5)

    # Flatten all points to get bounds
    all_pts = np.vstack(contours)
    min_y, min_x = all_pts.min(axis=0)
    max_y, max_x = all_pts.max(axis=0)

    w = max_x - min_x
    h = max_y - min_y

    glyph_w = configs["GLYPH_WIDTH"]
    glyph_h = configs["X_HEIGHT"]   # lowercase a

    scale = min(glyph_w / w, glyph_h / h)

    x_off = (glyph_w - w * scale) / 2
    y_off = (glyph_h - h * scale) / 2

    for c in contours:
        pts = [(
            float((x - min_x) * scale + x_off),
            float((y - min_y) * scale + y_off)
        ) for y, x in c]

        pen.moveTo(pts[0])
        for p in pts[1:]:
            pen.lineTo(p)

        if np.linalg.norm(c[0] - c[-1]) < 1.0:
            pen.closePath()


configs, font = ut.setup(FONT_NAME, OUTPUT_OTF, UFO_PATH)

# === Generate Glyphs with Unicode values ===
for char in GLYPH_SET:
    print(f"Processing glyph: {char}")
    glyph = ut.setup_glyph(char, configs)

    PNG_PATH = os.path.join(OUT_DIR, f"{char}.png")

    pen = glyph.getPen()
    draw_glyph_from_bitmap(pen, PNG_PATH, configs)
    font.addGlyph(glyph)

font = ut.make_req_glyphs(font, configs)
ut.make_save_font(font, configs)
