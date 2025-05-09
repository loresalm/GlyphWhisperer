import random
import math


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
def create_multi_circle_glyph(pen, char,  configs, num_circles=3):
    """Creates multiple random circles for each character to make it unique."""

    # Set boundary and size parameters based on character type
    if char.isupper() and char.isalpha():
        y_min = 200
        y_max = configs["CAP_HEIGHT"]
        base_radius = configs["CAP_HEIGHT"] / 5
    elif char.islower() and char.isalpha():
        y_min = 100
        y_max = configs["X_HEIGHT"]
        base_radius = configs["X_HEIGHT"] / 5
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
        x_center = random.randint(100, configs["GLYPH_WIDTH"] - 100)
        y_center = random.randint(y_min, y_max)

        # Randomize radius within reasonable bounds
        radius_variance = 0.5 + random.random()  # Between 0.5 and 1.5
        radius = int(base_radius * radius_variance)

        # Ensure circles stay within glyph boundaries
        radius = min(radius, 200)  # Cap maximum radius

        # Draw the circle
        draw_circle(pen, x_center, y_center, radius)


def draw_line_with_stroke(pen, x1, y1, x2, y2, stroke_width=15):
    """
    Draws a line between two points with specified stroke width.
    This creates a rectangular path representing a line with thickness.
    Parameters:
    - pen: The pen object from the glyph
    - x1, y1: Start point coordinates
    - x2, y2: End point coordinates
    - stroke_width: Width of the stroke (thickness of the line)
    """
    # Calculate the angle of the line
    angle = math.atan2(y2 - y1, x2 - x1)

    # Calculate the perpendicular angle (90 degrees offset)
    perp_angle = angle + math.pi / 2

    # Calculate half stroke offset
    half_stroke = stroke_width / 2
    dx_perp = half_stroke * math.cos(perp_angle)
    dy_perp = half_stroke * math.sin(perp_angle)

    # Calculate the four corners of the rectangle
    # Top left
    tlx = x1 + dx_perp
    tly = y1 + dy_perp
    # Top right
    tr_x = x2 + dx_perp
    tr_y = y2 + dy_perp
    # Bottom right
    brx = x2 - dx_perp
    bry = y2 - dy_perp
    # Bottom left
    blx = x1 - dx_perp
    bly = y1 - dy_perp

    # Draw the rectangular path
    pen.moveTo((tlx, tly))
    pen.lineTo((tr_x, tr_y))
    pen.lineTo((brx, bry))
    pen.lineTo((blx, bly))
    pen.closePath()


def create_random_stroked_lines_glyph(pen, char, configs, num_lines=4):
    """
    Creates multiple random lines,
    with varying stroke weights for each character.

    Parameters:
    - pen: The pen object from the glyph
    - char: The character to create the glyph for
    - num_lines: Number of lines to draw
    """
    # Set boundary and size parameters based on character type
    if char.isupper() and char.isalpha():
        y_min = 200
        y_max = configs["CAP_HEIGHT"]
        base_stroke = 25
    elif char.islower() and char.isalpha():
        y_min = 100
        y_max = configs["X_HEIGHT"]
        base_stroke = 20
    elif char.isdigit():
        y_min = 150
        y_max = 650
        base_stroke = 22
    else:  # Symbol
        y_min = 150
        y_max = 550
        base_stroke = 18

    # Create a deterministic but unique seed for each character
    # This ensures the same character always gets the same pattern
    char_seed = ord(char) * 1000
    random.seed(char_seed)

    # Glyph width - adjust as needed
    glyph_width = 600

    # Draw multiple lines with varying stroke weights
    for i in range(num_lines):
        # Randomize start and end points within bounds
        x1 = random.randint(50, glyph_width - 50)
        y1 = random.randint(y_min, y_max)

        # Determine line length and direction
        line_length = random.randint(100, 400)
        angle = random.uniform(0, 2 * math.pi)  # Random angle in radians

        # Calculate end point
        x2 = int(x1 + line_length * math.cos(angle))
        y2 = int(y1 + line_length * math.sin(angle))

        # Ensure endpoints are within glyph boundaries
        x2 = max(20, min(x2, glyph_width - 20))
        y2 = max(20, min(y2, y_max))

        # Randomize stroke width
        stroke_variance = 0.6 + random.random() * 0.8  # Between 0.6 and 1.4
        stroke_width = int(base_stroke * stroke_variance)

        # Draw the stroked line
        draw_line_with_stroke(pen, x1, y1, x2, y2, stroke_width)
