import os
import math
from PIL import Image, ImageDraw, ImageFont
from diagram_helpers import (
    create_canvas, draw_top_banner, draw_actor, draw_dashed_line, draw_arrow,
    get_fonts, COLOR_BORDER, COLOR_TEXT, COLOR_MUTED, WIDTH, HEIGHT
)

def generate_diagram_1():
    img, draw = create_canvas(1600, 1100)
    fonts = get_fonts()

    # Draw Top Banner matching friend's image
    draw_top_banner(draw, "1. USE CASE DIAGRAM", "Smart Assignment Tracker", "(User Roles, Subtasks, Calendar & Collaboration)")

    # System Boundary Box
    SYS_X1 = 260
    SYS_Y1 = 135
    SYS_X2 = 1340
    SYS_Y2 = 1070
    draw.rectangle([(SYS_X1, SYS_Y1), (SYS_X2, SYS_Y2)], fill=(235, 246, 254), outline=COLOR_BORDER, width=2)
    draw.text(((SYS_X1 + SYS_X2) // 2, SYS_Y1 + 22), "Smart Assignment Tracker System", fill=COLOR_TEXT, font=fonts["banner_proj"], anchor="mm")

    # Helper for use case oval
    def draw_uc_oval(cx, cy, rx, ry, lines, bg_color, border_color=COLOR_BORDER):
        draw.ellipse([(cx - rx, cy - ry), (cx + rx, cy + ry)], fill=bg_color, outline=border_color, width=2)
        total_h = len(lines) * 16
        start_y = cy - (total_h // 2) + 7
        for i, line in enumerate(lines):
            draw.text((cx, start_y + i * 16), line, fill=COLOR_TEXT, font=fonts["body"], anchor="mm")

    # Colors
    C_BLUE = (191, 219, 254)    # Student ovals
    C_PURPLE = (233, 213, 255)  # Middle auth / core ovals
    C_PINK = (254, 205, 211)    # Middle shared operations
    C_ORANGE = (254, 215, 170)  # Collaborator ovals
    C_GREEN = (187, 247, 208)   # Admin ovals

    # --- LEFT COLUMN (Student Ovals) ---
    RX_L = 100
    RY_L = 22
    CX_L = 385
    student_cases = [
        ("Register Account", 195),
        ("Login", 255),
        ("View Dashboard", 315),
        ("Create Assignment", 380),
        ("Search / Filter Tasks", 445),
        ("View Task Details", 510),
        ("Manage Checklist", 575),
        ("View Calendar Heatmap", 640),
        ("Priority Spotlight", 705),
        ("Invite Collaborator", 770),
        ("View Notifications", 835),
        ("Mark Assignment Done", 900),
        ("Sign Out Session", 965),
    ]

    for name, cy in student_cases:
        draw_uc_oval(CX_L, cy, RX_L, RY_L, [name], C_BLUE)

    # --- MIDDLE CORE CASES ---
    RX_M = 100
    RY_M = 24
    CX_M = 780
    middle_cases = {
        "AUTH": (CX_M, 225, "Authenticate User", C_PURPLE),
        "RBAC": (CX_M, 345, "Role-based Access Control", C_PURPLE),
        "CALC_PRIORITY": (CX_M, 460, "Calculate Rank Score", C_PINK),
        "COMPUTE_PROG": (CX_M, 575, "Compute Progress %", C_PINK),
        "HEATMAP_LOAD": (CX_M, 690, "Aggregate Daily Load", C_PINK),
        "MANAGE_COLLAB": (CX_M, 805, "Manage Collab Invite", C_PINK),
        "NOTIFY_ALERT": (CX_M, 920, "Dispatch Notifications", C_PINK),
    }

    for key, (cx, cy, name, col) in middle_cases.items():
        draw_uc_oval(cx, cy, RX_M, RY_M, [name], col)

    # --- RIGHT TOP (Collaborator Ovals) ---
    RX_R = 100
    RY_R = 22
    CX_R = 1180
    collab_cases = [
        ("Login", 205),
        ("View Collab Requests", 265),
        ("Accept / Decline Invite", 325),
        ("View Shared Tasks", 385),
        ("Update Checklist Status", 445),
        ("View Team Hierarchy", 505)
    ]
    for name, cy in collab_cases:
        draw_uc_oval(CX_R, cy, RX_R, RY_R, [name], C_ORANGE)

    # --- RIGHT BOTTOM (Admin Ovals) ---
    admin_cases = [
        ("Login", 600),
        ("Manage User Accounts", 655),
        ("Manage All Assignments", 710),
        ("Monitor Database Workload", 765),
        ("View Analytics & Reports", 820),
        ("System Configuration", 875),
        ("Manage Notifications", 930)
    ]
    for name, cy in admin_cases:
        draw_uc_oval(CX_R, cy, RX_R, RY_R, [name], C_GREEN)

    # --- ACTORS ---
    # Left: Student (Blue head)
    ACTOR_STUDENT = (110, 560)
    draw_actor(draw, ACTOR_STUDENT[0], ACTOR_STUDENT[1], "Student", head_color=(147, 197, 253))

    # Right Top: Collaborator (Orange head)
    ACTOR_COLLAB = (1480, 355)
    draw_actor(draw, ACTOR_COLLAB[0], ACTOR_COLLAB[1], "Collaborator\n(Peer)", head_color=(254, 215, 170))

    # Right Bottom: Admin (Green head)
    ACTOR_ADMIN = (1480, 765)
    draw_actor(draw, ACTOR_ADMIN[0], ACTOR_ADMIN[1], "Admin", head_color=(187, 247, 208))

    # --- CONNECTIONS ---
    # Student connections
    for name, cy in student_cases:
        draw.line([(ACTOR_STUDENT[0] + 28, ACTOR_STUDENT[1] - 4), (CX_L - RX_L, cy)], fill=COLOR_BORDER, width=2)

    # Collaborator connections
    for name, cy in collab_cases:
        draw.line([(ACTOR_COLLAB[0] - 28, ACTOR_COLLAB[1] - 4), (CX_R + RX_R, cy)], fill=COLOR_BORDER, width=2)

    # Admin connections
    for name, cy in admin_cases:
        draw.line([(ACTOR_ADMIN[0] - 28, ACTOR_ADMIN[1] - 4), (CX_R + RX_R, cy)], fill=COLOR_BORDER, width=2)

    # --- INCLUDES & EXTENDS (Dashed arrows) ---
    def connect_inc(p1, p2, label="«include»"):
        x1, y1 = p1
        x2, y2 = p2
        draw_dashed_line(draw, x1, y1, x2, y2, color=COLOR_BORDER, width=1)
        draw_arrow(draw, x1, y1, x2, y2, color=COLOR_BORDER, open_arrow=True, size=8, width=1)
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - 8
        draw.text((mx, my), label, fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # Left to Middle Includes
    connect_inc((CX_L + RX_L, 195), (CX_M - RX_M, 225)) # Register -> Auth
    connect_inc((CX_L + RX_L, 255), (CX_M - RX_M, 225)) # Login -> Auth
    connect_inc((CX_M, 249), (CX_M, 321))               # Auth -> RBAC
    connect_inc((CX_L + RX_L, 380), (CX_M - RX_M, 460)) # Create -> Calc Priority
    connect_inc((CX_L + RX_L, 575), (CX_M - RX_M, 575)) # Manage Checklist -> Compute Progress
    connect_inc((CX_L + RX_L, 640), (CX_M - RX_M, 690)) # Calendar -> Heatmap Load
    connect_inc((CX_L + RX_L, 770), (CX_M - RX_M, 805)) # Invite Collab -> Manage Collab
    connect_inc((CX_L + RX_L, 835), (CX_M - RX_M, 920)) # View Notifications -> Dispatch

    # Middle to Right Includes
    connect_inc((CX_R - RX_R, 205), (CX_M + RX_M, 225)) # Collab Login -> Auth
    connect_inc((CX_R - RX_R, 325), (CX_M + RX_M, 805)) # Collab Accept/Decline -> Manage Collab
    connect_inc((CX_R - RX_R, 445), (CX_M + RX_M, 575)) # Collab Update Checklist -> Compute Progress
    connect_inc((CX_R - RX_R, 600), (CX_M + RX_M, 225)) # Admin Login -> Auth
    connect_inc((CX_R - RX_R, 655), (CX_M + RX_M, 345)) # Admin Manage Users -> RBAC
    connect_inc((CX_R - RX_R, 765), (CX_M + RX_M, 690)) # Admin Monitor DB -> Heatmap Load
    connect_inc((CX_R - RX_R, 930), (CX_M + RX_M, 920)) # Admin Notifications -> Dispatch

    # Save
    out_dir = r"c:\Users\HOME\Downloads\Assignment-Tracker-main\Assignment-Tracker-main\uml_diagrams"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "1_use_case_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Diagram 1 saved at: {out_file}")

if __name__ == "__main__":
    generate_diagram_1()
