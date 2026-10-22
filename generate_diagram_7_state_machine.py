import os
from PIL import Image, ImageDraw, ImageFont
from diagram_helpers import (
    create_canvas, draw_top_banner, draw_arrow,
    get_fonts, COLOR_BORDER, COLOR_TEXT, COLOR_MUTED,
    PALETTE_BLUE, PALETTE_GREEN, PALETTE_ORANGE, PALETTE_PINK, PALETTE_PURPLE, PALETTE_YELLOW, PALETTE_TEAL
)

def generate_diagram_7():
    WIDTH = 1600
    HEIGHT = 1150
    img, draw = create_canvas(WIDTH, HEIGHT)
    fonts = get_fonts()

    # Draw Top Banner
    draw_top_banner(draw, "7. STATE MACHINE DIAGRAM", "Smart Assignment Tracker", "(Assignment & Subtask Lifecycle)", canvas_w=WIDTH)

    # State box drawer helper
    def draw_state(cx, cy, w, h, state_title, desc, pal=PALETTE_BLUE):
        x1 = cx - w // 2
        y1 = cy - h // 2
        x2 = cx + w // 2
        y2 = cy + h // 2
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill=pal["fill"], outline=COLOR_BORDER, width=2)
        # Header partition
        hdr_h = 28
        draw.rounded_rectangle([(x1, y1), (x2, y1 + hdr_h)], radius=10, fill=pal["header"], outline=COLOR_BORDER, width=2)
        # Fix rounded corners overlap
        draw.rectangle([(x1, y1 + 10), (x2, y1 + hdr_h)], fill=pal["header"], outline=None)
        draw.line([(x1, y1 + hdr_h), (x2, y1 + hdr_h)], fill=COLOR_BORDER, width=1)
        draw.text((cx, y1 + 14), state_title, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")
        # Description
        lines = desc.split("\n")
        sy = y1 + hdr_h + 8
        for line in lines:
            draw.text((cx, sy), line, fill=COLOR_TEXT, font=fonts["small"], anchor="mm")
            sy += 16
        return cx, cy, w, h

    # Helper for state transition arrow with event label
    def draw_transition(p1, p2, event_text, text_offset=(0, -10)):
        draw.line([p1, p2], fill=COLOR_BORDER, width=2)
        draw_arrow(draw, p1[0], p1[1], p2[0], p2[1], color=COLOR_BORDER, open_arrow=False, size=8, width=2)
        mx = (p1[0] + p2[0]) / 2 + text_offset[0]
        my = (p1[1] + p2[1]) / 2 + text_offset[1]
        draw.text((mx, my), event_text, fill=COLOR_TEXT, font=fonts["small_bold"], anchor="mm")

    # --- Start Node ---
    START_X = 520
    START_Y = 160
    draw.ellipse([(START_X - 14, START_Y - 14), (START_X + 14, START_Y + 14)], fill=(0, 0, 0), outline=COLOR_BORDER, width=1)
    draw.text((START_X + 30, START_Y), "Start", fill=COLOR_TEXT, font=fonts["heading"], anchor="lm")

    # --- States ---
    # 1. DRAFT / CREATED (Top Center)
    s_draft = draw_state(520, 250, 260, 68, "DRAFT / CREATED", "Assignment initialized,\nawaiting subtasks & schedule", PALETTE_BLUE)
    draw_transition((START_X, START_Y + 14), (s_draft[0], s_draft[1] - 34), "createAssignment()")

    # 2. CANCELLED / DELETED (Top Right)
    s_cancel = draw_state(1200, 250, 260, 68, "CANCELLED / DELETED", "Assignment deleted by owner\nor discarded from list", PALETTE_PINK)
    draw_transition((s_draft[0] + 130, s_draft[1]), (s_cancel[0] - 130, s_cancel[1]), "deleteAssignment()")

    # 3. ACTIVE_IN_PROGRESS (Below Draft)
    s_active = draw_state(520, 420, 280, 72, "ACTIVE / IN_PROGRESS", "Task published, checklist items pending,\npriority score calculated", PALETTE_GREEN)
    draw_transition((s_draft[0], s_draft[1] + 34), (s_active[0], s_active[1] - 36), "addSubtasks() & publish()")

    # Active to Cancelled
    draw.line([(s_active[0] + 140, s_active[1]), (1200, s_active[1])], fill=COLOR_BORDER, width=2)
    draw_transition((1200, s_active[1]), (s_cancel[0], s_cancel[1] + 34), "deleteTask()", text_offset=(35, -20))

    # 4. COLLAB_PENDING (Left of Active)
    s_pending = draw_state(160, 420, 250, 72, "COLLABORATION_PENDING", "Invite sent to peer,\nwaiting for acceptance", PALETTE_YELLOW)
    draw_transition((s_active[0] - 140, s_active[1] - 15), (s_pending[0] + 125, s_pending[1] - 15), "inviteCollaborator()")
    draw_transition((s_pending[0] + 125, s_pending[1] + 15), (s_active[0] - 140, s_active[1] + 15), "declineInvite()", text_offset=(0, 12))

    # 5. SHARED_ACTIVE (Below Active)
    s_shared = draw_state(520, 590, 280, 72, "SHARED_ACTIVE", "Peer accepted, collaborative\nchecklist execution active", PALETTE_PURPLE)
    # Collab Pending to Shared Active
    p_pen1 = (s_pending[0], s_pending[1] + 36)
    p_pen2 = (s_pending[0], s_shared[1])
    draw.line([p_pen1, p_pen2], fill=COLOR_BORDER, width=2)
    draw_transition(p_pen2, (s_shared[0] - 140, s_shared[1]), "acceptInvite()", text_offset=(-20, -10))

    # 6. OVERDUE / URGENT (Below Shared Active)
    s_overdue = draw_state(520, 760, 280, 72, "OVERDUE / URGENT", "Deadline approached or passed,\nPriority Spotlight active", PALETTE_ORANGE)
    draw_transition((s_shared[0], s_shared[1] + 36), (s_overdue[0], s_overdue[1] - 36), "deadlineExceeded()")

    # Overdue to Cancelled
    draw.line([(s_overdue[0] - 140, s_overdue[1]), (s_overdue[0] - 140, s_overdue[1] + 60)], fill=COLOR_BORDER, width=2)

    # 7. REVIEW_READY (Right of Shared Active)
    s_review = draw_state(1000, 590, 260, 72, "REVIEW_READY", "All subtasks 100% checked,\nawaiting final completion", PALETTE_TEAL)
    draw_transition((s_shared[0] + 140, s_shared[1]), (s_review[0] - 130, s_review[1]), "allSubtasksCompleted()")

    # Active straight to Review (if solo task)
    p_act_rev1 = (s_active[0] + 100, s_active[1] + 36)
    p_act_rev2 = (s_active[0] + 100, 510)
    p_act_rev3 = (s_review[0], 510)
    draw.line([p_act_rev1, p_act_rev2], fill=COLOR_BORDER, width=2)
    draw.line([p_act_rev2, p_act_rev3], fill=COLOR_BORDER, width=2)
    draw_transition(p_act_rev3, (s_review[0], s_review[1] - 36), "100% subtasks done", text_offset=(0, -12))

    # Overdue to Review
    p_over_rev1 = (s_overdue[0] + 140, s_overdue[1])
    p_over_rev2 = (s_review[0], s_overdue[1])
    draw.line([p_over_rev1, p_over_rev2], fill=COLOR_BORDER, width=2)
    draw_transition(p_over_rev2, (s_review[0], s_review[1] + 36), "finishOverdueTasks()", text_offset=(50, 0))

    # 8. COMPLETED (Below Review Ready)
    s_done = draw_state(1000, 760, 260, 72, "COMPLETED", "Assignment officially marked done,\narchived into Completed view", PALETTE_GREEN)
    draw_transition((s_review[0], s_review[1] + 36), (s_done[0], s_done[1] - 36), "markAssignmentDone()")

    # End Node (Bullseye)
    END_X = 1000
    END_Y = 890
    draw.ellipse([(END_X - 16, END_Y - 16), (END_X + 16, END_Y + 16)], outline=COLOR_BORDER, width=2, fill=(255, 255, 255))
    draw.ellipse([(END_X - 10, END_Y - 10), (END_X + 10, END_Y + 10)], fill=(0, 0, 0), outline=COLOR_BORDER, width=1)
    draw.text((END_X + 30, END_Y), "End", fill=COLOR_TEXT, font=fonts["heading"], anchor="lm")
    draw_transition((s_done[0], s_done[1] + 36), (END_X, END_Y - 16), "archive()")

    # --- Possible States Card (Bottom Right, matching friend's layout) ---
    CARD_X = 850
    CARD_Y = 945
    CARD_W = 680
    CARD_H = 185
    draw.rectangle([(CARD_X, CARD_Y), (CARD_X + CARD_W, CARD_Y + CARD_H)], fill=(235, 246, 254), outline=COLOR_BORDER, width=2)
    draw.rectangle([(CARD_X, CARD_Y), (CARD_X + CARD_W, CARD_Y + 30)], fill=(191, 219, 254), outline=COLOR_BORDER, width=2)
    draw.text((CARD_X + CARD_W // 2, CARD_Y + 15), "Possible States Description", fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")

    states_legend = [
        ("1. DRAFT / CREATED", ": Initial task entry with title, due date, category & importance"),
        ("2. ACTIVE / IN_PROGRESS", ": Ongoing task where student works through checklist items"),
        ("3. COLLABORATION_PENDING", ": Collaboration invite dispatched to peer, awaiting response"),
        ("4. SHARED_ACTIVE", ": Accepted peer collaboration; real-time subtask synchronization"),
        ("5. OVERDUE / URGENT", ": Deadline exceeded; task promoted to priority spotlight"),
        ("6. REVIEW_READY", ": All granular subtasks verified 100% complete"),
        ("7. COMPLETED", ": Final confirmation; task marked done and removed from active list"),
        ("8. CANCELLED / DELETED", ": Task removed by owner or cancelled by mutual consensus")
    ]

    ly = CARD_Y + 38
    for st_title, st_desc in states_legend:
        draw.text((CARD_X + 16, ly), st_title, fill=COLOR_TEXT, font=fonts["small_bold"])
        draw.text((CARD_X + 220, ly), st_desc, fill=COLOR_TEXT, font=fonts["small"])
        ly += 17

    # Save
    out_dir = r"c:\Users\HOME\Downloads\Assignment-Tracker-main\Assignment-Tracker-main\uml_diagrams"
    out_file = os.path.join(out_dir, "7_state_machine_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Diagram 7 saved at: {out_file}")

if __name__ == "__main__":
    generate_diagram_7()
