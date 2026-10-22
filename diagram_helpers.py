import os
import math
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1600
HEIGHT = 1100

# Fonts loader
def get_fonts():
    try:
        font_banner_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
        font_banner_proj = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
        font_banner_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
        font_heading = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
        font_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
        font_body_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
        font_small = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
        font_small_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11)
        font_small_italic = ImageFont.truetype("C:/Windows/Fonts/segoeuii.ttf", 11)
    except Exception:
        font_banner_title = ImageFont.load_default()
        font_banner_proj = ImageFont.load_default()
        font_banner_sub = ImageFont.load_default()
        font_heading = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_body_bold = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_small_bold = ImageFont.load_default()
        font_small_italic = ImageFont.load_default()

    return {
        "banner_title": font_banner_title,
        "banner_proj": font_banner_proj,
        "banner_sub": font_banner_sub,
        "heading": font_heading,
        "body": font_body,
        "body_bold": font_body_bold,
        "small": font_small,
        "small_bold": font_small_bold,
        "small_italic": font_small_italic
    }

# Standard Color Palette
COLOR_BORDER = (30, 41, 59)
COLOR_TEXT = (15, 23, 42)
COLOR_MUTED = (100, 116, 139)

COLOR_BANNER_BG = (224, 242, 254)      # Light sky blue
COLOR_BANNER_BORDER = (3, 105, 161)

# Pastel box colors
PALETTE_BLUE = {"fill": (239, 246, 255), "header": (191, 219, 254), "border": (30, 41, 59)}
PALETTE_GREEN = {"fill": (240, 253, 244), "header": (187, 247, 208), "border": (30, 41, 59)}
PALETTE_ORANGE = {"fill": (255, 247, 237), "header": (254, 215, 170), "border": (30, 41, 59)}
PALETTE_PINK = {"fill": (255, 241, 242), "header": (254, 205, 211), "border": (30, 41, 59)}
PALETTE_PURPLE = {"fill": (250, 245, 255), "header": (233, 213, 255), "border": (30, 41, 59)}
PALETTE_YELLOW = {"fill": (254, 252, 232), "header": (254, 240, 138), "border": (30, 41, 59)}
PALETTE_TEAL = {"fill": (240, 253, 250), "header": (153, 246, 228), "border": (30, 41, 59)}

# Create canvas
def create_canvas(w=WIDTH, h=HEIGHT):
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    return img, draw

# Top Banner matching friend's layout
def draw_top_banner(draw, number_and_title, project_name="Smart Assignment Tracker", subtitle=None, canvas_w=WIDTH):
    bw, bh = 650, 100
    bx = (canvas_w - bw) // 2
    by = 18
    # Banner rounded rectangle
    draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=8, fill=COLOR_BANNER_BG, outline=COLOR_BANNER_BORDER, width=2)
    
    fonts = get_fonts()
    # Number & Diagram Name
    draw.text((canvas_w // 2, by + 24), number_and_title, fill=COLOR_TEXT, font=fonts["banner_title"], anchor="mm")
    # Project Name
    draw.text((canvas_w // 2, by + 56), project_name, fill=COLOR_TEXT, font=fonts["banner_proj"], anchor="mm")
    # Subtitle
    if subtitle:
        draw.text((canvas_w // 2, by + 82), subtitle, fill=COLOR_TEXT, font=fonts["banner_sub"], anchor="mm")

# Draw Stick Figure Actor with colored circular head
def draw_actor(draw, x, y, name, head_color=(254, 224, 114), subtitle=None):
    r = 16
    fonts = get_fonts()
    # Head
    draw.ellipse([(x - r, y - 50), (x + r, y - 18)], fill=head_color, outline=COLOR_BORDER, width=2)
    # Spine
    draw.line([(x, y - 18), (x, y + 22)], fill=COLOR_BORDER, width=2)
    # Arms
    draw.line([(x - 26, y - 4), (x + 26, y - 4)], fill=COLOR_BORDER, width=2)
    # Legs
    draw.line([(x, y + 22), (x - 20, y + 58)], fill=COLOR_BORDER, width=2)
    draw.line([(x, y + 22), (x + 20, y + 58)], fill=COLOR_BORDER, width=2)
    # Labels
    draw.text((x, y + 74), name, fill=COLOR_TEXT, font=fonts["body_bold"], anchor="mm")
    if subtitle:
        draw.text((x, y + 90), subtitle, fill=COLOR_MUTED, font=fonts["small_italic"], anchor="mm")

# Draw dashed line
def draw_dashed_line(draw, x1, y1, x2, y2, color=COLOR_BORDER, width=2, dash=7, gap=5):
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    curr = 0
    while curr < dist:
        end = min(curr + dash, dist)
        draw.line([(x1 + curr * ux, y1 + curr * uy), (x1 + end * ux, y1 + end * uy)], fill=color, width=width)
        curr += dash + gap

# Draw Arrow
def draw_arrow(draw, x1, y1, x2, y2, color=COLOR_BORDER, open_arrow=True, size=10, width=2):
    angle = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - size * math.cos(angle - 0.4), y2 - size * math.sin(angle - 0.4))
    p2 = (x2 - size * math.cos(angle + 0.4), y2 - size * math.sin(angle + 0.4))
    if open_arrow:
        draw.line([p1, (x2, y2)], fill=color, width=width)
        draw.line([p2, (x2, y2)], fill=color, width=width)
    else:
        draw.polygon([(x2, y2), p1, p2], fill=(255, 255, 255), outline=color)

# Draw Class Box (3 compartments)
def draw_class_box(draw, x, y, w, title, stereotype=None, attributes=[], methods=[], palette=PALETTE_BLUE):
    fonts = get_fonts()
    header_h = 32 if not stereotype else 44
    attr_h = max(24, len(attributes) * 18 + 10)
    meth_h = max(24, len(methods) * 18 + 10)
    total_h = header_h + attr_h + meth_h

    # Box outline
    draw.rectangle([(x, y), (x + w, y + total_h)], fill=palette["fill"], outline=palette["border"], width=2)
    # Header fill
    draw.rectangle([(x, y), (x + w, y + header_h)], fill=palette["header"], outline=palette["border"], width=2)

    # Title text
    if stereotype:
        draw.text((x + w // 2, y + 14), stereotype, fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")
        draw.text((x + w // 2, y + 32), title, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")
    else:
        draw.text((x + w // 2, y + 16), title, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")

    # Divider between header and attributes is the outline
    # Attributes
    ay = y + header_h + 8
    for attr in attributes:
        draw.text((x + 10, ay), attr, fill=COLOR_TEXT, font=fonts["body"])
        ay += 18

    # Divider line between attributes and methods
    div_y = y + header_h + attr_h
    draw.line([(x, div_y), (x + w, div_y)], fill=palette["border"], width=1)

    # Methods
    my = div_y + 8
    for meth in methods:
        draw.text((x + 10, my), meth, fill=COLOR_TEXT, font=fonts["body"])
        my += 18

    return x, y, w, total_h

# Draw Object Box (Instance box for Object Diagram)
def draw_object_box(draw, x, y, w, instance_name, attributes=[], palette=PALETTE_BLUE):
    fonts = get_fonts()
    header_h = 34
    attr_h = max(24, len(attributes) * 19 + 12)
    total_h = header_h + attr_h

    # Body
    draw.rectangle([(x, y), (x + w, y + total_h)], fill=palette["fill"], outline=palette["border"], width=2)
    # Header
    draw.rectangle([(x, y), (x + w, y + header_h)], fill=palette["header"], outline=palette["border"], width=2)

    # Title with underline (UML object convention)
    draw.text((x + w // 2, y + 17), instance_name, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")
    # Underline text
    bbox = draw.textbbox((x + w // 2, y + 17), instance_name, font=fonts["heading"], anchor="mm")
    draw.line([(bbox[0], bbox[3] + 2), (bbox[2], bbox[3] + 2)], fill=COLOR_TEXT, width=1)

    # Attributes
    ay = y + header_h + 8
    for attr in attributes:
        draw.text((x + 10, ay), attr, fill=COLOR_TEXT, font=fonts["body"])
        ay += 19

    return x, y, w, total_h
