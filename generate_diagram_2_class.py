import os
from PIL import Image, ImageDraw, ImageFont
from diagram_helpers import (
    create_canvas, draw_top_banner, get_fonts,
    PALETTE_BLUE, PALETTE_GREEN, PALETTE_ORANGE, PALETTE_PINK, PALETTE_PURPLE, PALETTE_YELLOW, PALETTE_TEAL,
    COLOR_BORDER, COLOR_TEXT, COLOR_MUTED, WIDTH, HEIGHT
)

def generate_diagram_2():
    img, draw = create_canvas(1600, 1100)
    fonts = get_fonts()

    # Draw Top Banner
    draw_top_banner(draw, "2. CLASS DIAGRAM", "Smart Assignment Tracker", "(Entities, Attributes, Methods & Relationships)")

    # Box drawer helper
    def draw_box(x, y, w, title, stereotype=None, attributes=[], methods=[], pal=PALETTE_BLUE):
        head_h = 32 if not stereotype else 44
        attr_h = max(20, len(attributes) * 17 + 8)
        meth_h = max(20, len(methods) * 17 + 8) if methods else 0
        tot_h = head_h + attr_h + meth_h

        draw.rectangle([(x, y), (x + w, y + tot_h)], fill=pal["fill"], outline=COLOR_BORDER, width=2)
        draw.rectangle([(x, y), (x + w, y + head_h)], fill=pal["header"], outline=COLOR_BORDER, width=2)

        if stereotype:
            draw.text((x + w // 2, y + 13), stereotype, fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")
            draw.text((x + w // 2, y + 31), title, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")
        else:
            draw.text((x + w // 2, y + 16), title, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")

        ay = y + head_h + 6
        for a in attributes:
            draw.text((x + 8, ay), a, fill=COLOR_TEXT, font=fonts["small"])
            ay += 17

        if methods:
            draw.line([(x, y + head_h + attr_h), (x + w, y + head_h + attr_h)], fill=COLOR_BORDER, width=1)
            my = y + head_h + attr_h + 6
            for m in methods:
                draw.text((x + 8, my), m, fill=COLOR_TEXT, font=fonts["small"])
                my += 17

        return x, y, w, tot_h

    # 1. User Class (Parent)
    u_box = draw_box(
        220, 140, 240, "User",
        attributes=[
            "- userId: Long",
            "- username: String",
            "- email: String",
            "- passwordHash: String",
            "- role: Role",
            "- isActive: boolean",
            "- createdAt: LocalDateTime"
        ],
        methods=[
            "+ login(): boolean",
            "+ logout(): void",
            "+ updateProfile(): void",
            "+ changePassword(): void"
        ],
        pal=PALETTE_PURPLE
    )

    # 2. Inheritance Subclasses: Student, Collaborator, Admin
    s_box = draw_box(
        30, 420, 200, "Student",
        attributes=[
            "- studentId: Long",
            "- academicTerm: String",
            "- department: String",
            "- totalTasks: int"
        ],
        methods=[
            "+ createAssignment(): void",
            "+ viewCalendar(): void",
            "+ inviteCollaborator(): void",
            "+ markTaskDone(): void"
        ],
        pal=PALETTE_BLUE
    )

    c_box = draw_box(
        250, 420, 200, "Collaborator",
        attributes=[
            "- collabId: Long",
            "- peerUsername: String",
            "- acceptedInvites: int",
            "- pendingInvites: int"
        ],
        methods=[
            "+ viewSharedTasks(): void",
            "+ acceptInvite(): void",
            "+ declineInvite(): void",
            "+ toggleSubtask(): void"
        ],
        pal=PALETTE_GREEN
    )

    a_box = draw_box(
        470, 420, 200, "Admin",
        attributes=[
            "- adminId: Long",
            "- securityBadge: String",
            "- accessLevel: int"
        ],
        methods=[
            "+ manageUsers(): void",
            "+ manageAssignments(): void",
            "+ viewReports(): void",
            "+ monitorDatabase(): void"
        ],
        pal=PALETTE_ORANGE
    )

    # Generalization line from subclasses to User
    user_bottom_mid = (u_box[0] + u_box[2] // 2, u_box[1] + u_box[3])
    stem_y = 390
    draw.line([user_bottom_mid, (user_bottom_mid[0], stem_y)], fill=COLOR_BORDER, width=2)
    # Hollow triangle at User bottom
    draw.polygon([
        user_bottom_mid,
        (user_bottom_mid[0] - 10, user_bottom_mid[1] + 16),
        (user_bottom_mid[0] + 10, user_bottom_mid[1] + 16)
    ], fill=(255, 255, 255), outline=COLOR_BORDER)

    # Horizontal bar for 3 children
    draw.line([(s_box[0] + s_box[2] // 2, stem_y), (a_box[0] + a_box[2] // 2, stem_y)], fill=COLOR_BORDER, width=2)
    # Stems down to each child
    draw.line([(s_box[0] + s_box[2] // 2, stem_y), (s_box[0] + s_box[2] // 2, s_box[1])], fill=COLOR_BORDER, width=2)
    draw.line([(c_box[0] + c_box[2] // 2, stem_y), (c_box[0] + c_box[2] // 2, c_box[1])], fill=COLOR_BORDER, width=2)
    draw.line([(a_box[0] + a_box[2] // 2, stem_y), (a_box[0] + a_box[2] // 2, a_box[1])], fill=COLOR_BORDER, width=2)

    # 3. Category Class
    cat_box = draw_box(
        540, 140, 220, "Category",
        attributes=[
            "- categoryId: Long",
            "- name: CategoryType",
            "- description: String",
            "- colorCode: String",
            "- isActive: boolean"
        ],
        methods=[
            "+ addCategory(): void",
            "+ filterAssignments(): List",
            "+ deleteCategory(): void"
        ],
        pal=PALETTE_TEAL
    )

    # 4. Assignment Class (Center core domain)
    asg_box = draw_box(
        600, 480, 260, "Assignment",
        attributes=[
            "- assignmentId: Long",
            "- userId: Long",
            "- title: String",
            "- description: String",
            "- dueDate: LocalDate",
            "- category: CategoryType",
            "- importance: int (1-5)",
            "- priorityScore: int",
            "- isCompleted: boolean",
            "- createdAt: LocalDateTime"
        ],
        methods=[
            "+ calculatePriorityScore(): int",
            "+ markCompleted(): void",
            "+ getChecklistProgress(): double",
            "+ addSubtask(): void",
            "+ updateAssignment(): void"
        ],
        pal=PALETTE_PINK
    )

    # 5. Subtask Class (Composition from Assignment)
    sub_box = draw_box(
        950, 480, 240, "Subtask",
        attributes=[
            "- subtaskId: Long",
            "- assignmentId: Long",
            "- title: String",
            "- isCompleted: boolean",
            "- orderIndex: int",
            "- completedByUserId: Long"
        ],
        methods=[
            "+ toggleStatus(): void",
            "+ updateTitle(): void",
            "+ removeSubtask(): void"
        ],
        pal=PALETTE_BLUE
    )

    # Composition diamond from Assignment to Subtask
    # Filled black diamond at Assignment
    asg_right = (asg_box[0] + asg_box[2], asg_box[1] + 60)
    sub_left = (sub_box[0], sub_box[1] + 60)
    draw.line([(asg_right[0] + 16, asg_right[1]), sub_left], fill=COLOR_BORDER, width=2)
    # Diamond
    draw.polygon([
        asg_right,
        (asg_right[0] + 8, asg_right[1] - 6),
        (asg_right[0] + 16, asg_right[1]),
        (asg_right[0] + 8, asg_right[1] + 6)
    ], fill=COLOR_BORDER, outline=COLOR_BORDER)
    # Multiplicity
    draw.text((asg_right[0] + 20, asg_right[1] - 12), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((sub_left[0] - 16, sub_left[1] - 12), "0..*", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text(((asg_right[0] + sub_left[0]) // 2, asg_right[1] - 14), "contains", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # 6. Collaboration Class
    collab_entity_box = draw_box(
        220, 770, 260, "Collaboration",
        attributes=[
            "- collabId: Long",
            "- assignmentId: Long",
            "- senderId: Long",
            "- receiverId: Long",
            "- status: CollabStatus",
            "- invitedAt: LocalDateTime",
            "- respondedAt: LocalDateTime"
        ],
        methods=[
            "+ sendInvite(): void",
            "+ acceptInvite(): void",
            "+ declineInvite(): void",
            "+ removeCollaborator(): void"
        ],
        pal=PALETTE_YELLOW
    )

    # 7. CalendarSchedule Class
    cal_box = draw_box(
        600, 830, 260, "CalendarSchedule",
        attributes=[
            "- scheduleId: Long",
            "- date: LocalDate",
            "- totalTasksDue: int",
            "- workloadIntensity: int",
            "- topPriorityTaskTitle: String"
        ],
        methods=[
            "+ getTasksForDay(): List<Assignment>",
            "+ computeDailyWorkload(): int",
            "+ getMonthHeatmapGrid(): Map"
        ],
        pal=PALETTE_TEAL
    )

    # 8. Notification Class
    notif_box = draw_box(
        950, 780, 240, "Notification",
        attributes=[
            "- notificationId: Long",
            "- userId: Long",
            "- message: String",
            "- type: NotificationType",
            "- isRead: boolean",
            "- createdAt: LocalDateTime"
        ],
        methods=[
            "+ markAsRead(): void",
            "+ dispatchAlert(): void",
            "+ deleteNotification(): void"
        ],
        pal=PALETTE_PURPLE
    )

    # 9. PrioritySpotlight Engine Class (Utility / Domain service)
    spot_box = draw_box(
        880, 140, 240, "PrioritySpotlight",
        attributes=[
            "- calculationFormula: String",
            "- importanceWeight: int = 1000",
            "- daysWeight: int = 1",
            "- spotlightThreshold: int"
        ],
        methods=[
            "+ getTopIncompleteTask(): Assignment",
            "+ rankAssignments(): List<Assignment>",
            "+ getUrgentAlerts(): List"
        ],
        pal=PALETTE_ORANGE
    )

    # --- ENUMERATIONS (Right Side, yellow boxes like friend's diagram) ---
    def draw_enum(x, y, w, title, items):
        head_h = 36
        tot_h = head_h + len(items) * 16 + 8
        draw.rectangle([(x, y), (x + w, y + tot_h)], fill=(254, 252, 232), outline=COLOR_BORDER, width=2)
        draw.rectangle([(x, y), (x + w, y + head_h)], fill=(254, 240, 138), outline=COLOR_BORDER, width=2)
        draw.text((x + w // 2, y + 11), "«enumeration»", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")
        draw.text((x + w // 2, y + 26), title, fill=COLOR_TEXT, font=fonts["heading"], anchor="mm")
        iy = y + head_h + 6
        for item in items:
            draw.text((x + 12, iy), item, fill=COLOR_TEXT, font=fonts["small_bold"])
            iy += 16
        return x, y, w, tot_h

    EX = 1350
    draw_enum(EX, 140, 200, "CollabStatus", ["PENDING", "ACCEPTED", "DECLINED", "REMOVED"])
    draw_enum(EX, 320, 200, "CategoryType", ["COURSEWORK", "PROJECT", "EXAM_PREP", "PERSONAL", "LAB_REPORT"])
    draw_enum(EX, 500, 200, "PriorityLevel", ["CRITICAL", "HIGH", "MEDIUM", "LOW"])
    draw_enum(EX, 680, 200, "NotificationType", ["INVITE_RECEIVED", "INVITE_ACCEPTED", "DEADLINE_ALERT", "SUBTASK_DONE", "ASSIGNMENT_COMPLETED"])

    # --- ASSOCIATIONS ---
    # User has Cart / Assignment
    draw.line([(cat_box[0], cat_box[1] + 80), (u_box[0] + u_box[2], cat_box[1] + 80)], fill=COLOR_BORDER, width=2)
    draw.text((cat_box[0] - 12, cat_box[1] + 66), "0..*", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((u_box[0] + u_box[2] + 8, cat_box[1] + 66), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text(((cat_box[0] + u_box[0] + u_box[2]) // 2, cat_box[1] + 68), "categorizes", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # Student creates Assignment (dogleg routing cleanly under Student/Admin)
    p1 = (s_box[0] + 80, s_box[1] + s_box[3])
    p2 = (s_box[0] + 80, 680)
    p3 = (asg_box[0], 680)
    draw.line([p1, p2], fill=COLOR_BORDER, width=2)
    draw.line([p2, p3], fill=COLOR_BORDER, width=2)
    draw.text((p1[0] + 6, p1[1] + 8), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((p3[0] - 16, p3[1] - 12), "0..*", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text(((p2[0] + p3[0]) // 2 - 40, p2[1] - 12), "maintains", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # Assignment to CalendarSchedule (generates / maps)
    draw.line([(asg_box[0] + 100, asg_box[1] + asg_box[3]), (asg_box[0] + 100, cal_box[1])], fill=COLOR_BORDER, width=2)
    draw.text((asg_box[0] + 108, asg_box[1] + asg_box[3] + 4), "1..*", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((asg_box[0] + 108, cal_box[1] - 14), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((asg_box[0] + 130, (asg_box[1] + asg_box[3] + cal_box[1]) // 2), "schedules", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="lm")

    # Assignment to Collaboration
    draw.line([(asg_box[0], asg_box[1] + asg_box[3] - 40), (collab_entity_box[0] + collab_entity_box[2], collab_entity_box[1] + 40)], fill=COLOR_BORDER, width=2)
    draw.text((asg_box[0] - 16, asg_box[1] + asg_box[3] - 54), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((collab_entity_box[0] + collab_entity_box[2] + 8, collab_entity_box[1] + 26), "0..*", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text(((asg_box[0] + collab_entity_box[0] + collab_entity_box[2]) // 2, (asg_box[1] + asg_box[3] - 40 + collab_entity_box[1] + 40) // 2 - 10), "shares via", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # Assignment generates Notifications
    draw.line([(asg_box[0] + asg_box[2], asg_box[1] + asg_box[3] - 20), (notif_box[0], notif_box[1] + 30)], fill=COLOR_BORDER, width=2)
    draw.text((asg_box[0] + asg_box[2] + 8, asg_box[1] + asg_box[3] - 34), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((notif_box[0] - 20, notif_box[1] + 16), "0..*", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text(((asg_box[0] + asg_box[2] + notif_box[0]) // 2, (asg_box[1] + asg_box[3] - 20 + notif_box[1] + 30) // 2 - 10), "generates", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # Save
    out_dir = r"c:\Users\HOME\Downloads\Assignment-Tracker-main\Assignment-Tracker-main\uml_diagrams"
    out_file = os.path.join(out_dir, "2_class_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Diagram 2 saved at: {out_file}")

if __name__ == "__main__":
    generate_diagram_2()
