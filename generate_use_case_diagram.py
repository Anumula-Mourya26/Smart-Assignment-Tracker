import os
import math
import shutil
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions (Ultra High Resolution for Crisp Printing / PDF Submission)
WIDTH = 2600
HEIGHT = 1680

# Create canvas
image = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 255))
draw = ImageDraw.Draw(image)

# Load native TrueType fonts
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
font_subtitle = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 19)
font_section = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 19)
font_actor = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 17)
font_actor_sub = ImageFont.truetype("C:/Windows/Fonts/segoeuii.ttf", 13)
font_uc = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
font_uc_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 14)
font_rel = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_legend = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)

# Professional Color Palette
COLOR_BG = (248, 250, 252)
COLOR_SYSTEM_BORDER = (51, 65, 85)
COLOR_SYSTEM_BG = (255, 255, 255)
COLOR_LINE = (71, 85, 105)
COLOR_ACTOR = (30, 41, 59)
COLOR_INCLUDE = (16, 185, 129)   # Emerald Green
COLOR_EXTEND = (217, 119, 6)     # Amber Orange

# Canvas Background
draw.rectangle([(0, 0), (WIDTH, HEIGHT)], fill=COLOR_BG)

# Title Header
draw.text((WIDTH // 2, 42), "USE CASE DIAGRAM: SMART ASSIGNMENT TRACKER", fill=(15, 23, 42), font=font_title, anchor="mm")
draw.text((WIDTH // 2, 80), "UML 2.5 Specification • Academic Task Planning, Subtask Checklist, Calendar Heatmap & Collaboration System", fill=(100, 116, 139), font=font_subtitle, anchor="mm")

# System Boundary Rectangle
SYS_X1 = 360
SYS_Y1 = 115
SYS_X2 = 2240
SYS_Y2 = 1620

# System shadow & boundary box
draw.rectangle([(SYS_X1 + 4, SYS_Y1 + 4), (SYS_X2 + 4, SYS_Y2 + 4)], fill=(226, 232, 240))
draw.rectangle([(SYS_X1, SYS_Y1), (SYS_X2, SYS_Y2)], fill=COLOR_SYSTEM_BG, outline=COLOR_SYSTEM_BORDER, width=3)

# Header Tab
draw.rectangle([(SYS_X1, SYS_Y1), (SYS_X1 + 500, SYS_Y1 + 36)], fill=(15, 23, 42))
draw.text((SYS_X1 + 250, SYS_Y1 + 18), "System: Smart Assignment Tracker Web App", fill=(255, 255, 255), font=font_section, anchor="mm")

# Actor Drawing Helper
def draw_actor(x, y, name, subtitle=None):
    # Head
    draw.ellipse([(x - 17, y - 52), (x + 17, y - 18)], outline=COLOR_ACTOR, width=3, fill=(255, 255, 255))
    # Spine
    draw.line([(x, y - 18), (x, y + 24)], fill=COLOR_ACTOR, width=3)
    # Arms
    draw.line([(x - 28, y - 5), (x + 28, y - 5)], fill=COLOR_ACTOR, width=3)
    # Legs
    draw.line([(x, y + 24), (x - 22, y + 62)], fill=COLOR_ACTOR, width=3)
    draw.line([(x, y + 24), (x + 22, y + 62)], fill=COLOR_ACTOR, width=3)
    # Name Labels
    draw.text((x, y + 78), name, fill=COLOR_ACTOR, font=font_actor, anchor="mm")
    if subtitle:
        draw.text((x, y + 96), subtitle, fill=(100, 116, 139), font=font_actor_sub, anchor="mm")

# Database & Cloud Secondary Actor Drawing Helper
def draw_db_actor(x, y, name, stereotype="<<Secondary Actor>>"):
    w, h = 38, 22
    draw.chord([(x - w, y + 8), (x + w, y + 8 + h)], 0, 180, fill=(241, 245, 249), outline=COLOR_ACTOR, width=3)
    draw.rectangle([(x - w, y - 8), (x + w, y + 19)], fill=(241, 245, 249), outline=None)
    draw.line([(x - w, y), (x - w, y + 19)], fill=COLOR_ACTOR, width=3)
    draw.line([(x + w, y), (x + w, y + 19)], fill=COLOR_ACTOR, width=3)
    draw.arc([(x - w, y + 8), (x + w, y + 8 + h)], 0, 180, fill=COLOR_ACTOR, width=3)
    draw.ellipse([(x - w, y - 18), (x + w, y + 4)], fill=(224, 231, 255), outline=COLOR_ACTOR, width=3)
    draw.text((x, y + 46), stereotype, fill=(100, 116, 139), font=font_actor_sub, anchor="mm")
    draw.text((x, y + 66), name, fill=COLOR_ACTOR, font=font_actor, anchor="mm")

# Use Case Drawing Helper
def draw_use_case(cx, cy, rx, ry, lines, bg_color, border_color):
    draw.ellipse([(cx - rx + 3, cy - ry + 3), (cx + rx + 3, cy + ry + 3)], fill=(226, 232, 240))
    draw.ellipse([(cx - rx, cy - ry), (cx + rx, cy + ry)], fill=bg_color, outline=border_color, width=2)
    total_h = len(lines) * 17
    start_y = cy - (total_h // 2) + 8
    for i, line in enumerate(lines):
        f = font_uc_bold if i == 0 and len(lines) > 1 else font_uc
        draw.text((cx, start_y + i * 17), line, fill=(15, 23, 42), font=f, anchor="mm")

# Dashed Line Helper
def draw_dashed_line(x1, y1, x2, y2, color=(100, 116, 139), width=2, dash_len=8, gap_len=6):
    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux = dx / dist
    uy = dy / dist
    curr = 0
    while curr < dist:
        end = min(curr + dash_len, dist)
        draw.line([(x1 + curr * ux, y1 + curr * uy), (x1 + end * ux, y1 + end * uy)], fill=color, width=width)
        curr += dash_len + gap_len

# Arrowhead Helper
def draw_arrowhead(x, y, angle, color=COLOR_LINE, size=11, open_arrow=True):
    p1 = (x - size * math.cos(angle - 0.4), y - size * math.sin(angle - 0.4))
    p2 = (x - size * math.cos(angle + 0.4), y - size * math.sin(angle + 0.4))
    if open_arrow:
        draw.line([p1, (x, y)], fill=color, width=2)
        draw.line([p2, (x, y)], fill=color, width=2)
    else:
        draw.polygon([(x, y), p1, p2], fill=(255, 255, 255), outline=color)

# ----------------- 4 SUBSYSTEM ZONES (Clean 2-Column + Bottom Layout) -----------------
# Zone 1: Auth & Profile (Top Left)
draw.rectangle([(SYS_X1 + 20, 160), (1270, 500)], fill=(240, 249, 255), outline=(186, 230, 253), width=1)
draw.text((SYS_X1 + 35, 175), "1. Authentication & User Profile Management", fill=(3, 105, 161), font=font_section)

# Zone 3: Assignments & Subtasks (Middle Left)
draw.rectangle([(SYS_X1 + 20, 530), (1270, 1180)], fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((SYS_X1 + 35, 545), "3. Assignment & Subtask Checklist Management", fill=(21, 128, 61), font=font_section)

# Zone 2: Collaboration (Right Top / Mid)
draw.rectangle([(1310, 160), (SYS_X2 - 20, 1180)], fill=(245, 243, 255), outline=(221, 214, 254), width=1)
draw.text((1325, 175), "2. Collaboration & Team Workload Sharing", fill=(109, 40, 217), font=font_section)

# Zone 4: Calendar Heatmap & Decision Engine (Full Width Bottom)
draw.rectangle([(SYS_X1 + 20, 1210), (SYS_X2 - 20, 1590)], fill=(255, 251, 235), outline=(254, 240, 138), width=1)
draw.text((SYS_X1 + 35, 1225), "4. Calendar Heatmap & Priority Decision Engine", fill=(180, 83, 9), font=font_section)

# ----------------- USE CASES DEFINITIONS -----------------
use_cases = {}

# Module 1: Auth (Top Left)
use_cases["UC_REGISTER"] = (580, 250, 115, 32, ["Register Account", "(Username, Gmail, Pass)"])
use_cases["UC_VALID_GMAIL"] = (890, 250, 115, 30, ["Validate Gmail", "(@gmail.com suffix)"])
use_cases["UC_LOGIN"] = (580, 345, 115, 32, ["Authenticate & Login", "(Username or Gmail)"])
use_cases["UC_VERIFY_PASS"] = (890, 345, 115, 30, ["Verify Password Hash", "(SHA-256 Salted)"])
use_cases["UC_PROFILE"] = (580, 440, 110, 30, ["View User Profile", "(@username & ID)"])
use_cases["UC_LOGOUT"] = (890, 440, 105, 30, ["Sign Out Session"])

# Module 3: Assignments & Subtasks (Middle Left)
use_cases["UC_TASK_LIST"] = (580, 610, 120, 32, ["View Chronological", "Assignments List"])
use_cases["UC_FILTER_TASKS"] = (890, 610, 115, 30, ["Filter Categories", "(All, Active, Completed)"])
use_cases["UC_CREATE_TASK"] = (580, 720, 120, 32, ["Create Assignment", "(Title, DueDate, Imp 1-5)"])
use_cases["UC_CALC_PRIORITY"] = (890, 720, 115, 30, ["Calculate Rank Score", "(Imp x 1000 - Days)"])
use_cases["UC_DETAIL_VIEW"] = (580, 835, 125, 34, ["Open Dedicated Task View", "(Left Checklist, Right Collab)"])
use_cases["UC_ADD_SUBTASK"] = (890, 835, 115, 30, ["Add Subtask Item", "(Checklist Entry)"])
use_cases["UC_TOGGLE_SUBTASK"] = (580, 955, 125, 34, ["Toggle Subtask Status", "(Mark Done / Undone)"])
use_cases["UC_SUBTASK_PROGRESS"] = (890, 955, 115, 30, ["Compute Task Progress", "(done / total %)"])
use_cases["UC_MARK_COMPLETE"] = (580, 1080, 125, 34, ["Mark Assignment Done", "(Allowed ONLY in View)"])
use_cases["UC_DELETE_SUBTASK"] = (890, 1080, 115, 30, ["Delete Subtask Item"])

# Module 2: Collaboration (Right Top / Mid)
use_cases["UC_INVITE"] = (1510, 260, 125, 32, ["Invite Collaborator", "(By @username or Gmail)"])
use_cases["UC_REQUESTS"] = (1940, 260, 125, 32, ["View Collaboration", "Requests on Dashboard"])
use_cases["UC_ACCEPT"] = (1940, 385, 125, 32, ["Accept Collab Request", "(Status -> ACCEPTED)"])
use_cases["UC_DECLINE"] = (1940, 510, 125, 32, ["Decline Collab Request", "(Removes Invite)"])
use_cases["UC_VIEW_TEAM"] = (1510, 385, 125, 32, ["View Collaborator Order", "(Owner -> You -> Others)"])
use_cases["UC_SHARED_VIEW"] = (1510, 510, 125, 32, ["View 'Shared With Me'", "Assignments Filter"])
use_cases["UC_CAN_ACCESS"] = (1510, 640, 130, 32, ["Verify Access Rights", "(Owner or Collaborator)"])

# Module 4: Calendar Heatmap & Decision Engine (Full Width Bottom)
use_cases["UC_CALENDAR"] = (600, 1315, 130, 34, ["View Monthly Calendar Grid", "(Workload Intensity)"])
use_cases["UC_HEATMAP"] = (960, 1315, 125, 30, ["Aggregate Daily Workload", "(Sum Priorities per Date)"])
use_cases["UC_MONTH_YEAR"] = (600, 1475, 125, 30, ["Select Month & Year", "(Interactive Dropdowns)"])
use_cases["UC_DAY_TASKS"] = (960, 1475, 125, 32, ["Inspect Day Assignments", "(Day Click Modal)"])
use_cases["UC_SPOTLIGHT"] = (1510, 1315, 130, 34, ["Priority Spotlight Panel", "(Top Incomplete Task)"])

# Draw all Use Cases
for k, (cx, cy, rx, ry, lines) in use_cases.items():
    if "REGISTER" in k or "LOGIN" in k or "VALID" in k or "VERIFY" in k or "PROFILE" in k or "LOGOUT" in k:
        bg, border = (224, 242, 254), (2, 132, 199)
    elif "INVITE" in k or "REQUEST" in k or "ACCEPT" in k or "DECLINE" in k or "TEAM" in k or "ACCESS" in k or "SHARED" in k:
        bg, border = (237, 233, 254), (124, 58, 237)
    elif "CALENDAR" in k or "MONTH" in k or "DAY" in k or "HEATMAP" in k or "SPOTLIGHT" in k:
        bg, border = (254, 243, 199), (217, 119, 6)
    else:
        bg, border = (220, 252, 231), (22, 163, 74)
    draw_use_case(cx, cy, rx, ry, lines, bg_color=bg, border_color=border)

# ----------------- ACTORS PLACEMENT -----------------
# Primary Actors on Left
ACTOR_GUEST = (180, 270)
ACTOR_STUDENT = (180, 520)
ACTOR_OWNER = (180, 870)

# Peer Primary Actor on Right
ACTOR_COLLAB = (2420, 390)

# Secondary Supporting Cloud Actors on Right
ACTOR_MYSQL = (2420, 780)
ACTOR_RENDER = (2420, 1120)

# Draw Stick Figures and Cylinders
draw_actor(ACTOR_GUEST[0], ACTOR_GUEST[1], "Guest / Visitor", "<<Unregistered>>")
draw_actor(ACTOR_STUDENT[0], ACTOR_STUDENT[1], "Registered Student", "<<Primary Base Actor>>")
draw_actor(ACTOR_OWNER[0], ACTOR_OWNER[1], "Assignment Owner", "<<Task Creator>>")
draw_actor(ACTOR_COLLAB[0], ACTOR_COLLAB[1], "Collaborator", "<<Invited Peer>>")

draw_db_actor(ACTOR_MYSQL[0], ACTOR_MYSQL[1], "MySQL Cloud Database")
draw_db_actor(ACTOR_RENDER[0], ACTOR_RENDER[1], "Render API Engine", "<<Cloud Backend Host>>")

# Actor Generalization: Assignment Owner -> Registered Student
def draw_generalization(x1, y1, x2, y2):
    draw.line([(x1, y1), (x2, y2 + 16)], fill=COLOR_ACTOR, width=2)
    # Open triangle head pointing at parent
    draw.polygon([(x2, y2), (x2 - 10, y2 + 16), (x2 + 10, y2 + 16)], fill=(255, 255, 255), outline=COLOR_ACTOR)

# Owner inherits from Student (drawn cleanly vertically)
draw_generalization(ACTOR_OWNER[0], ACTOR_OWNER[1] - 40, ACTOR_STUDENT[0], ACTOR_STUDENT[1] + 95)

# ----------------- RELATIONSHIPS & ASSOCIATIONS -----------------
def connect_actor_uc(actor_pos, uc_key, offset_actor=(30, 0), offset_uc=(0, 0)):
    uc = use_cases[uc_key]
    draw.line([(actor_pos[0] + offset_actor[0], actor_pos[1] + offset_actor[1]), (uc[0] - uc[2] + offset_uc[0], uc[1] + offset_uc[1])], fill=COLOR_LINE, width=2)

def connect_right_actor_uc(actor_pos, uc_key, offset_actor=(-30, 0), offset_uc=(0, 0)):
    uc = use_cases[uc_key]
    draw.line([(actor_pos[0] + offset_actor[0], actor_pos[1] + offset_actor[1]), (uc[0] + uc[2] + offset_uc[0], uc[1] + offset_uc[1])], fill=COLOR_LINE, width=2)

def connect_sec_actor_uc(actor_pos, uc_key, offset_uc=(0, 0)):
    uc = use_cases[uc_key]
    draw.line([(actor_pos[0] - 45, actor_pos[1]), (uc[0] + uc[2] + offset_uc[0], uc[1] + offset_uc[1])], fill=(148, 163, 184), width=2)

# 1. Guest Associations
connect_actor_uc(ACTOR_GUEST, "UC_REGISTER")
connect_actor_uc(ACTOR_GUEST, "UC_LOGIN")

# 2. Registered Student Associations (Base operations accessible by all logged in users)
connect_actor_uc(ACTOR_STUDENT, "UC_LOGIN")
connect_actor_uc(ACTOR_STUDENT, "UC_PROFILE")
connect_actor_uc(ACTOR_STUDENT, "UC_TASK_LIST")
connect_actor_uc(ACTOR_STUDENT, "UC_DETAIL_VIEW")

# 3. Assignment Owner Associations (Creator Exclusive Operations)
connect_actor_uc(ACTOR_OWNER, "UC_CREATE_TASK")
connect_actor_uc(ACTOR_OWNER, "UC_ADD_SUBTASK", offset_uc=(-10, 10))
connect_actor_uc(ACTOR_OWNER, "UC_TOGGLE_SUBTASK")
connect_actor_uc(ACTOR_OWNER, "UC_MARK_COMPLETE")
connect_actor_uc(ACTOR_OWNER, "UC_DELETE_SUBTASK", offset_uc=(-10, 10))
connect_actor_uc(ACTOR_OWNER, "UC_CALENDAR", offset_uc=(-10, -10))

# 4. Collaborator Associations (Invited Peer on Right Side)
connect_right_actor_uc(ACTOR_COLLAB, "UC_REQUESTS")
connect_right_actor_uc(ACTOR_COLLAB, "UC_ACCEPT")
connect_right_actor_uc(ACTOR_COLLAB, "UC_DECLINE")
connect_right_actor_uc(ACTOR_COLLAB, "UC_VIEW_TEAM")
connect_right_actor_uc(ACTOR_COLLAB, "UC_SHARED_VIEW")

# 5. Secondary Supporting Actor Associations
connect_sec_actor_uc(ACTOR_MYSQL, "UC_ACCEPT")
connect_sec_actor_uc(ACTOR_MYSQL, "UC_DECLINE")
connect_sec_actor_uc(ACTOR_MYSQL, "UC_CAN_ACCESS")

connect_sec_actor_uc(ACTOR_RENDER, "UC_CAN_ACCESS")
connect_sec_actor_uc(ACTOR_RENDER, "UC_SPOTLIGHT")

# ----------------- <<INCLUDE>> & <<EXTEND>> CONNECTIONS -----------------
def draw_include_extend(from_key, to_key, stereotype):
    f = use_cases[from_key]
    t = use_cases[to_key]
    angle = math.atan2(t[1] - f[1], t[0] - f[0])
    x1 = f[0] + f[2] * math.cos(angle)
    y1 = f[1] + f[3] * math.sin(angle)
    x2 = t[0] - t[2] * math.cos(angle)
    y2 = t[1] - t[3] * math.sin(angle)

    is_include = stereotype == "<<include>>"
    col = COLOR_INCLUDE if is_include else COLOR_EXTEND
    draw_dashed_line(x1, y1, x2, y2, color=col, width=2)
    draw_arrowhead(x2, y2, angle, color=col, size=11, open_arrow=True)

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    # Clean background badge
    draw.rectangle([(mx - 36, my - 9), (mx + 36, my + 9)], fill=(255, 255, 255), outline=col, width=1)
    draw.text((mx, my), stereotype, fill=col, font=font_rel, anchor="mm")

# Module 1 Includes
draw_include_extend("UC_REGISTER", "UC_VALID_GMAIL", "<<include>>")
draw_include_extend("UC_LOGIN", "UC_VERIFY_PASS", "<<include>>")

# Module 3 Includes & Extends
draw_include_extend("UC_CREATE_TASK", "UC_CALC_PRIORITY", "<<include>>")
draw_include_extend("UC_TOGGLE_SUBTASK", "UC_SUBTASK_PROGRESS", "<<include>>")
draw_include_extend("UC_FILTER_TASKS", "UC_TASK_LIST", "<<extend>>")

# Module 4 Includes & Extends
draw_include_extend("UC_CALENDAR", "UC_HEATMAP", "<<include>>")
draw_include_extend("UC_MONTH_YEAR", "UC_CALENDAR", "<<extend>>")
draw_include_extend("UC_DAY_TASKS", "UC_CALENDAR", "<<extend>>")

# ----------------- UML 2.5 NOTATION LEGEND -----------------
LEG_X = 50
LEG_Y = 1260
LEG_W = 280
LEG_H = 310

draw.rectangle([(LEG_X + 3, LEG_Y + 3), (LEG_X + LEG_W + 3, LEG_Y + LEG_H + 3)], fill=(226, 232, 240))
draw.rectangle([(LEG_X, LEG_Y), (LEG_X + LEG_W, LEG_Y + LEG_H)], fill=(255, 255, 255), outline=COLOR_SYSTEM_BORDER, width=2)
draw.rectangle([(LEG_X, LEG_Y), (LEG_X + LEG_W, LEG_Y + 32)], fill=(15, 23, 42))
draw.text((LEG_X + 14, LEG_Y + 16), "UML 2.5 Notation Legend", fill=(255, 255, 255), font=font_actor, anchor="lm")

# 1. Use Case Ellipse
draw.ellipse([(LEG_X + 16, LEG_Y + 48), (LEG_X + 76, LEG_Y + 74)], fill=(224, 242, 254), outline=(2, 132, 199), width=2)
draw.text((LEG_X + 90, LEG_Y + 61), "Use Case (Action)", fill=COLOR_ACTOR, font=font_legend, anchor="lm")

# 2. Association line
draw.line([(LEG_X + 16, LEG_Y + 100), (LEG_X + 76, LEG_Y + 100)], fill=COLOR_LINE, width=2)
draw.text((LEG_X + 90, LEG_Y + 100), "Association Line", fill=COLOR_ACTOR, font=font_legend, anchor="lm")

# 3. <<include>>
draw_dashed_line(LEG_X + 16, LEG_Y + 140, LEG_X + 76, LEG_Y + 140, color=COLOR_INCLUDE, width=2)
draw_arrowhead(LEG_X + 76, LEG_Y + 140, 0, color=COLOR_INCLUDE, size=9)
draw.text((LEG_X + 90, LEG_Y + 140), "<<include>> (Mandatory)", fill=COLOR_INCLUDE, font=font_legend, anchor="lm")

# 4. <<extend>>
draw_dashed_line(LEG_X + 16, LEG_Y + 180, LEG_X + 76, LEG_Y + 180, color=COLOR_EXTEND, width=2)
draw_arrowhead(LEG_X + 76, LEG_Y + 180, 0, color=COLOR_EXTEND, size=9)
draw.text((LEG_X + 90, LEG_Y + 180), "<<extend>> (Optional)", fill=COLOR_EXTEND, font=font_legend, anchor="lm")

# 5. Generalization
draw.line([(LEG_X + 16, LEG_Y + 220), (LEG_X + 64, LEG_Y + 220)], fill=COLOR_ACTOR, width=2)
draw.polygon([(LEG_X + 76, LEG_Y + 220), (LEG_X + 64, LEG_Y + 214), (LEG_X + 64, LEG_Y + 226)], fill=(255, 255, 255), outline=COLOR_ACTOR)
draw.text((LEG_X + 90, LEG_Y + 220), "Generalization", fill=COLOR_ACTOR, font=font_legend, anchor="lm")

# 6. Secondary Actor
draw.text((LEG_X + 16, LEG_Y + 260), "<<Secondary Actor>>", fill=(100, 116, 139), font=font_actor_sub, anchor="lm")
draw.text((LEG_X + 16, LEG_Y + 285), "Cloud Database & API Host", fill=COLOR_ACTOR, font=font_legend, anchor="lm")

# Save high-res PNG image
OUTPUT_PATH = "use_case_diagram.png"
image.save(OUTPUT_PATH, "PNG", dpi=(300, 300))
print(f"High-resolution PNG saved successfully at: {os.path.abspath(OUTPUT_PATH)}")

# Copy to frontend/public and artifact directory
public_dest = os.path.join("frontend", "public", "use_case_diagram.png")
if os.path.exists("frontend/public"):
    shutil.copy2(OUTPUT_PATH, public_dest)
    print(f"Copied to frontend public folder: {os.path.abspath(public_dest)}")

artifact_dir = r"C:\Users\HOME\.gemini\antigravity\brain\4a0523a3-a273-4092-a38d-2aa8e2a2fca6"
if os.path.exists(artifact_dir):
    artifact_dest = os.path.join(artifact_dir, "use_case_diagram.png")
    shutil.copy2(OUTPUT_PATH, artifact_dest)
    print(f"Copied to artifact directory: {artifact_dest}")
