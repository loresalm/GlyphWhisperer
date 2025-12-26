import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# === Helper: render centered glyph in a rectangle ===
def render_glyph(glyph, size, font_path, GLYPH_DIR):
    canvas = Image.new("L", size, 255)
    draw = ImageDraw.Draw(canvas)

    font_size = size[0] * 2
    font = ImageFont.truetype(font_path, font_size)

    bbox = draw.textbbox((0, 0), glyph, font=font)
    gw, gh = bbox[2] - bbox[0], bbox[3] - bbox[1]

    scale = min(size[0] / gw, size[1] / gh)
    font = ImageFont.truetype(font_path, int(font_size * scale))

    bbox = draw.textbbox((0, 0), glyph, font=font)
    gw, gh = bbox[2] - bbox[0], bbox[3] - bbox[1]

    tx = (size[0] - gw) // 2 - bbox[0]
    ty = (size[1] - gh) // 2 - bbox[1]

    draw.text((tx, ty), glyph, fill=0, font=font)

    glyph_bin = np.array(canvas)
    canvas.save(os.path.join(GLYPH_DIR, "glyph_reference.png"))
    glyph_black_ratio = np.sum(glyph_bin == 0) / (size[0] * size[1])
    return glyph_bin, glyph_black_ratio


def preprocess_source(INPUT_IMAGE, TRSH, OUT_DIR):
    # === Load and threshold image ===
    img = Image.open(INPUT_IMAGE).convert("L")
    img_np = np.array(img) / 255.0
    img_bin = (img_np > TRSH).astype(np.uint8) * 255
    Image.fromarray(img_bin).save(os.path.join(OUT_DIR, "thresholded.png"))
    h_img, w_img = img_bin.shape
    return img_bin, h_img, w_img


def select_smples(NSAMP, RECT_W, RECT_H, img_bin, h_img, w_img,
                  glyph_black_ratio, BLACK_DEV, GLYPH_DIR):
    # === Randomly sample rectangles matching black pixel ratio ===
    selected_samples = []
    for i in range(NSAMP):
        x0 = random.randint(0, w_img - RECT_W)
        y0 = random.randint(0, h_img - RECT_H)
        crop = img_bin[y0:y0+RECT_H, x0:x0+RECT_W]

        crop_black_ratio = np.sum(crop == 0) / (RECT_W * RECT_H)
        if abs(crop_black_ratio - glyph_black_ratio) > BLACK_DEV:
        # if crop_black_ratio - glyph_black_ratio < 0:
            continue
        else:
            selected_samples.append((crop, (x0, y0)))
            idx = len(selected_samples)
            Image.fromarray(crop).save(os.path.join(GLYPH_DIR, f"selected_crop_{idx}.png"))
    if len(selected_samples) == 0:
        print("Warning: No samples selected for this glyph.")
    return selected_samples


def compute_similarity(selected_samples, glyph_bin, OUT_DIR, GLYPH):
    best_dir = os.path.join(OUT_DIR, "best")
    os.makedirs(best_dir, exist_ok=True)
    # === Compute similarity only on selected rectangles ===
    scores = []
    for crop, pos in selected_samples:
        sim = np.mean(np.abs(crop/255 - glyph_bin/255))  # pixel-wise mean absolute difference
        scores.append((sim, crop, pos))
        scores.sort(key=lambda x: x[0])
        sim, crop, pos = scores[0]
        Image.fromarray(crop).save(os.path.join(best_dir, f"{GLYPH}.png"))
    return scores[0]


def pipeline(GLYPH, img_bin, h_img, w_img, NSAMP, RECT_W, RECT_H,
             OUT_DIR, BLACK_DEV, FONT_PATH, GLYPH_DIR):
    # === Render glyph once for comparison ===
    print(f"Processing glyph: {GLYPH}")
    glyph_bin, glyph_black_ratio = render_glyph(GLYPH, (RECT_W, RECT_H),
                                                FONT_PATH, GLYPH_DIR)

    selected_samples = select_smples(NSAMP, RECT_W, RECT_H, img_bin,
                                     h_img, w_img, glyph_black_ratio,
                                     BLACK_DEV, GLYPH_DIR)

    best = compute_similarity(selected_samples, glyph_bin, OUT_DIR, GLYPH)

    return best


# === Configuration ===
INPUT_IMAGE = "inputs/cros_sect.png"

TRSH = 0.6
NSAMP = 300
RECT_H, RECT_W = 200, 200
OUT_DIR = "outputs/glyphgen/"
BLACK_DEV = 0.4  # max allowed deviation of black pixel ratio
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # adjust as needed

os.makedirs(OUT_DIR, exist_ok=True)


GLYPH_SET = "ABCDEFGHIJKLMNOPQRSTUVW"

img_bin, h_img, w_img = preprocess_source(INPUT_IMAGE, TRSH, OUT_DIR)
for GLYPH in GLYPH_SET:
    GLYPH_DIR = os.path.join(OUT_DIR, GLYPH)
    os.makedirs(GLYPH_DIR, exist_ok=True)
    pipeline(GLYPH, img_bin, h_img, w_img, NSAMP, RECT_W, RECT_H,
             OUT_DIR, BLACK_DEV, FONT_PATH, GLYPH_DIR)
