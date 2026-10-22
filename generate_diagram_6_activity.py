import os
from PIL import Image, ImageDraw, ImageFont
from diagram_helpers import (
    create_canvas, draw_top_banner, draw_arrow,
    get_fonts, COLOR_BORDER, COLOR_TEXT, COLOR_MUTED
)

def generate_diagram_6():
    WIDTH = 1600
    HEIGHT = 1200
    img, draw = create_canvas(WIDTH, HEIGHT)
    fonts = get_fonts()

    # Draw Top Banner
    draw_top_banner(draw, "6. ACTIVITY DIAGRAM", "Smart Assignment Tracker", "(Create, Collaborate & Complete Assignment Workflow)", canvas_w=WIDTH)

    # 4 Swimlanes
    SWIM_Y1 = 140
    SWIM_Y2 = 1160
    lanes = [
        ("Student (Owner)", 50, 420, (239, 246, 255), (191, 219, 254)),
        ("System (API Engine)", 420, 800, (240, 253, 244), (187, 247, 208)),
        ("Cloud Database (MySQL)", 800, 1180, (254, 252, 232), (254, 240, 138)),
        ("Collaborator (Peer)", 1180, 1550, (255, 247, 237), (254, 215, 170)),
    ]

    for title, x1, x2, bg_col, hdr_col in lanes:
        # Lane Body
        draw.rectangle([(x1, SWIM_Y1), (x2, SWIM_Y2)], fill=bg_col, outline=COLOR_BORDER, width=2)
        # Lane Header
        draw.rectangle([(x1, SWIM_Y1), (x2, SWIM_Y1 + 40)], fill=hdr_col, outline=COLOR_BORDER, width=2)
        draw.text(((x1 + x2) // 2, SWIM_Y1 + 20), title, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")

    # Helper for activity node
    def draw_activity(cx, cy, w, h, text, fill=(191, 219, 254), outline=COLOR_BORDER):
        draw.rounded_rectangle([(cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2)], radius=12, fill=fill, outline=outline, width=2)
        lines = text.split("\n")
        total_h = len(lines) * 16
        start_y = cy - (total_h // 2) + 7
        for i, line in enumerate(lines):
            draw.text((cx, start_y + i * 16), line, fill=COLOR_TEXT, font=fonts["small_bold"], anchor="mm")
        return cx, cy, w, h

    # Helper for decision diamond
    def draw_diamond(cx, cy, size, text):
        half = size // 2
        draw.polygon([(cx, cy - half), (cx + half, cy), (cx, cy + half), (cx - half, cy)], fill=(233, 213, 255), outline=COLOR_BORDER, width=2)
        lines = text.split("\n")
        total_h = len(lines) * 14
        start_y = cy - (total_h // 2) + 6
        for i, line in enumerate(lines):
            draw.text((cx, start_y + i * 14), line, fill=COLOR_TEXT, font=fonts["small_bold"], anchor="mm")
        return cx, cy, size

    # Helper for arrow
    def draw_conn(p1, p2, text=None, text_offset=(0, -10)):
        draw.line([p1, p2], fill=COLOR_BORDER, width=2)
        draw_arrow(draw, p1[0], p1[1], p2[0], p2[1], color=COLOR_BORDER, open_arrow=False, size=7, width=2)
        if text:
            mx = (p1[0] + p2[0]) / 2 + text_offset[0]
            my = (p1[1] + p2[1]) / 2 + text_offset[1]
            draw.text((mx, my), text, fill=COLOR_TEXT, font=fonts["small_bold"], anchor="mm")

    # --- Start Node (Black circle in Student lane) ---
    START_X = 235
    START_Y = 205
    draw.ellipse([(START_X - 12, START_Y - 12), (START_X + 12, START_Y + 12)], fill=(0, 0, 0), outline=COLOR_BORDER, width=1)
    draw.text((START_X + 32, START_Y), "Start", fill=COLOR_TEXT, font=fonts["small_bold"], anchor="lm")

    # --- Flow Steps ---
    # 1. Open Web App
    n_open = draw_activity(235, 255, 190, 38, "Open Web Application", fill=(191, 219, 254))
    draw_conn((START_X, START_Y + 12), (n_open[0], n_open[1] - 19))

    # 2. Login / Register
    n_login = draw_activity(235, 320, 190, 38, "Login / Register Account", fill=(191, 219, 254))
    draw_conn((n_open[0], n_open[1] + 19), (n_login[0], n_login[1] - 19))

    # To System: Validate Credentials
    n_val = draw_activity(610, 320, 200, 38, "Validate User Credentials", fill=(187, 247, 208))
    draw_conn((n_login[0] + 95, n_login[1]), (n_val[0] - 100, n_val[1]))

    # Decision: Valid?
    d_valid = draw_diamond(610, 395, 65, "Valid?")
    draw_conn((n_val[0], n_val[1] + 19), (d_valid[0], d_valid[1] - 32))

    # Invalid path (Red box)
    n_err = draw_activity(740, 395, 100, 32, "Show Error", fill=(254, 205, 211))
    draw_conn((d_valid[0] + 32, d_valid[1]), (n_err[0] - 50, n_err[1]), "No")
    # Loop back to login
    draw.line([(n_err[0], n_err[1] - 16), (n_err[0], 285)], fill=COLOR_BORDER, width=2)
    draw.line([(n_err[0], 285), (235, 285)], fill=COLOR_BORDER, width=2)
    draw_conn((235, 285), (n_login[0], n_login[1] - 19))

    # Valid path -> Load Dashboard
    n_dash = draw_activity(610, 480, 210, 38, "Fetch & Display Dashboard\n(Chronological Tasks)", fill=(187, 247, 208))
    draw_conn((d_valid[0], d_valid[1] + 32), (n_dash[0], n_dash[1] - 19), "Yes", text_offset=(16, 0))

    # Back to Student: Create Assignment
    n_asg = draw_activity(235, 480, 200, 38, "Create Assignment\n(Title, Due Date, Imp 1-5)", fill=(191, 219, 254))
    draw_conn((n_dash[0] - 105, n_dash[1]), (n_asg[0] + 100, n_asg[1]))

    # To System: Calculate Rank Score
    n_score = draw_activity(610, 560, 210, 38, "Calculate Priority Score\n(Imp * 1000 - Days)", fill=(187, 247, 208))
    # Route from n_asg to n_score
    draw.line([(n_asg[0], n_asg[1] + 19), (n_asg[0], 560)], fill=COLOR_BORDER, width=2)
    draw_conn((n_asg[0], 560), (n_score[0] - 105, 560))

    # To Database: Store Assignment
    n_db_asg = draw_activity(990, 560, 210, 38, "Store Assignment Record\n(Status = ACTIVE)", fill=(254, 240, 138))
    draw_conn((n_score[0] + 105, 560), (n_db_asg[0] - 105, 560))

    # Student adds checklist subtasks
    n_sub = draw_activity(235, 640, 200, 38, "Add Checklist Subtasks\n(Granular Items)", fill=(191, 219, 254))
    draw.line([(n_db_asg[0], n_db_asg[1] + 19), (n_db_asg[0], 610)], fill=COLOR_BORDER, width=2)
    draw.line([(n_db_asg[0], 610), (235, 610)], fill=COLOR_BORDER, width=2)
    draw_conn((235, 610), (n_sub[0], n_sub[1] - 19))

    # System: Save Subtasks & Init Progress (0%)
    n_sub_svc = draw_activity(610, 640, 210, 38, "Save Subtasks & Init\nProgress Bar (0%)", fill=(187, 247, 208))
    draw_conn((n_sub[0] + 100, 640), (n_sub_svc[0] - 105, 640))

    # Decision: Invite Peer?
    d_peer = draw_diamond(610, 725, 65, "Invite\nPeer?")
    draw_conn((n_sub_svc[0], n_sub_svc[1] + 19), (d_peer[0], d_peer[1] - 32))

    # If Yes -> To Collaborator
    n_inv = draw_activity(1365, 725, 210, 38, "Receive Collaboration\nInvitation Alert", fill=(254, 215, 170))
    draw_conn((d_peer[0] + 32, d_peer[1]), (n_inv[0] - 105, n_inv[1]), "Yes", text_offset=(0, -12))

    # Decision: Accept Invite?
    d_acc = draw_diamond(1365, 805, 65, "Accept\nInvite?")
    draw_conn((n_inv[0], n_inv[1] + 19), (d_acc[0], d_acc[1] - 32))

    # Decline path
    n_dec = draw_activity(1500, 805, 80, 32, "Decline", fill=(254, 205, 211))
    draw_conn((d_acc[0] + 32, d_acc[1]), (n_dec[0] - 40, n_dec[1]), "No")

    # Accept path -> Join Shared Task
    n_join = draw_activity(1365, 890, 210, 38, "Accept Request & Join\nShared Task View", fill=(254, 215, 170))
    draw_conn((d_acc[0], d_acc[1] + 32), (n_join[0], n_join[1] - 19), "Yes", text_offset=(16, 0))

    # Collaborator / Student checks off subtask
    n_chk = draw_activity(1365, 965, 210, 38, "Toggle Checklist Item\n(Mark Subtask Done)", fill=(254, 215, 170))
    draw_conn((n_join[0], n_join[1] + 19), (n_chk[0], n_chk[1] - 19))

    # No peer invite goes straight down to checklist
    draw.line([(d_peer[0] - 32, d_peer[1]), (380, d_peer[1])], fill=COLOR_BORDER, width=2)
    draw.line([(380, d_peer[1]), (380, 965)], fill=COLOR_BORDER, width=2)
    draw_conn((380, 965), (495, 965), "No", text_offset=(0, -12))

    # System updates progress percentage
    n_prog = draw_activity(610, 965, 210, 38, "Update Progress Bar %\n(completed / total)", fill=(187, 247, 208))
    draw_conn((n_chk[0] - 105, 965), (n_prog[0] + 105, 965))

    # Save to Database
    n_db_up = draw_activity(990, 965, 210, 38, "Persist Subtask & State\nto MySQL Database", fill=(254, 240, 138))
    draw_conn((n_prog[0] + 105, 965), (n_db_up[0] - 105, 965))

    # Decision: 100% Complete?
    d_done = draw_diamond(610, 1050, 65, "100%\nDone?")
    draw_conn((n_prog[0], n_prog[1] + 19), (d_done[0], d_done[1] - 32))

    # If No -> loop back to toggle subtasks
    draw.line([(d_done[0] - 32, d_done[1]), (500, d_done[1])], fill=COLOR_BORDER, width=2)
    draw.line([(500, d_done[1]), (500, 930)], fill=COLOR_BORDER, width=2)
    draw_conn((500, 930), (n_prog[0] - 105, 945), "No", text_offset=(0, -10))

    # If Yes -> Mark Assignment Done (Student)
    n_finish = draw_activity(235, 1050, 200, 38, "Mark Assignment as Done\n(Archived to Completed)", fill=(191, 219, 254))
    draw_conn((d_done[0] - 32, d_done[1]), (n_finish[0] + 100, n_finish[1]), "Yes", text_offset=(0, -12))

    # End Node (Bullseye)
    END_X = 235
    END_Y = 1125
    draw.ellipse([(END_X - 14, END_Y - 14), (END_X + 14, END_Y + 14)], outline=COLOR_BORDER, width=2, fill=(255, 255, 255))
    draw.ellipse([(END_X - 9, END_Y - 9), (END_X + 9, END_Y + 9)], fill=(0, 0, 0), outline=COLOR_BORDER, width=1)
    draw.text((END_X + 26, END_Y), "End", fill=COLOR_TEXT, font=fonts["small_bold"], anchor="lm")
    draw_conn((n_finish[0], n_finish[1] + 19), (END_X, END_Y - 14))

    # Save
    out_dir = r"c:\Users\HOME\Downloads\Assignment-Tracker-main\Assignment-Tracker-main\uml_diagrams"
    out_file = os.path.join(out_dir, "6_activity_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Diagram 6 saved at: {out_file}")

if __name__ == "__main__":
    generate_diagram_6()
