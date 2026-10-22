import os
import math
import shutil
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions (spacious and balanced 1500 x 1050)
WIDTH = 1500
HEIGHT = 1050

image = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 255))
draw = ImageDraw.Draw(image)

# Native Windows Fonts
font_title = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 28)
font_box_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
font_actor = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 16)
font_uc = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
font_uc_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 14)
font_rel = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)

# Colors matching the reference image precisely
COLOR_CANVAS = (255, 255, 255)
COLOR_BORDER = (30, 41, 59)            # Crisp slate border
COLOR_SYSTEM_BG = (235, 246, 254)      # Soft pastel sky blue
COLOR_UC_FILL = (199, 230, 253)        # Clean light blue fill
COLOR_UC_BORDER = (30, 41, 59)
COLOR_LINE = (30, 41, 59)

# Actor Head Colors from reference image
COLOR_HEAD_STUDENT = (254, 224, 114)   # Sunny pastel yellow
COLOR_HEAD_ADMIN = (187, 247, 208)     # Soft mint green
COLOR_HEAD_COLLAB = (221, 214, 254)    # Soft pastel lavender

# Draw Title (Top Left)
draw.text((70, 42), "1. Smart Assignment Tracker — Use Case Diagram", fill=(15, 23, 42), font=font_title)

# System Boundary Box
SYS_X1 = 250
SYS_Y1 = 95
SYS_X2 = 1200
SYS_Y2 = 985

draw.rectangle([(SYS_X1, SYS_Y1), (SYS_X2, SYS_Y2)], fill=COLOR_SYSTEM_BG, outline=COLOR_BORDER, width=2)

# System Title centered at top inside box
draw.text(((SYS_X1 + SYS_X2) // 2, SYS_Y1 + 24), "Smart Assignment Tracker", fill=(15, 23, 42), font=font_box_title, anchor="mm")

# Helper function to draw Actor with colored head
def draw_actor(x, y, name, head_color):
    r = 18
    # Head (circle with outline)
    draw.ellipse([(x - r, y - 55), (x + r, y - 19)], fill=head_color, outline=COLOR_BORDER, width=2)
    # Spine
    draw.line([(x, y - 19), (x, y + 25)], fill=COLOR_BORDER, width=2)
    # Arms
    draw.line([(x - 28, y - 3), (x + 28, y - 3)], fill=COLOR_BORDER, width=2)
    # Legs
    draw.line([(x, y + 25), (x - 22, y + 65)], fill=COLOR_BORDER, width=2)
    draw.line([(x, y + 25), (x + 22, y + 65)], fill=COLOR_BORDER, width=2)
    # Label
    draw.text((x, y + 84), name, fill=(15, 23, 42), font=font_actor, anchor="mm")

# Helper function to draw Use Case Oval
def draw_use_case(cx, cy, rx, ry, lines):
    draw.ellipse([(cx - rx, cy - ry), (cx + rx, cy + ry)], fill=COLOR_UC_FILL, outline=COLOR_UC_BORDER, width=2)
    total_h = len(lines) * 18
    start_y = cy - (total_h // 2) + 8
    for i, line in enumerate(lines):
        draw.text((cx, start_y + i * 18), line, fill=(15, 23, 42), font=font_uc, anchor="mm")

# Helper function for dashed relationship line with arrow
def draw_relationship(from_pos, to_pos, stereotype, label_side="top"):
    x1, y1, rx1, ry1 = from_pos
    x2, y2, rx2, ry2 = to_pos
    
    angle = math.atan2(y2 - y1, x2 - x1)
    start_x = x1 + rx1 * math.cos(angle)
    start_y = y1 + ry1 * math.sin(angle)
    end_x = x2 - rx2 * math.cos(angle)
    end_y = y2 - ry2 * math.sin(angle)

    # Dashed line
    dx = end_x - start_x
    dy = end_y - start_y
    dist = math.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    curr = 0
    dash_len, gap_len = 7, 5
    while curr < dist:
        seg_end = min(curr + dash_len, dist)
        draw.line([(start_x + curr * ux, start_y + curr * uy), (start_x + seg_end * ux, start_y + seg_end * uy)], fill=COLOR_LINE, width=2)
        curr += dash_len + gap_len

    # Arrowhead
    size = 11
    p1 = (end_x - size * math.cos(angle - 0.4), end_y - size * math.sin(angle - 0.4))
    p2 = (end_x - size * math.cos(angle + 0.4), end_y - size * math.sin(angle + 0.4))
    draw.line([p1, (end_x, end_y)], fill=COLOR_LINE, width=2)
    draw.line([p2, (end_x, end_y)], fill=COLOR_LINE, width=2)

    # Label with subtle background mask to avoid line collision
    mx = (start_x + end_x) / 2
    my = (start_y + end_y) / 2
    if label_side == "top":
        my -= 14
    elif label_side == "right":
        mx += 36

    # Mask behind text
    bbox = draw.textbbox((mx, my), stereotype, font=font_rel, anchor="mm")
    draw.rectangle([(bbox[0] - 3, bbox[1] - 1), (bbox[2] + 3, bbox[3] + 1)], fill=COLOR_SYSTEM_BG)
    draw.text((mx, my), stereotype, fill=(15, 23, 42), font=font_rel, anchor="mm")

# Helper function for actor-to-oval line
def connect_actor(actor_x, actor_y, oval_x, oval_y, oval_rx, oval_ry, is_left_actor=True):
    start_pt = (actor_x + 28, actor_y - 3) if is_left_actor else (actor_x - 28, actor_y - 3)
    end_pt = (oval_x - oval_rx, oval_y) if is_left_actor else (oval_x + oval_rx, oval_y)
    draw.line([start_pt, end_pt], fill=COLOR_LINE, width=2)

# ---------------- USE CASES POSITIONS ----------------
# Left Column Use Cases (Center X = 420, close to left boundary, width = 220)
RX_LEFT = 110
RY_LEFT = 28
CX_LEFT = 405

uc_left = [
    ("Register / Login", 180),
    ("Create Assignment", 275),
    ("View Assignments List", 370),
    ("Search & Filter Tasks", 465),
    ("View Task Details", 560),
    ("Manage Checklist", 665),
    ("View Calendar Heatmap", 770),
    ("Invite Collaborator", 875)
]

# Draw Left Column Ovals
for text, cy in uc_left:
    draw_use_case(CX_LEFT, cy, RX_LEFT, RY_LEFT, [text])

# Middle Extended / Included Ovals (Center X = 770, perfectly aligned)
RX_MID = 105
RY_MID = 28
CX_MID = 760

draw_use_case(CX_MID, 665, RX_MID, RY_MID, ["Calculate Progress"])
draw_use_case(CX_MID, 770, RX_MID, RY_MID, ["Inspect Day Tasks"])
draw_use_case(CX_MID, 875, RX_MID, RY_MID, ["Accept / Decline Request"])

# Relationships in Middle
draw_relationship((CX_LEFT, 665, RX_LEFT, RY_LEFT), (CX_MID, 665, RX_MID, RY_MID), "«include»", label_side="top")
draw_relationship((CX_LEFT, 770, RX_LEFT, RY_LEFT), (CX_MID, 770, RX_MID, RY_MID), "«extend»", label_side="top")
draw_relationship((CX_LEFT, 875, RX_LEFT, RY_LEFT), (CX_MID, 875, RX_MID, RY_MID), "«include»", label_side="top")

# Right Column Ovals (Admin - Center X = 1000)
RX_ADMIN = 105
RY_ADMIN = 28
CX_ADMIN = 995

draw_use_case(CX_ADMIN, 215, RX_ADMIN, RY_ADMIN, ["Manage Assignments", "(CRUD)"])
draw_use_case(CX_ADMIN, 335, RX_ADMIN, RY_ADMIN, ["Manage Users"])
draw_use_case(CX_ADMIN, 465, RX_ADMIN, RY_ADMIN, ["View Reports"])

# Admin Extend relationship
draw_relationship((CX_ADMIN, 335, RX_ADMIN, RY_ADMIN), (CX_ADMIN, 465, RX_ADMIN, RY_ADMIN), "«extend»", label_side="right")

# ---------------- ACTORS ----------------
# Left Actor: Student
ACTOR_STUDENT = (100, 520)
draw_actor(ACTOR_STUDENT[0], ACTOR_STUDENT[1], "Student", COLOR_HEAD_STUDENT)

# Connect Student to all 8 left ovals
for _, cy in uc_left:
    connect_actor(ACTOR_STUDENT[0], ACTOR_STUDENT[1], CX_LEFT, cy, RX_LEFT, RY_LEFT, is_left_actor=True)

# Top Right Actor: Admin
ACTOR_ADMIN = (1330, 310)
draw_actor(ACTOR_ADMIN[0], ACTOR_ADMIN[1], "Admin", COLOR_HEAD_ADMIN)

# Connect Admin to his 3 ovals
connect_actor(ACTOR_ADMIN[0], ACTOR_ADMIN[1], CX_ADMIN, 215, RX_ADMIN, RY_ADMIN, is_left_actor=False)
connect_actor(ACTOR_ADMIN[0], ACTOR_ADMIN[1], CX_ADMIN, 335, RX_ADMIN, RY_ADMIN, is_left_actor=False)
connect_actor(ACTOR_ADMIN[0], ACTOR_ADMIN[1], CX_ADMIN, 465, RX_ADMIN, RY_ADMIN, is_left_actor=False)

# Bottom Right Actor: Collaborator
ACTOR_COLLAB = (1330, 875)
draw_actor(ACTOR_COLLAB[0], ACTOR_COLLAB[1], "Collaborator", COLOR_HEAD_COLLAB)

# Connect Collaborator to "Accept / Decline Request"
connect_actor(ACTOR_COLLAB[0], ACTOR_COLLAB[1], CX_MID, 875, RX_MID, RY_MID, is_left_actor=False)

# Save images to root, frontend/public, and artifact directory
OUTPUT_PATH = "use_case_diagram.png"
image.save(OUTPUT_PATH, "PNG", dpi=(300, 300))
print(f"Clean diagram saved at: {os.path.abspath(OUTPUT_PATH)}")

public_dest = os.path.join("frontend", "public", "use_case_diagram.png")
if os.path.exists("frontend/public"):
    shutil.copy2(OUTPUT_PATH, public_dest)
    print(f"Copied to frontend public folder: {os.path.abspath(public_dest)}")

artifact_dir = r"C:\Users\HOME\.gemini\antigravity\brain\4a0523a3-a273-4092-a38d-2aa8e2a2fca6"
if os.path.exists(artifact_dir):
    artifact_dest = os.path.join(artifact_dir, "use_case_diagram.png")
    shutil.copy2(OUTPUT_PATH, artifact_dest)
    print(f"Copied to artifact directory: {artifact_dest}")
