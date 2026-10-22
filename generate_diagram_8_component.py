import os
from PIL import Image, ImageDraw, ImageFont
from diagram_helpers import (
    create_canvas, draw_top_banner, draw_dashed_line, draw_arrow,
    get_fonts, COLOR_BORDER, COLOR_TEXT, COLOR_MUTED, COLOR_BANNER_BORDER,
    PALETTE_BLUE, PALETTE_GREEN, PALETTE_ORANGE, PALETTE_PINK, PALETTE_PURPLE, PALETTE_YELLOW, PALETTE_TEAL
)

def generate_diagram_8():
    WIDTH = 1650
    HEIGHT = 1150
    img, draw = create_canvas(WIDTH, HEIGHT)
    fonts = get_fonts()

    # Draw Top Banner
    draw_top_banner(draw, "8. COMPONENT DIAGRAM", "Smart Assignment Tracker", "(Frontend, Backend Services and Cloud Database)", canvas_w=WIDTH)

    # Helper for UML Component Box with component icon in top right
    def draw_component(x, y, w, h, title, subtitle=None, items=[], pal=PALETTE_BLUE):
        draw.rectangle([(x, y), (x + w, y + h)], fill=pal["fill"], outline=COLOR_BORDER, width=2)
        # Component stereotype
        draw.text((x + w // 2, y + 13), "«component»", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")
        draw.text((x + w // 2, y + 30), title, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")
        if subtitle:
            draw.text((x + w // 2, y + 46), subtitle, fill=COLOR_TEXT, font=fonts["small_bold"], anchor="mm")

        # Component Icon (UML 2.0 standard: rectangle with 2 protruding tabs on top right)
        ix = x + w - 24
        iy = y + 10
        draw.rectangle([(ix, iy), (ix + 16, iy + 22)], fill=(255, 255, 255), outline=COLOR_BORDER, width=1)
        draw.rectangle([(ix - 4, iy + 4), (ix + 3, iy + 9)], fill=(255, 255, 255), outline=COLOR_BORDER, width=1)
        draw.rectangle([(ix - 4, iy + 13), (ix + 3, iy + 18)], fill=(255, 255, 255), outline=COLOR_BORDER, width=1)

        # Items
        sy = y + 50 if not subtitle else y + 64
        for itm in items:
            draw.text((x + 12, sy), itm, fill=COLOR_TEXT, font=fonts["small"])
            sy += 16
        return x, y, w, h

    # Helper for lollipop interface
    def draw_lollipop(cx, cy, name, side="left"):
        r = 7
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(255, 255, 255), outline=COLOR_BORDER, width=2)
        if side == "left":
            draw.line([(cx + r, cy), (cx + 25, cy)], fill=COLOR_BORDER, width=2)
            draw.text((cx - 10, cy - 14), name, fill=COLOR_TEXT, font=fonts["small_bold"], anchor="rm")
        elif side == "top":
            draw.line([(cx, cy + r), (cx, cy + 25)], fill=COLOR_BORDER, width=2)
            draw.text((cx, cy - 14), name, fill=COLOR_TEXT, font=fonts["small_bold"], anchor="mm")
        return cx, cy

    # ================= 1. CLIENT LAYER =================
    draw.rectangle([(50, 140), (320, 560)], fill=(255, 241, 242), outline=COLOR_BANNER_BORDER, width=2)
    draw.text((70, 160), "Client Layer", fill=COLOR_BANNER_BORDER, font=fonts["heading"], anchor="lm")

    draw_component(
        70, 190, 230, 340, "Web Application", "(React / Vite SPA)",
        items=[
            "- UI Dashboard Pages",
            "- Chronological Task View",
            "- Subtask Checklist Manager",
            "- Calendar Heatmap UI",
            "- Priority Spotlight Card",
            "- Collaboration Modal",
            "- Notification Bell Banner",
            "- Context API State",
            "- Axios HTTP Client"
        ],
        pal=PALETTE_PINK
    )

    # ================= 2. BACKEND LAYER (Node.js / Express on Render) =================
    draw.rectangle([(380, 140), (1600, 560)], fill=(239, 246, 255), outline=COLOR_BANNER_BORDER, width=2)
    draw.text((400, 160), "Backend Layer (Node.js / Express on Render)", fill=COLOR_BANNER_BORDER, font=fonts["heading"], anchor="lm")

    # API Gateway / Router Component
    draw_component(
        420, 185, 1140, 90, "API Gateway / Express Router", "(index.js)",
        items=[
            "- Request Routing, CORS Configuration & Error Handling",
            "- Salted SHA-256 Auth & Role-based Shared Task Access Control"
        ],
        pal=PALETTE_BLUE
    )

    # Lollipop into API Gateway from Client
    draw_lollipop(390, 230, "IAPI", side="left")
    draw_dashed_line(draw, 300, 230, 383, 230, color=COLOR_BORDER, width=2)
    draw_arrow(draw, 300, 230, 383, 230, color=COLOR_BORDER, size=8, width=2)
    draw.text((345, 215), "HTTPS\n(REST API)", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # 6 Service Components in a row
    SVC_Y = 360
    SVC_W = 180
    SVC_H = 175
    services = [
        ("Auth Service", "IAuthService", 420, [
            "- User Registration",
            "- Salted SHA-256",
            "- JWT Token Gen",
            "- Profile Manager"
        ], PALETTE_GREEN),
        ("Assignment Svc", "IAssignmentSvc", 610, [
            "- CRUD Assignments",
            "- Category Filter",
            "- Status Updates",
            "- Sorting Engine"
        ], PALETTE_ORANGE),
        ("Subtask Service", "ISubtaskSvc", 800, [
            "- Checklist Items",
            "- Toggle Done/Undone",
            "- Compute Progress",
            "- Subtask Deletion"
        ], PALETTE_PURPLE),
        ("Priority Engine", "IPriorityEngine", 990, [
            "- Rank Score Calc",
            "- Imp * 1000 - Days",
            "- Spotlight Logic",
            "- Overdue Alerts"
        ], PALETTE_YELLOW),
        ("Calendar Service", "ICalendarSvc", 1180, [
            "- Monthly Heatmap",
            "- Daily Load Sum",
            "- Date Filter Modal",
            "- Year Nav Dropdowns"
        ], PALETTE_TEAL),
        ("Collab Service", "ICollabSvc", 1370, [
            "- Invite Handling",
            "- Accept / Decline",
            "- Team Order",
            "- Shared Permissions"
        ], PALETTE_PINK),
    ]

    for title, iface_name, sx, items, pal in services:
        draw_component(sx, SVC_Y, SVC_W, SVC_H, title, items=items, pal=pal)
        lp_x = sx + SVC_W // 2
        draw_lollipop(lp_x, 320, iface_name, side="top")
        draw_dashed_line(draw, lp_x, 275, lp_x, 313, color=COLOR_BORDER, width=1)
        draw_dashed_line(draw, lp_x, 345, lp_x, SVC_Y, color=COLOR_BORDER, width=1)

    # ================= 3. DATABASE LAYER (MySQL on Cloud) =================
    draw.rectangle([(580, 620), (1050, 950)], fill=(240, 253, 244), outline=COLOR_BANNER_BORDER, width=2)
    draw.text((600, 642), "Database Layer", fill=COLOR_BANNER_BORDER, font=fonts["heading"], anchor="lm")

    draw_component(
        610, 675, 410, 245, "MySQL Relational Database", "(Cloud Instance - Aiven / TiDB)",
        items=[
            "- users (userId, username, email, passwordHash)",
            "- assignments (assignmentId, userId, title, dueDate, imp)",
            "- subtasks (subtaskId, assignmentId, title, isCompleted)",
            "- collaborations (collabId, assignmentId, sender, receiver)",
            "- notifications (notificationId, userId, message, isRead)",
            "- categories (categoryId, name, description, colorCode)"
        ],
        pal=PALETTE_GREEN
    )

    # Connect Services to Database via mysql2 connection pool
    draw.line([(700, SVC_Y + SVC_H), (700, 675)], fill=COLOR_BORDER, width=2)
    draw_arrow(draw, 700, SVC_Y + SVC_H, 700, 675, color=COLOR_BORDER, size=8, width=2)
    draw.text((750, 590), "mysql2 / TCP Pool", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="lm")

    # ================= 4. EXTERNAL SERVICES =================
    draw.rectangle([(50, 620), (510, 950)], fill=(250, 245, 255), outline=COLOR_BANNER_BORDER, width=2)
    draw.text((70, 642), "External Hosting & Cloud Platforms", fill=COLOR_BANNER_BORDER, font=fonts["heading"], anchor="lm")

    draw_component(
        70, 675, 420, 115, "Vercel Edge Platform", "(Global CDN & Frontend Host)",
        items=[
            "- Static React Asset Hosting (HTML / JS / CSS)",
            "- Automatic SSL Termination & Custom Domains",
            "- Edge CDN Fast Global Distribution"
        ],
        pal=PALETTE_PURPLE
    )

    draw_component(
        70, 810, 420, 115, "Render Cloud Engine", "(Backend REST API Host)",
        items=[
            "- Node.js Containerized Linux Runtime",
            "- Continuous Deployment Webhook from GitHub",
            "- Automated Health Checks & Auto-Restart"
        ],
        pal=PALETTE_PURPLE
    )

    # ================= 5. THIRD PARTY / CLOUD TOOLS =================
    draw.rectangle([(1120, 620), (1600, 950)], fill=(255, 241, 242), outline=COLOR_BANNER_BORDER, width=2)
    draw.text((1140, 642), "Cloud Integrations & Tooling", fill=COLOR_BANNER_BORDER, font=fonts["heading"], anchor="lm")

    draw_component(
        1140, 675, 440, 115, "GitHub Version Control", "(CI/CD Pipeline)",
        items=[
            "- Git Repository (Anumula-Mourya26/Smart-Assignment-Tracker)",
            "- Continuous Integration / Continuous Deployment",
            "- Automated Production Deploy Trigger"
        ],
        pal=PALETTE_PINK
    )

    draw_component(
        1140, 810, 440, 115, "SMTP / Notification Service", "(Gmail / SendGrid API)",
        items=[
            "- Verification Emails for Student Accounts",
            "- Collaboration Invitation Alerts",
            "- Deadline Reminders & Overdue Notifications"
        ],
        pal=PALETTE_PINK
    )

    # Connections between services and cloud
    draw_dashed_line(draw, 280, 560, 280, 675, color=COLOR_BORDER, width=2)
    draw_arrow(draw, 280, 560, 280, 675, color=COLOR_BORDER, size=8, width=2)
    draw.text((290, 600), "CDN Deploy", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="lm")

    draw_dashed_line(draw, 1460, SVC_Y + SVC_H, 1460, 810, color=COLOR_BORDER, width=2)
    draw_arrow(draw, 1460, SVC_Y + SVC_H, 1460, 810, color=COLOR_BORDER, size=8, width=2)
    draw.text((1475, 590), "Email Alerts (HTTPS)", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="lm")

    # ================= 6. LEGEND =================
    LEG_X = 50
    LEG_Y = 990
    LEG_W = 550
    LEG_H = 110
    draw.rectangle([(LEG_X, LEG_Y), (LEG_X + LEG_W, LEG_Y + LEG_H)], fill=(255, 255, 255), outline=COLOR_BANNER_BORDER, width=2)
    draw.text((LEG_X + 16, LEG_Y + 16), "Legend", fill=COLOR_TEXT, font=fonts["heading"], anchor="lm")

    # Component Icon
    draw.rectangle([(LEG_X + 20, LEG_Y + 45), (LEG_X + 45, LEG_Y + 75)], fill=(255, 255, 255), outline=COLOR_BORDER, width=1)
    draw.rectangle([(LEG_X + 16, LEG_Y + 50), (LEG_X + 24, LEG_Y + 56)], fill=(255, 255, 255), outline=COLOR_BORDER, width=1)
    draw.rectangle([(LEG_X + 16, LEG_Y + 62), (LEG_X + 24, LEG_Y + 68)], fill=(255, 255, 255), outline=COLOR_BORDER, width=1)
    draw.text((LEG_X + 55, LEG_Y + 60), "Component", fill=COLOR_TEXT, font=fonts["small_bold"], anchor="lm")

    # Lollipop
    draw_lollipop(LEG_X + 160, LEG_Y + 60, "", side="left")
    draw.text((LEG_X + 195, LEG_Y + 60), "Provided Interface", fill=COLOR_TEXT, font=fonts["small_bold"], anchor="lm")

    # Dashed line
    draw_dashed_line(draw, LEG_X + 330, LEG_Y + 60, LEG_X + 375, LEG_Y + 60, color=COLOR_BORDER, width=2)
    draw_arrow(draw, LEG_X + 330, LEG_Y + 60, LEG_X + 375, LEG_Y + 60, color=COLOR_BORDER, size=7, width=2)
    draw.text((LEG_X + 385, LEG_Y + 60), "Dependency", fill=COLOR_TEXT, font=fonts["small_bold"], anchor="lm")

    # Save
    out_dir = r"c:\Users\HOME\Downloads\Assignment-Tracker-main\Assignment-Tracker-main\uml_diagrams"
    out_file = os.path.join(out_dir, "8_component_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Diagram 8 saved at: {out_file}")

if __name__ == "__main__":
    generate_diagram_8()
