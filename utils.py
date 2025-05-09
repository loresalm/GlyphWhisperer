from ufoLib2 import Font  # type: ignore
from ufoLib2.objects import Glyph  # type: ignore
import subprocess
import os


def setup(FONT_NAME, OUTPUT_OTF, UFO_PATH):
    configs = {
        "OUTPUT_OTF": OUTPUT_OTF,
        "UFO_PATH": UFO_PATH,
        "GLYPH_WIDTH": 600,
        "FONT_SIZE": 1000,
        "ASCENDER": 800,
        "DESCENDER": -200,
        "X_HEIGHT": 500,
        "CAP_HEIGHT": 700
    }

    # === Initialize Font with proper metrics ===
    font = Font()
    font.info.familyName = FONT_NAME
    font.info.styleName = "Regular"
    font.info.versionMajor = 1
    font.info.versionMinor = 0
    font.info.unitsPerEm = configs["FONT_SIZE"]
    font.info.ascender = configs["ASCENDER"]
    font.info.descender = configs["DESCENDER"]
    font.info.xHeight = configs["X_HEIGHT"]
    font.info.capHeight = configs["CAP_HEIGHT"]

    # Essential font attributes for proper rendering
    font.info.openTypeHheaAscender = configs["ASCENDER"]
    font.info.openTypeHheaDescender = configs["DESCENDER"]
    font.info.openTypeHheaLineGap = 200
    font.info.openTypeOS2TypoAscender = configs["ASCENDER"]
    font.info.openTypeOS2TypoDescender = configs["DESCENDER"]
    font.info.openTypeOS2TypoLineGap = 200
    font.info.openTypeOS2WinAscent = configs["ASCENDER"]
    font.info.openTypeOS2WinDescent = abs(configs["DESCENDER"])

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

    # Set OS/2 Type (bit 3: Subsetting allowed,
    # bit 8: Embedding allowed, bit 9: for preview & print embedding)
    font.info.openTypeOS2Type = [3, 8, 9]
    return configs, font


def setup_glyph(char, configs):
    glyph = Glyph(name=char)
    glyph.width = configs["GLYPH_WIDTH"]

    # Set the unicode value for the glyph
    glyph.unicodes = [ord(char)]
    return glyph


def make_req_glyphs(font, configs):
    # === Add Required Glyphs ===
    # .notdef glyph (essential)
    notdef = Glyph(name=".notdef")
    notdef.width = configs["GLYPH_WIDTH"]
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
    space.width = configs["GLYPH_WIDTH"] // 2
    space.unicodes = [0x0020]  # Unicode for space
    font.addGlyph(space)

    # Add tab glyph
    tab = Glyph(name="tab")
    tab.width = configs["GLYPH_WIDTH"] * 2
    tab.unicodes = [0x0009]  # Unicode for tab
    font.addGlyph(tab)

    # NULL glyph
    null = Glyph(name="NULL")
    null.width = 0
    null.unicodes = [0x0000]  # Unicode for NULL
    font.addGlyph(null)

    # CR glyph
    cr = Glyph(name="CR")
    cr.width = configs["GLYPH_WIDTH"] // 2
    cr.unicodes = [0x000D]  # Unicode for CR
    font.addGlyph(cr)
    return font


def make_save_font(font, configs):
    # === Save to UFO and Overwrite if Exists ===
    if os.path.exists(configs["UFO_PATH"]):
        import shutil
        shutil.rmtree(configs["UFO_PATH"])

    print(f"Saving UFO font to {configs['UFO_PATH']}...")
    font.save(configs["UFO_PATH"], overwrite=True)

    # === Use fontmake to generate OTF ===
    try:
        print(f"Generating OTF font from {configs['UFO_PATH']}...")
        subprocess.run([
            "fontmake",
            "-u", configs["UFO_PATH"],
            "-o", "otf",
            "--output-path", configs["OUTPUT_OTF"],
            "--production-names"       # Use production glyph names
        ], check=True)
        print(f"Font successfully generated: {configs['OUTPUT_OTF']}")

        # Verify the file was created
        if os.path.exists(configs["OUTPUT_OTF"]):
            print(f"File - size: {os.path.getsize(configs['OUTPUT_OTF'])} byt")
        else:
            print("Warning: Output file not found!")

    except subprocess.CalledProcessError as e:
        print(f"Failed to generate OTF: {e}")
        print(
            f"cmd output: {e.output if hasattr(e, 'output') else 'No output'}")
