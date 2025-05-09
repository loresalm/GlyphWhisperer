import random
from ufoLib2 import Font
from ufoLib2.objects import Glyph
import subprocess
import os
import math

# === Configuration ===
GLYPH_SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:!?()[]{}@#$%&*-_+=<>/\\|"
FONT_NAME = "CircleFont"
OUTPUT_OTF = "circlefont.otf"
UFO_PATH = "circlefont.ufo"
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
font.info.versionMajor = 1
font.info.versionMinor = 0
font.info.unitsPerEm = FONT_SIZE
font.info.ascender = ASCENDER
font.info.descender = DESCENDER
font.info.xHeight = X_HEIGHT
font.info.capHeight = CAP_HEIGHT

# Essential font attributes for proper rendering
font.info.openTypeHheaAscender = ASCENDER
font.info.openTypeHheaDescender = DESCENDER
font.info.openTypeHheaLineGap = 200
font.info.openTypeOS2TypoAscender = ASCENDER
font.info.openTypeOS2TypoDescender = DESCENDER
font.info.openTypeOS2TypoLineGap = 200
font.info.openTypeOS2WinAscent = ASCENDER
font.info.openTypeOS2WinDescent = abs(DESCENDER)

# PostScript specific attributes
font.info.postscriptUnderlinePosition = -100
font.info.postscriptUnderlineThickness = 50
font.info.postscriptFontName = f"{FONT_NAME}-Regular"
font.info.postscriptFullName = f"{FONT_NAME} Regular"

# Copyright and Identification
font.info.copyright = f"Copyright © 2025 {FONT_NAME}"
font.info.openTypeNameDesigner = "Font Designer"
font.info.openTypeNameDesignerURL = "https://example.com"
font.info.openTypeNameManufacturer = "Font Foundry"
font.info.openTypeNameManufacturerURL = "https://example.com"
font.info.openTypeNameLicense = "SIL Open Font License, Version 1.1"
font.info.openTypeNameLicenseURL = "https://scripts.sil.org/OFL"
font.info.openTypeNameVersion = "Version 1.000"
font.info.openTypeNameUniqueID = f"{FONT_NAME}-Regular"

# Define Unicode ranges (Basic Latin)
font.info.openTypeOS2UnicodeRanges = [0]  # Basic Latin
font.info.openTypeOS2CodePageRanges = [0, 1]  # Latin 1

# Weight class (Regular = 400)
font.info.openTypeOS2WeightClass = 400
font.info.openTypeOS2WidthClass = 5  # Medium (normal)

# OS/2 Vendor ID - 4 characters
font.info.openTypeOS2VendorID = "MYFT"

# Set OS/2 Type (bit 3: Subsetting allowed, bit 8: Embedding allowed, bit 9: for preview & print embedding)
font.info.openTypeOS2Type = [3, 8, 9]

# === Function to draw a single circle ===
def draw_circle(pen, x_center, y_center, radius):
    """Creates a single circle using Bezier curves."""
    # Magic number for control points: 0.552284749831
    c = 0.552284749831 * radius
    
    # Starting at the right midpoint of the circle
    pen.moveTo((x_center + radius, y_center))
    
    # Bottom-right quadrant
    pen.curveTo(
        (x_center + radius, y_center - c),
        (x_center + c, y_center - radius),
        (x_center, y_center - radius)
    )
    
    # Bottom-left quadrant
    pen.curveTo(
        (x_center - c, y_center - radius),
        (x_center - radius, y_center - c),
        (x_center - radius, y_center)
    )
    
    # Top-left quadrant
    pen.curveTo(
        (x_center - radius, y_center + c),
        (x_center - c, y_center + radius),
        (x_center, y_center + radius)
    )
    
    # Top-right quadrant
    pen.curveTo(
        (x_center + c, y_center + radius),
        (x_center + radius, y_center + c),
        (x_center + radius, y_center)
    )
    
    pen.closePath()

# === Function to create multiple random circles for each glyph ===
def create_multi_circle_glyph(pen, char, num_circles=3):
    """Creates multiple random circles for each character to make it unique."""
    
    # Set boundary and size parameters based on character type
    if char.isupper() and char.isalpha():
        y_min = 200
        y_max = CAP_HEIGHT
        base_radius = CAP_HEIGHT / 5
    elif char.islower() and char.isalpha():
        y_min = 100
        y_max = X_HEIGHT
        base_radius = X_HEIGHT / 5
    elif char.isdigit():
        y_min = 150
        y_max = 650
        base_radius = 100
    else:  # Symbol
        y_min = 150
        y_max = 550
        base_radius = 80
    
    # Create a deterministic but unique seed for each character
    # This ensures the same character always gets the same pattern
    char_seed = ord(char) * 1000
    random.seed(char_seed)
    
    # Draw multiple circles
    for i in range(num_circles):
        # Randomize position within bounds
        x_center = random.randint(100, GLYPH_WIDTH - 100)
        y_center = random.randint(y_min, y_max)
        
        # Randomize radius within reasonable bounds
        radius_variance = 0.5 + random.random()  # Between 0.5 and 1.5
        radius = int(base_radius * radius_variance)
        
        # Ensure circles stay within glyph boundaries
        radius = min(radius, 200)  # Cap maximum radius
        
        # Draw the circle
        draw_circle(pen, x_center, y_center, radius)

# === Generate Glyphs with Unicode values ===
for char in GLYPH_SET:
    glyph = Glyph(name=char)
    glyph.width = GLYPH_WIDTH
    
    # Set the unicode value for the glyph
    glyph.unicodes = [ord(char)]
    
    pen = glyph.getPen()
    create_multi_circle_glyph(pen, char, num_circles=3)
    font.addGlyph(glyph)

# === Add Required Glyphs ===
# .notdef glyph (essential)
notdef = Glyph(name=".notdef")
notdef.width = GLYPH_WIDTH
pen = notdef.getPen()
# Draw a box for .notdef
pen.moveTo((100, 100))
pen.lineTo((500, 100))
pen.lineTo((500, 700))
pen.lineTo((100, 700))
pen.closePath()
# Draw the cross
pen.moveTo((100, 100))
pen.lineTo((500, 700))
pen.moveTo((500, 100))
pen.lineTo((100, 700))
font.addGlyph(notdef)

# Space glyph (essential)
space = Glyph(name="space")
space.width = GLYPH_WIDTH // 2
space.unicodes = [0x0020]  # Unicode for space
font.addGlyph(space)

# Add tab glyph
tab = Glyph(name="tab")
tab.width = GLYPH_WIDTH * 2
tab.unicodes = [0x0009]  # Unicode for tab
font.addGlyph(tab)

# NULL glyph
null = Glyph(name="NULL")
null.width = 0
null.unicodes = [0x0000]  # Unicode for NULL
font.addGlyph(null)

# CR glyph
cr = Glyph(name="CR")
cr.width = GLYPH_WIDTH // 2
cr.unicodes = [0x000D]  # Unicode for CR
font.addGlyph(cr)

# === Save to UFO and Overwrite if Exists ===
if os.path.exists(UFO_PATH):
    import shutil
    shutil.rmtree(UFO_PATH)

print(f"Saving UFO font to {UFO_PATH}...")
font.save(UFO_PATH, overwrite=True)

# === Use fontmake to generate OTF ===
try:
    print(f"Generating OTF font from {UFO_PATH}...")
    subprocess.run([
        "fontmake",
        "-u", UFO_PATH,
        "-o", "otf",
        "--output-path", OUTPUT_OTF,
        "--production-names"       # Use production glyph names
    ], check=True)
    print(f"Font successfully generated: {OUTPUT_OTF}")
    
    # Verify the file was created
    if os.path.exists(OUTPUT_OTF):
        print(f"File exists and has size: {os.path.getsize(OUTPUT_OTF)} bytes")
    else:
        print("Warning: Output file not found!")
        
except subprocess.CalledProcessError as e:
    print(f"Failed to generate OTF: {e}")
    print(f"Command output: {e.output if hasattr(e, 'output') else 'No output available'}")