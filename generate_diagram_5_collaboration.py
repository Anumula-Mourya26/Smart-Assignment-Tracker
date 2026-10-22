import os
from PIL import Image, ImageDraw, ImageFont
from diagram_helpers import (
    create_canvas, draw_top_banner, draw_actor, draw_arrow,
    get_fonts, COLOR_BORDER, COLOR_TEXT, COLOR_MUTED,
    PALETTE_BLUE, PALETTE_GREEN, PALETTE_ORANGE, PALETTE_PINK, PALETTE_PURPLE, PALETTE_YELLOW, PALETTE_TEAL
)

def generate_diagram_5():
    WIDTH = 1650
    HEIGHT = 1150
    img, draw = create_canvas(WIDTH, HEIGHT)
    fonts = get_fonts()

    # Draw Top Banner
    draw_top_banner(draw, "5. COLLABORATION DIAGRAM", "Smart Assignment Tracker", "(Create Assignment, Subtasks & Team Collaboration)", canvas_w=WIDTH)

    # Box drawer helper
    def draw_obj_box(x, y, w, h, title, subtitle=None, pal=PALETTE_BLUE):
        draw.rectangle([(x, y), (x + w, y + h)], fill=pal["fill"], outline=COLOR_BORDER, width=2)
        draw.rectangle([(x, y), (x + w, y + 26)], fill=pal["header"], outline=COLOR_BORDER, width=2)
        draw.text((x + w // 2, y + 13), title, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")
        if subtitle:
            draw.text((x + w // 2, y + (h + 26) // 2), subtitle, fill=COLOR_TEXT, font=fonts["small"], anchor="mm")
        return x, y, w, h

    # Actors: Student on Left, Collaborator on Right
    ACTOR_STUDENT = (90, 240)
    draw_actor(draw, ACTOR_STUDENT[0], ACTOR_STUDENT[1], ": Student\n(Owner)", head_color=(147, 197, 253))

    ACTOR_COLLAB = (1540, 890)
    draw_actor(draw, ACTOR_COLLAB[0], ACTOR_COLLAB[1], ": Collaborator\n(Peer)", head_color=(153, 246, 228))

    # Object boxes (Clean, well-spaced layout)
    b_fe = draw_obj_box(300, 180, 220, 65, ": Frontend", "(React SPA)", PALETTE_BLUE)
    b_auth = draw_obj_box(740, 180, 220, 65, ": AuthService", "(JWT / Password Hash)", PALETTE_PINK)

    b_ctrl = draw_obj_box(300, 370, 250, 75, ": AssignmentController", "(REST API Gateway)", PALETTE_PURPLE)

    b_prio = draw_obj_box(740, 370, 220, 75, ": PriorityEngine", "(Rank Score Algorithm)", PALETTE_YELLOW)
    b_asg_svc = draw_obj_box(300, 560, 250, 75, ": AssignmentService", "(Core Business Logic)", PALETTE_PINK)
    b_asg_ent = draw_obj_box(740, 560, 220, 65, ": Assignment", "(Domain Entity)", PALETTE_BLUE)

    b_sub_svc = draw_obj_box(300, 750, 250, 75, ": SubtaskService", "(Checklist Manager)", PALETTE_GREEN)
    b_sub_ent = draw_obj_box(740, 750, 220, 65, ": Subtask", "(Checklist Item)", PALETTE_BLUE)

    b_col_svc = draw_obj_box(300, 940, 250, 75, ": CollaborationService", "(Invite & Access Control)", PALETTE_ORANGE)
    b_col_ent = draw_obj_box(740, 940, 220, 65, ": Collaboration", "(Team Share Entity)", PALETTE_YELLOW)

    b_notif_svc = draw_obj_box(1140, 940, 230, 75, ": NotificationService", "(Dispatch & Alerts)", PALETTE_PURPLE)

    # Helper for link with numbered message text & directional arrow
    def draw_msg_link(p1, p2, messages=[]):
        draw.line([p1, p2], fill=COLOR_BORDER, width=2)
        for msg, mx, my, arr_dir in messages:
            draw.text((mx, my), msg, fill=COLOR_TEXT, font=fonts["small"])
            bbox = draw.textbbox((mx, my), msg, font=fonts["small"])
            ax = bbox[2] + 8
            ay = my + 6
            if arr_dir == "right":
                draw.line([(ax, ay), (ax + 12, ay)], fill=COLOR_BORDER, width=1)
                draw_arrow(draw, ax, ay, ax + 12, ay, color=COLOR_BORDER, size=5, width=1)
            elif arr_dir == "left":
                draw.line([(ax + 12, ay), (ax, ay)], fill=COLOR_BORDER, width=1)
                draw_arrow(draw, ax + 12, ay, ax, ay, color=COLOR_BORDER, size=5, width=1)
            elif arr_dir == "up":
                draw.line([(ax, ay + 6), (ax, ay - 6)], fill=COLOR_BORDER, width=1)
                draw_arrow(draw, ax, ay + 6, ax, ay - 6, color=COLOR_BORDER, size=5, width=1)
            elif arr_dir == "down":
                draw.line([(ax, ay - 6), (ax, ay + 6)], fill=COLOR_BORDER, width=1)
                draw_arrow(draw, ax, ay - 6, ax, ay + 6, color=COLOR_BORDER, size=5, width=1)

    # 1. Student <-> Frontend (horizontal line)
    draw_msg_link(
        (ACTOR_STUDENT[0] + 30, b_fe[1] + 32), (b_fe[0], b_fe[1] + 32),
        messages=[
            ("1: login()", 155, 155, "right"),
            ("2: createAssignment()", 135, 175, "right"),
            ("3: addSubtasks()", 145, 195, "right"),
            ("4: invitePeer()", 155, 215, "right")
        ]
    )

    # 2. Frontend <-> AuthService (horizontal line)
    draw_msg_link(
        (b_fe[0] + b_fe[2], b_fe[1] + 32), (b_auth[0], b_auth[1] + 32),
        messages=[
            ("5: authenticate(email, hash)", 530, 165, "right"),
            ("6: return JWT token", 545, 225, "left")
        ]
    )

    # 3. Frontend <-> AssignmentController (vertical line)
    draw_msg_link(
        (b_fe[0] + 125, b_fe[1] + b_fe[3]), (b_ctrl[0] + 125, b_ctrl[1]),
        messages=[
            ("7: postAssignment()", 435, 275, "down"),
            ("8: postSubtasks()", 435, 300, "down"),
            ("9: postInvite()", 435, 325, "down")
        ]
    )

    # 4. AssignmentController <-> PriorityEngine (horizontal line)
    draw_msg_link(
        (b_ctrl[0] + b_ctrl[2], b_ctrl[1] + 37), (b_prio[0], b_prio[1] + 37),
        messages=[
            ("10: computeRankScore(imp, due)", 560, 345, "right"),
            ("11: rankScore = 4993", 580, 395, "left")
        ]
    )

    # 5. AssignmentController <-> AssignmentService (vertical line)
    draw_msg_link(
        (b_ctrl[0] + 125, b_ctrl[1] + b_ctrl[3]), (b_asg_svc[0] + 125, b_asg_svc[1]),
        messages=[
            ("12: createAssignment(data, score)", 435, 470, "down"),
            ("13: assignmentCreated(id=201)", 435, 505, "up")
        ]
    )

    # 6. AssignmentService <-> Assignment (Entity) (horizontal line)
    draw_msg_link(
        (b_asg_svc[0] + b_asg_svc[2], b_asg_svc[1] + 37), (b_asg_ent[0], b_asg_ent[1] + 37),
        messages=[
            ("14: saveAssignment()", 565, 535, "right"),
            ("15: status = ACTIVE", 575, 580, "left")
        ]
    )

    # 7. AssignmentService <-> SubtaskService (vertical line)
    draw_msg_link(
        (b_asg_svc[0] + 125, b_asg_svc[1] + b_asg_svc[3]), (b_sub_svc[0] + 125, b_sub_svc[1]),
        messages=[
            ("16: addChecklistItems(items)", 435, 660, "down"),
            ("17: checklistCreated(total=3)", 435, 695, "up")
        ]
    )

    # 8. SubtaskService <-> Subtask (Entity) (horizontal line)
    draw_msg_link(
        (b_sub_svc[0] + b_sub_svc[2], b_sub_svc[1] + 37), (b_sub_ent[0], b_sub_ent[1] + 37),
        messages=[
            ("18: batchSaveSubtasks()", 565, 725, "right"),
            ("19: subtasksSaved", 580, 770, "left")
        ]
    )

    # 9. SubtaskService <-> CollaborationService (vertical line)
    draw_msg_link(
        (b_sub_svc[0] + 125, b_sub_svc[1] + b_sub_svc[3]), (b_col_svc[0] + 125, b_col_svc[1]),
        messages=[
            ("20: inviteCollaborator(peerId)", 435, 850, "down"),
            ("21: collabPending(id=401)", 435, 885, "up")
        ]
    )

    # 10. CollaborationService <-> Collaboration (Entity) (horizontal line)
    draw_msg_link(
        (b_col_svc[0] + b_col_svc[2], b_col_svc[1] + 37), (b_col_ent[0], b_col_ent[1] + 37),
        messages=[
            ("22: saveCollabRecord()", 565, 915, "right"),
            ("23: status = PENDING", 575, 960, "left")
        ]
    )

    # 11. Collaboration (Entity) <-> NotificationService (horizontal line)
    draw_msg_link(
        (b_col_ent[0] + b_col_ent[2], b_col_ent[1] + 37), (b_notif_svc[0], b_notif_svc[1] + 37),
        messages=[
            ("24: sendInviteAlert(peerId)", 970, 915, "right"),
            ("25: alertQueued", 990, 960, "left")
        ]
    )

    # 12. NotificationService <-> Collaborator (horizontal line)
    draw_msg_link(
        (b_notif_svc[0] + b_notif_svc[2], b_notif_svc[1] + 37), (ACTOR_COLLAB[0] - 25, b_notif_svc[1] + 37),
        messages=[
            ("26: notifyInvite()", 1385, 955, "right")
        ]
    )

    # 13. Collaborator <-> Collaboration (Entity) (Accept Flow - clean line underneath)
    draw.line([(ACTOR_COLLAB[0] - 10, ACTOR_COLLAB[1] + 50), (b_col_ent[0] + 110, ACTOR_COLLAB[1] + 50)], fill=COLOR_BORDER, width=2)
    draw.line([(b_col_ent[0] + 110, ACTOR_COLLAB[1] + 50), (b_col_ent[0] + 110, b_col_ent[1] + b_col_ent[3])], fill=COLOR_BORDER, width=2)
    draw.text((1050, 1030), "27: acceptCollabRequest(collabId)", fill=COLOR_TEXT, font=fonts["small"])
    draw.text((1050, 1055), "28: accessGranted(\"Shared With Me\")", fill=COLOR_TEXT, font=fonts["small"])

    # 14. Collaborator updates subtask status -> Subtask (Entity) (clean route above)
    draw.line([(ACTOR_COLLAB[0] - 10, ACTOR_COLLAB[1] - 50), (1450, 785)], fill=COLOR_BORDER, width=2)
    draw.line([(1450, 785), (b_sub_ent[0] + b_sub_ent[2], 785)], fill=COLOR_BORDER, width=2)
    draw.text((1000, 765), "29: toggleSubtaskDone(subtaskId=302)", fill=COLOR_TEXT, font=fonts["small"])
    draw.text((1000, 795), "30: updateProgress(100% Complete)", fill=COLOR_TEXT, font=fonts["small"])

    # Save
    out_dir = r"c:\Users\HOME\Downloads\Assignment-Tracker-main\Assignment-Tracker-main\uml_diagrams"
    out_file = os.path.join(out_dir, "5_collaboration_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Diagram 5 saved at: {out_file}")

if __name__ == "__main__":
    generate_diagram_5()
