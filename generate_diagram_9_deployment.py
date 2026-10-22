import os
import math
from PIL import Image, ImageDraw, ImageFont
from diagram_helpers import (
    create_canvas, draw_top_banner, draw_arrow,
    get_fonts, COLOR_BORDER, COLOR_TEXT, COLOR_MUTED, COLOR_BANNER_BORDER,
    PALETTE_BLUE, PALETTE_GREEN, PALETTE_ORANGE, PALETTE_PINK, PALETTE_PURPLE, PALETTE_YELLOW, PALETTE_TEAL
)

def generate_diagram_9():
    WIDTH = 1750
    HEIGHT = 1250
    img, draw = create_canvas(WIDTH, HEIGHT)
    fonts = get_fonts()

    # Draw Top Banner
    draw_top_banner(draw, "9. DEPLOYMENT DIAGRAM", "Smart Assignment Tracker", "(Physical Deployment Architecture on Vercel, Render & MySQL)", canvas_w=WIDTH)

    # Helper for 3D Node
    def draw_3d_node(x, y, w, h, title, subtitle=None, depth=18, pal=PALETTE_BLUE):
        draw.rectangle([(x, y + depth), (x + w, y + h)], fill=pal["fill"], outline=COLOR_BORDER, width=2)
        draw.polygon([
            (x, y + depth),
            (x + depth, y),
            (x + w + depth, y),
            (x + w, y + depth)
        ], fill=pal["header"], outline=COLOR_BORDER)
        draw.polygon([
            (x + w, y + depth),
            (x + w + depth, y),
            (x + w + depth, y + h - depth),
            (x + w, y + h)
        ], fill=pal["header"], outline=COLOR_BORDER)

        draw.text((x + w // 2, y + depth + 16), title, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")
        if subtitle:
            draw.text((x + w // 2, y + depth + 33), subtitle, fill=COLOR_MUTED, font=fonts["small_italic"], anchor="mm")
        return x, y, w, h

    # Helper for Artifact Box
    def draw_artifact(x, y, w, h, title, subtitle=None, items=[], fill=(255, 241, 242)):
        draw.rectangle([(x, y), (x + w, y + h)], fill=fill, outline=COLOR_BORDER, width=1)
        ix = x + w - 20
        iy = y + 8
        draw.polygon([(ix, iy), (ix + 10, iy), (ix + 14, iy + 4), (ix + 14, iy + 16), (ix, iy + 16)], fill=(255, 255, 255), outline=COLOR_BORDER)
        draw.polygon([(ix + 10, iy), (ix + 14, iy + 4), (ix + 10, iy + 4)], fill=(200, 200, 200), outline=COLOR_BORDER)

        draw.text((x + w // 2, y + 12), "«artifact»", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")
        draw.text((x + w // 2, y + 26), title, fill=COLOR_TEXT, font=fonts["small_bold"], anchor="mm")
        if subtitle:
            draw.text((x + w // 2, y + 40), subtitle, fill=COLOR_MUTED, font=fonts["small_italic"], anchor="mm")

        sy = y + 44 if not subtitle else y + 54
        for itm in items:
            draw.text((x + 10, sy), itm, fill=COLOR_TEXT, font=fonts["small"])
            sy += 16
        return x, y, w, h

    # Helper for laptop icon
    def draw_laptop_icon(x, y):
        draw.rectangle([(x, y), (x + 28, y + 18)], fill=(255, 255, 255), outline=COLOR_BORDER, width=2)
        draw.line([(x - 4, y + 18), (x + 32, y + 18)], fill=COLOR_BORDER, width=3)

    # Helper for phone icon
    def draw_phone_icon(x, y):
        draw.rounded_rectangle([(x, y), (x + 14, y + 22)], radius=2, fill=(255, 255, 255), outline=COLOR_BORDER, width=2)
        draw.line([(x + 5, y + 18), (x + 9, y + 18)], fill=COLOR_BORDER, width=1)

    # Helper for Cylinder icon
    def draw_cylinder(cx, cy, w=16, h=22):
        draw.ellipse([(cx - w, cy - h), (cx + w, cy - h + 10)], fill=(255, 255, 255), outline=COLOR_BORDER, width=1)
        draw.rectangle([(cx - w, cy - h + 5), (cx + w, cy + h - 5)], fill=(255, 255, 255), outline=None)
        draw.line([(cx - w, cy - h + 5), (cx - w, cy + h - 5)], fill=COLOR_BORDER, width=1)
        draw.line([(cx + w, cy - h + 5), (cx + w, cy + h - 5)], fill=COLOR_BORDER, width=1)
        draw.arc([(cx - w, cy + h - 10), (cx + w, cy + h)], 0, 180, fill=COLOR_BORDER, width=1)

    # Helper for Cloud shape
    def draw_cloud(cx, cy, label="Internet"):
        rx, ry = 65, 40
        draw.ellipse([(cx - rx, cy - ry + 8), (cx + rx, cy + ry - 8)], fill=(243, 232, 255), outline=COLOR_BORDER, width=2)
        draw.ellipse([(cx - 35, cy - ry - 10), (cx + 35, cy + 10)], fill=(243, 232, 255), outline=COLOR_BORDER, width=2)
        draw.ellipse([(cx - 55, cy - 15), (cx + 5, cy + ry - 5)], fill=(243, 232, 255), outline=COLOR_BORDER, width=2)
        draw.ellipse([(cx - 5, cy - 15), (cx + 55, cy + ry - 5)], fill=(243, 232, 255), outline=COLOR_BORDER, width=2)
        draw.ellipse([(cx - rx + 3, cy - ry + 11), (cx + rx - 3, cy + ry - 11)], fill=(243, 232, 255), outline=None)
        draw.ellipse([(cx - 32, cy - ry - 7), (cx + 32, cy + 7)], fill=(243, 232, 255), outline=None)
        draw.text((cx, cy), label, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")

    # Helper for bi-directional communication link
    def draw_link(p1, p2, label="HTTPS"):
        draw.line([p1, p2], fill=COLOR_BORDER, width=2)
        draw_arrow(draw, p2[0], p2[1], p1[0], p1[1], color=COLOR_BORDER, open_arrow=False, size=6, width=2)
        draw_arrow(draw, p1[0], p1[1], p2[0], p2[1], color=COLOR_BORDER, open_arrow=False, size=6, width=2)
        mx = (p1[0] + p2[0]) / 2
        my = (p1[1] + p2[1]) / 2
        draw.text((mx, my - 10), label, fill=COLOR_TEXT, font=fonts["small_bold"], anchor="mm")

    # ================= 1. CLIENT NODES (Left Column) =================
    # Top Left: Student Device
    draw_3d_node(40, 140, 270, 220, "Student Device", "(Laptop / PC Browser)", depth=16, pal=PALETTE_BLUE)
    draw_laptop_icon(58, 220)
    draw_artifact(
        105, 205, 190, 140, "React Web Application", "(Frontend SPA)",
        items=[
            "- UI Dashboard Pages",
            "- Chronological Task View",
            "- Subtask Checklist",
            "- Calendar Heatmap UI"
        ],
        fill=(255, 241, 242)
    )

    # Middle Left: Collaborator Device
    draw_3d_node(40, 390, 270, 220, "Collaborator Device", "(Mobile / Tablet Browser)", depth=16, pal=PALETTE_BLUE)
    draw_phone_icon(65, 470)
    draw_artifact(
        105, 455, 190, 140, "Responsive Web App", "(Peer Collaboration View)",
        items=[
            "- View Shared Tasks",
            "- Check Off Subtasks",
            "- Accept / Decline Invite",
            "- Team Hierarchy View"
        ],
        fill=(255, 241, 242)
    )

    # Bottom Left: Admin Device
    draw_3d_node(40, 640, 270, 210, "Admin Device", "(Laptop / Workstation)", depth=16, pal=PALETTE_BLUE)
    draw_laptop_icon(58, 720)
    draw_artifact(
        105, 705, 190, 130, "Admin Portal Client", "(Web Dashboard)",
        items=[
            "- User Accounts Audit",
            "- Manage All Tasks",
            "- System Health Metrics"
        ],
        fill=(255, 241, 242)
    )

    # ================= 2. INTERNET CLOUD =================
    CLOUD_X = 450
    CLOUD_Y = 480
    draw_cloud(CLOUD_X, CLOUD_Y, "Internet")

    draw_link((310, 250), (CLOUD_X - 60, CLOUD_Y - 30), "HTTPS\n(Internet)")
    draw_link((310, 500), (CLOUD_X - 65, CLOUD_Y + 5), "HTTPS\n(Internet)")
    draw_link((310, 745), (CLOUD_X - 60, CLOUD_Y + 40), "HTTPS\n(Internet)")

    # ================= 3. FRONTEND EDGE SERVER (Vercel CDN) =================
    draw_3d_node(610, 140, 430, 175, "Frontend Edge Server", "(Vercel Global CDN)", depth=16, pal=PALETTE_PURPLE)
    draw_artifact(
        635, 205, 380, 95, "Static Frontend Build", "(dist/ bundle)",
        items=[
            "- Vite Production Build (HTML, JS, CSS)",
            "- Automatic Anycast Edge CDN Distribution",
            "- SSL Termination (https://...vercel.app)"
        ],
        fill=(250, 245, 255)
    )
    draw_link((CLOUD_X + 45, CLOUD_Y - 45), (635, 315), "HTTPS\n(CDN)")

    # ================= 4. APPLICATION SERVER (Render Cloud) =================
    draw_3d_node(610, 380, 450, 420, "Application Server", "(Render Cloud Linux Container)", depth=20, pal=PALETTE_GREEN)

    draw_artifact(
        630, 450, 410, 335, "Node.js Web Service", "(server.js / Express REST API)",
        items=[], fill=(254, 252, 232)
    )

    def draw_mini_comp(cx, cy, w, h, title):
        draw.rectangle([(cx, cy), (cx + w, cy + h)], fill=(239, 246, 255), outline=COLOR_BORDER, width=1)
        draw.rectangle([(cx - 3, cy + 3), (cx + 2, cy + 7)], fill=(255, 255, 255), outline=COLOR_BORDER, width=1)
        draw.rectangle([(cx - 3, cy + 10), (cx + 2, cy + 14)], fill=(255, 255, 255), outline=COLOR_BORDER, width=1)
        draw.text((cx + w // 2, cy + 8), "«component»", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")
        draw.text((cx + w // 2, cy + 22), title, fill=COLOR_TEXT, font=fonts["small_bold"], anchor="mm")

    draw_mini_comp(650, 505, 175, 38, "API Gateway")
    draw_mini_comp(845, 505, 175, 38, "Auth Service")
    draw_mini_comp(650, 555, 175, 38, "Assignment Svc")
    draw_mini_comp(845, 555, 175, 38, "Priority Engine")
    draw_mini_comp(650, 605, 175, 38, "Subtask Service")
    draw_mini_comp(845, 605, 175, 38, "Calendar Service")
    draw_mini_comp(650, 655, 370, 38, "Collaboration Service")

    draw_link((CLOUD_X + 65, CLOUD_Y), (610, CLOUD_Y), "HTTPS\n(REST API)")

    # ================= 5. DATABASE SERVER (Cloud MySQL) =================
    draw_3d_node(630, 880, 410, 260, "Database Server", "(Cloud MySQL - Aiven / TiDB / PlanetScale)", depth=18, pal=PALETTE_BLUE)
    draw_cylinder(670, 980)
    draw_artifact(
        710, 945, 310, 180, "MySQL Relational Database", "(central_assignment_db)",
        items=[
            "- users (Auth & Salted Passwords)",
            "- assignments (Core Task Details)",
            "- subtasks (Granular Checklist)",
            "- collaborations (Team Invites)",
            "- notifications (Alert History)",
            "- categories (Tagging & Filters)"
        ],
        fill=(240, 253, 244)
    )
    draw_link((835, 800), (835, 880), "TCP/IP\n(mysql2 Pool: 3306)")

    # ================= 6. NOTIFICATION & MAIL SERVER (Top Right) =================
    draw_3d_node(1280, 140, 410, 220, "Notification & Mail Server", "(Gmail SMTP / SendGrid API)", depth=16, pal=PALETTE_PINK)
    draw_artifact(
        1310, 205, 350, 140, "Notification API", "(Email Dispatcher)",
        items=[
            "- Account Verification Emails",
            "- Peer Collaboration Invitation Alerts",
            "- Deadline Reminders & Alerts",
            "- Overdue Priority Spotlight Warning"
        ],
        fill=(255, 241, 242)
    )
    draw_link((1060, 440), (1280, 250), "HTTPS\n(Mail API)")

    # ================= 7. GITHUB REPOSITORY & CI/CD (Middle Right) =================
    draw_3d_node(1280, 420, 410, 220, "CI/CD & Version Control Server", "(GitHub Cloud Platform)", depth=16, pal=PALETTE_PURPLE)
    draw_artifact(
        1310, 485, 350, 140, "Smart-Assignment-Tracker Repo", "(Anumula-Mourya26/Smart-...)",
        items=[
            "- Git Version Control Main Branch",
            "- Automated Webhooks to Render",
            "- Automated Webhooks to Vercel",
            "- Continuous Deployment CI/CD"
        ],
        fill=(250, 245, 255)
    )
    draw_link((1060, 530), (1280, 530), "HTTPS\n(Deploy Webhook)")

    # ================= 8. CLOUD MONITORING SERVER (Bottom Right) =================
    draw_3d_node(1280, 700, 410, 220, "Cloud Monitoring Server", "(Render Logs / Health Monitor)", depth=16, pal=PALETTE_YELLOW)
    draw_cylinder(1320, 800)
    draw_artifact(
        1360, 765, 300, 140, "System Telemetry & Logs", "(Server Health Metrics)",
        items=[
            "- CPU & RAM Usage Statistics",
            "- Request Latency & Status Codes",
            "- Active TCP Database Connections",
            "- Automated SSL Status"
        ],
        fill=(254, 252, 232)
    )
    draw_link((1060, 660), (1280, 770), "HTTPS\n(Telemetry API)")

    # ================= 9. LEGEND (Bottom Left) =================
    LEG_X = 40
    LEG_Y = 920
    LEG_W = 460
    LEG_H = 195
    draw.rectangle([(LEG_X, LEG_Y), (LEG_X + LEG_W, LEG_Y + LEG_H)], fill=(255, 255, 255), outline=COLOR_BANNER_BORDER, width=2)
    draw.text((LEG_X + 16, LEG_Y + 18), "Legend", fill=COLOR_TEXT, font=fonts["heading"], anchor="lm")

    # Node in legend
    draw.polygon([(LEG_X + 20, LEG_Y + 52), (LEG_X + 28, LEG_Y + 44), (LEG_X + 58, LEG_Y + 44), (LEG_X + 50, LEG_Y + 52)], fill=(191, 219, 254), outline=COLOR_BORDER)
    draw.polygon([(LEG_X + 50, LEG_Y + 52), (LEG_X + 58, LEG_Y + 44), (LEG_X + 58, LEG_Y + 69), (LEG_X + 50, LEG_Y + 77)], fill=(191, 219, 254), outline=COLOR_BORDER)
    draw.rectangle([(LEG_X + 20, LEG_Y + 52), (LEG_X + 50, LEG_Y + 77)], fill=(239, 246, 255), outline=COLOR_BORDER)
    draw.text((LEG_X + 75, LEG_Y + 54), "Node", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((LEG_X + 75, LEG_Y + 70), "(Physical Device / Server Instance)", fill=COLOR_MUTED, font=fonts["small"])

    # Artifact in legend
    draw.rectangle([(LEG_X + 20, LEG_Y + 98), (LEG_X + 50, LEG_Y + 128)], fill=(255, 241, 242), outline=COLOR_BORDER)
    draw.polygon([(LEG_X + 42, LEG_Y + 98), (LEG_X + 50, LEG_Y + 106), (LEG_X + 42, LEG_Y + 106)], fill=(200, 200, 200), outline=COLOR_BORDER)
    draw.text((LEG_X + 75, LEG_Y + 103), "Artifact", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((LEG_X + 75, LEG_Y + 119), "(Deployed Code / Software Component)", fill=COLOR_MUTED, font=fonts["small"])

    # Comm link in legend
    draw.line([(LEG_X + 20, LEG_Y + 160), (LEG_X + 55, LEG_Y + 160)], fill=COLOR_BORDER, width=2)
    draw_arrow(draw, LEG_X + 20, LEG_Y + 160, LEG_X + 55, LEG_Y + 160, color=COLOR_BORDER, open_arrow=False, size=6, width=2)
    draw_arrow(draw, LEG_X + 55, LEG_Y + 160, LEG_X + 20, LEG_Y + 160, color=COLOR_BORDER, open_arrow=False, size=6, width=2)
    draw.text((LEG_X + 75, LEG_Y + 153), "Communication Link", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((LEG_X + 75, LEG_Y + 169), "(Protocol: HTTPS, TCP/IP)", fill=COLOR_MUTED, font=fonts["small"])

    # Save
    out_dir = r"c:\Users\HOME\Downloads\Assignment-Tracker-main\Assignment-Tracker-main\uml_diagrams"
    out_file = os.path.join(out_dir, "9_deployment_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Diagram 9 saved at: {out_file}")

if __name__ == "__main__":
    generate_diagram_9()
