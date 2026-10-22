import os
from PIL import Image, ImageDraw, ImageFont
from diagram_helpers import (
    create_canvas, draw_top_banner, draw_actor, draw_dashed_line, draw_arrow,
    get_fonts, COLOR_BORDER, COLOR_TEXT, COLOR_MUTED
)

def generate_diagram_4():
    WIDTH = 1800
    HEIGHT = 1200
    img, draw = create_canvas(WIDTH, HEIGHT)
    fonts = get_fonts()

    # Draw Top Banner
    draw_top_banner(draw, "4. SEQUENCE DIAGRAM", "Smart Assignment Tracker", "(Create Assignment, Checklist & Collaboration)", canvas_w=WIDTH)

    # Actor: Student on far left
    ACTOR_STUDENT = (70, 190)
    draw_actor(draw, ACTOR_STUDENT[0], ACTOR_STUDENT[1], "Student", head_color=(147, 197, 253))

    # Lifeline components at top
    lifelines = [
        ("Frontend\n(React)", 270, (191, 219, 254)),
        ("Auth\nService", 480, (233, 213, 255)),
        ("Assignment\nService", 690, (254, 205, 211)),
        ("Priority\nEngine", 900, (254, 240, 138)),
        ("Subtask\nService", 1110, (187, 247, 208)),
        ("Collaboration\nService", 1320, (254, 215, 170)),
        ("Notification\nService", 1520, (254, 205, 211)),
        ("Collaborator\n(Peer)", 1700, (153, 246, 228)),
    ]

    # Draw Lifeline header boxes & vertical dashed lines
    Y_BOX = 150
    W_BOX = 115
    H_BOX = 50
    Y_LINE_START = Y_BOX + H_BOX
    Y_LINE_END = 1140

    for name, cx, col in lifelines:
        draw.rectangle([(cx - W_BOX // 2, Y_BOX), (cx + W_BOX // 2, Y_BOX + H_BOX)], fill=col, outline=COLOR_BORDER, width=2)
        lines = name.split("\n")
        if len(lines) == 1:
            draw.text((cx, Y_BOX + H_BOX // 2), lines[0], fill=COLOR_TEXT, font=fonts["body_bold"], anchor="mm")
        else:
            draw.text((cx, Y_BOX + 16), lines[0], fill=COLOR_TEXT, font=fonts["body_bold"], anchor="mm")
            draw.text((cx, Y_BOX + 34), lines[1], fill=COLOR_TEXT, font=fonts["small"], anchor="mm")

        # Dashed line
        draw_dashed_line(draw, cx, Y_LINE_START, cx, Y_LINE_END, color=(148, 163, 184), width=1)

    # Actor dashed line
    draw_dashed_line(draw, ACTOR_STUDENT[0], ACTOR_STUDENT[1] + 90, ACTOR_STUDENT[0], Y_LINE_END, color=(148, 163, 184), width=1)

    # Helper for activation bar
    def draw_activation(cx, y1, y2, fill=(255, 255, 255)):
        w = 14
        draw.rectangle([(cx - w // 2, y1), (cx + w // 2, y2)], fill=fill, outline=COLOR_BORDER, width=1)

    # Helper for message arrow
    def draw_msg(x1, x2, y, text, is_return=False):
        if is_return:
            draw_dashed_line(draw, x1, y, x2, y, color=COLOR_BORDER, width=1)
            draw_arrow(draw, x1, y, x2, y, color=COLOR_BORDER, open_arrow=True, size=8, width=1)
        else:
            draw.line([(x1, y), (x2, y)], fill=COLOR_BORDER, width=1)
            draw_arrow(draw, x1, y, x2, y, color=COLOR_BORDER, open_arrow=False, size=8, width=1)
        mx = (x1 + x2) / 2
        draw.text((mx, y - 8), text, fill=COLOR_TEXT, font=fonts["small"], anchor="mm")

    # Activation bars
    draw_activation(ACTOR_STUDENT[0], 230, 280, (219, 234, 254))
    draw_activation(ACTOR_STUDENT[0], 305, 410, (219, 234, 254))
    draw_activation(ACTOR_STUDENT[0], 435, 500, (219, 234, 254))
    draw_activation(ACTOR_STUDENT[0], 515, 595, (219, 234, 254))
    draw_activation(ACTOR_STUDENT[0], 1060, 1120, (219, 234, 254))

    draw_activation(270, 230, 1120, (191, 219, 254))
    draw_activation(480, 245, 275, (233, 213, 255))
    draw_activation(690, 320, 400, (254, 205, 211))
    draw_activation(900, 340, 370, (254, 240, 138))
    draw_activation(1110, 450, 495, (187, 247, 208))
    draw_activation(1320, 530, 910, (254, 215, 170))
    draw_activation(1520, 560, 605, (254, 205, 211))
    draw_activation(1700, 590, 900, (153, 246, 228))

    # --- Messages ---
    # Phase 1: Authentication
    draw_msg(ACTOR_STUDENT[0], 270, 240, "1. Login(email, password)")
    draw_msg(270, 480, 252, "2. authenticate(email, hash)")
    draw_msg(480, 270, 268, "3. token / session valid", is_return=True)
    draw_msg(270, ACTOR_STUDENT[0], 278, "4. Login successful", is_return=True)

    # Phase 2: Assignment Creation & Priority Scoring
    draw_msg(ACTOR_STUDENT[0], 270, 315, "5. Create Assignment(title, due_date, importance)")
    draw_msg(270, 690, 330, "6. processAssignment(data)")
    draw_msg(690, 900, 345, "7. computeRankScore(importance, due_date)")
    draw_msg(900, 690, 360, "8. rankScore = 4993", is_return=True)
    draw_msg(690, 270, 385, "9. assignmentCreated(id=201)", is_return=True)
    draw_msg(270, ACTOR_STUDENT[0], 400, "10. Display Task in Chronological List", is_return=True)

    # Phase 3: Subtasks Checklist
    draw_msg(ACTOR_STUDENT[0], 270, 445, "11. Add Checklist Subtasks(items)")
    draw_msg(270, 1110, 460, "12. batchCreateSubtasks(asgId, items)")
    draw_msg(1110, 270, 485, "13. subtasksCreated (progress=0%)", is_return=True)

    # Phase 4: Collaboration Invite
    draw_msg(ACTOR_STUDENT[0], 270, 525, "14. Invite Collaborator(peer_username)")
    draw_msg(270, 1320, 540, "15. createInvitation(asgId, peerId)")
    draw_msg(1320, 1520, 560, "16. dispatchNotification(peerId, \"You were invited\")")
    draw_msg(1520, 1700, 580, "17. New Collaboration Request Alert")

    # --- ALT Frame: Collaboration Response ---
    ALT_Y1 = 620
    ALT_Y2 = 910
    draw.rectangle([(130, ALT_Y1), (1750, ALT_Y2)], outline=COLOR_BORDER, width=2, fill=None)
    draw.rectangle([(130, ALT_Y1), (180, ALT_Y1 + 22)], fill=(254, 215, 170), outline=COLOR_BORDER, width=1)
    draw.text((155, ALT_Y1 + 11), "alt", fill=COLOR_TEXT, font=fonts["body_bold"], anchor="mm")
    draw.text((200, ALT_Y1 + 11), "[Collaborator Accepts Invite]", fill=COLOR_TEXT, font=fonts["small_bold"])

    # Accept flow
    draw_msg(1700, 1320, 655, "18. acceptCollabRequest(inviteId)")
    draw_msg(1320, 690, 675, "19. grantCollaboratorAccess(userId, asgId)")
    draw_msg(690, 1320, 695, "20. accessGranted(role=\"COLLABORATOR\")", is_return=True)
    draw_msg(1320, 1700, 715, "21. Task Added to \"Shared With Me\"", is_return=True)
    draw_msg(1320, 270, 735, "22. notifyOwner(peer accepted)", is_return=True)

    # Divider dashed line for else / decline
    DIV_Y = 770
    draw_dashed_line(draw, 130, DIV_Y, 1750, DIV_Y, color=COLOR_BORDER, width=1)
    draw.text((200, DIV_Y + 12), "[Collaborator Declines Invite]", fill=COLOR_TEXT, font=fonts["small_bold"])

    # Decline flow
    draw_msg(1700, 1320, 810, "23. declineCollabRequest(inviteId)")
    draw_msg(1320, 1700, 830, "24. inviteRemoved()", is_return=True)
    draw_msg(1320, 270, 850, "25. notifyOwner(peer declined)", is_return=True)

    # --- Phase 5: Collaborative Subtask Checklist & Completion ---
    draw_msg(1700, 270, 940, "26. Toggle Subtask Done(subtaskId=302)")
    draw_msg(270, 1110, 960, "27. updateSubtaskStatus(isCompleted=true)")
    draw_msg(1110, 690, 980, "28. recomputeProgress(completed/total)")
    draw_msg(690, 270, 1000, "29. Progress Updated (100% Complete)", is_return=True)

    # --- OPT Frame: Final Completion ---
    OPT_Y1 = 1030
    OPT_Y2 = 1130
    draw.rectangle([(130, OPT_Y1), (1750, OPT_Y2)], outline=COLOR_BORDER, width=2, fill=None)
    draw.rectangle([(130, OPT_Y1), (180, OPT_Y1 + 22)], fill=(187, 247, 208), outline=COLOR_BORDER, width=1)
    draw.text((155, OPT_Y1 + 11), "opt", fill=COLOR_TEXT, font=fonts["body_bold"], anchor="mm")
    draw.text((200, OPT_Y1 + 11), "[All Subtasks 100% Checked]", fill=COLOR_TEXT, font=fonts["small_bold"])

    draw_msg(ACTOR_STUDENT[0], 270, 1065, "30. Mark Assignment Done(asgId=201)")
    draw_msg(270, 690, 1085, "31. setStatus(COMPLETED)")
    draw_msg(690, 270, 1105, "32. Assignment Completed & Spotlight Cleared", is_return=True)

    # Save
    out_dir = r"c:\Users\HOME\Downloads\Assignment-Tracker-main\Assignment-Tracker-main\uml_diagrams"
    out_file = os.path.join(out_dir, "4_sequence_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Diagram 4 saved at: {out_file}")

if __name__ == "__main__":
    generate_diagram_4()
