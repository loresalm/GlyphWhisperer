import random
from ufoLib2 import Font
from ufoLib2.objects import Glyph
import subprocess

# === Configuration ===
GLYPH_SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:!?()[]{}@#$%&*-_+=<>/\\|"
NUM_SHAPES_PER_GLYPH = 1
FONT_NAME = "GlyphWhisperer"
OUTPUT_OTF = "glyphwhisperer.otf"
UFO_PATH = "glyphwhisperer.ufo"
GLYPH_WIDTH = 600
FONT_SIZE = 1000
ASCENDER = 800
DESCENDER = -200
X_HEIGHT = 500
CAP_HEIGHT = 700

# === Initialize Font with proper metrics ===
font = Font()
font.info.familyName = FONT_NAME
font.info.styleName = "Regular"
font.info.unitsPerEm = FONT_SIZE
font.info.ascender = ASCENDER
font.info.descender = DESCENDER
font.info.xHeight = X_HEIGHT
font.info.capHeight = CAP_HEIGHT

# === Function to Generate Simple Closed Shapes (Triangle or Rectangle) ===
def random_closed_shape(pen, width, height, is_uppercase=False, is_lowercase=False):
    """Draws a simple closed shape within the glyph bounding box, with position based on case."""
    shape_type = random.choice(['triangle', 'rectangle'])
    
    # Adjust vertical positioning based on character case
    if is_uppercase:
        # Position uppercase letters between baseline and cap height
        y_min = 0
        y_max = CAP_HEIGHT
    elif is_lowercase:
        # Position lowercase letters between baseline and x-height
        y_min = 0
        y_max = X_HEIGHT
    else:
        # For numbers and symbols, use the full range
        y_min = DESCENDER
        y_max = ASCENDER
    
    # Make sure we get visible shapes with reasonable dimensions
    min_size = 50
    
    if shape_type == 'triangle':
        # Random triangle with purposeful positioning
        x1, y1 = random.randint(50, width-50), random.randint(y_min, y_max)
        x2, y2 = random.randint(50, width-50), random.randint(y_min, y_max)
        x3, y3 = random.randint(50, width-50), random.randint(y_min, y_max)
        
        pen.moveTo((x1, y1))
        pen.lineTo((x2, y2))
        pen.lineTo((x3, y3))
        pen.closePath()
        
    elif shape_type == 'rectangle':
        # Safe calculation of rectangle dimensions
        x1 = random.randint(50, width-150)  # Ensure space for width
        
        # Ensure y1 has enough space above it
        max_y1 = y_max - min_size - 10
        if max_y1 <= y_min:
            max_y1 = y_max - 10  # Fallback if range is too small
            
        y1 = random.randint(y_min, max_y1) if max_y1 > y_min else y_min
        
        # Calculate safe dimensions
        max_width = width - x1 - 10
        rect_width = random.randint(min_size, max_width) if max_width > min_size else min_size
        
        max_height = y_max - y1 - 10
        rect_height = random.randint(min_size, max_height) if max_height > min_size else min_size
        
        x2 = x1 + rect_width
        y2 = y1 + rect_height
        
        pen.moveTo((x1, y1))
        pen.lineTo((x2, y1))
        pen.lineTo((x2, y2))
        pen.lineTo((x1, y2))
        pen.closePath()

# === Generate Glyphs ===
for char in GLYPH_SET:
    glyph = Glyph(char)
    glyph.width = GLYPH_WIDTH
    pen = glyph.getPen()
    
    # Determine character type
    is_uppercase = char.isupper() if char.isalpha() else False
    is_lowercase = char.islower() if char.isalpha() else False
    
    for _ in range(NUM_SHAPES_PER_GLYPH):
        random_closed_shape(pen, GLYPH_WIDTH, FONT_SIZE, is_uppercase, is_lowercase)
    
    font.addGlyph(glyph)

# === Add .notdef glyph (required for proper font functioning) ===
notdef = Glyph(".notdef")
notdef.width = GLYPH_WIDTH
pen = notdef.getPen()

# Simple rectangle for .notdef glyph
pen.moveTo((100, 100))
pen.lineTo((500, 100))
pen.lineTo((500, 800))
pen.lineTo((100, 800))
pen.closePath()

# Add an inner rectangle for the .notdef glyph
pen.moveTo((200, 200))
pen.lineTo((400, 200))
pen.lineTo((400, 700))
pen.lineTo((200, 700))
pen.closePath()

font.addGlyph(notdef)

# === Add space glyph (often required) ===
space = Glyph("space")
space.width = GLYPH_WIDTH // 2  # typically narrower than other glyphs
font.addGlyph(space)

# === Save to UFO and Overwrite if Exists ===
font.save(UFO_PATH, overwrite=True)

# === Compile to OTF using subprocess ===
try:
    subprocess.run([
        "fontmake",
        "-u", UFO_PATH,
        "-o", "otf",
        "--output-path", OUTPUT_OTF
    ], check=True)
    print(f"Font generated: {OUTPUT_OTF}")
except subprocess.CalledProcessError as e:
    print(f"Failed to generate OTF: {e}")