import os
from PIL import Image, ImageDraw, ImageFont
from diagram_helpers import (
    create_canvas, draw_top_banner, get_fonts, draw_object_box,
    PALETTE_BLUE, PALETTE_GREEN, PALETTE_ORANGE, PALETTE_PINK, PALETTE_PURPLE, PALETTE_YELLOW, PALETTE_TEAL,
    COLOR_BORDER, COLOR_TEXT, COLOR_MUTED, WIDTH, HEIGHT
)

def generate_diagram_3():
    img, draw = create_canvas(1600, 1100)
    fonts = get_fonts()

    # Draw Top Banner
    draw_top_banner(draw, "3. OBJECT DIAGRAM", "Smart Assignment Tracker", "(Example Instance / Runtime Snapshot)")

    # 1. student1 : Student (Top Left)
    s1 = draw_object_box(
        draw, 40, 150, 240, "student1 : Student",
        attributes=[
            "userId = 101",
            "username = \"mourya26\"",
            "email = \"mourya26@gmail.com\"",
            "academicTerm = \"Fall 2026\"",
            "totalAssignments = 8",
            "completedAssignments = 5",
            "isActive = true"
        ],
        palette=PALETTE_PURPLE
    )

    # 2. assignment1 : Assignment (Center Top)
    asg1 = draw_object_box(
        draw, 400, 150, 290, "assignment1 : Assignment",
        attributes=[
            "assignmentId = 201",
            "userId = 101",
            "title = \"OS Lab 3: CPU Scheduling\"",
            "category = \"COURSEWORK\"",
            "dueDate = 2026-10-28",
            "importance = 5",
            "priorityScore = 4993",
            "isCompleted = false",
            "progress = 66.7%"
        ],
        palette=PALETTE_PINK
    )

    # 3. Subtasks: subtask1, subtask2, subtask3 (Right Top)
    sub1 = draw_object_box(
        draw, 810, 140, 310, "subtask1 : Subtask",
        attributes=[
            "subtaskId = 301",
            "assignmentId = 201",
            "title = \"Implement Round Robin Algo\"",
            "isCompleted = true",
            "orderIndex = 1",
            "completedBy = \"mourya26\""
        ],
        palette=PALETTE_BLUE
    )

    sub2 = draw_object_box(
        draw, 810, 300, 310, "subtask2 : Subtask",
        attributes=[
            "subtaskId = 302",
            "assignmentId = 201",
            "title = \"Benchmark Priority Scheduling\"",
            "isCompleted = true",
            "orderIndex = 2",
            "completedBy = \"rahul_k\""
        ],
        palette=PALETTE_BLUE
    )

    sub3 = draw_object_box(
        draw, 810, 460, 310, "subtask3 : Subtask",
        attributes=[
            "subtaskId = 303",
            "assignmentId = 201",
            "title = \"Plot Gantt Chart & Write Report\"",
            "isCompleted = false",
            "orderIndex = 3",
            "completedBy = null"
        ],
        palette=PALETTE_BLUE
    )

    # Category object on far right top
    cat1 = draw_object_box(
        draw, 1240, 150, 310, "category1 : Category",
        attributes=[
            "categoryId = 1",
            "name = \"COURSEWORK\"",
            "description = \"Core CS Lab Work\"",
            "colorCode = \"#3B82F6\"",
            "isActive = true"
        ],
        palette=PALETTE_TEAL
    )

    # 4. Peer Collaborator: collabUser1 : Student (Middle Left)
    c_user = draw_object_box(
        draw, 40, 480, 240, "collabUser1 : Student",
        attributes=[
            "userId = 102",
            "username = \"rahul_k\"",
            "email = \"rahul.k@gmail.com\"",
            "academicTerm = \"Fall 2026\"",
            "totalAssignments = 6",
            "isActive = true"
        ],
        palette=PALETTE_GREEN
    )

    # 5. collab1 : Collaboration (Middle Center)
    collab1 = draw_object_box(
        draw, 400, 480, 290, "collab1 : Collaboration",
        attributes=[
            "collabId = 401",
            "assignmentId = 201",
            "senderId = 101",
            "receiverId = 102",
            "status = \"ACCEPTED\"",
            "invitedAt = 2026-10-20 14:30",
            "respondedAt = 2026-10-20 15:10"
        ],
        palette=PALETTE_YELLOW
    )

    # 6. PrioritySpotlight: spotlight1 (Far Right Middle)
    spot1 = draw_object_box(
        draw, 1240, 460, 310, "spotlight1 : PrioritySpotlight",
        attributes=[
            "spotlightTaskId = 201",
            "taskTitle = \"OS Lab 3\"",
            "priorityScore = 4993",
            "urgencyLevel = \"CRITICAL\"",
            "daysRemaining = 7",
            "computedRank = 1"
        ],
        palette=PALETTE_ORANGE
    )

    # 7. CalendarSchedule: calendarDay1 (Bottom Center)
    cal1 = draw_object_box(
        draw, 400, 780, 290, "calendarDay1 : CalendarSchedule",
        attributes=[
            "scheduleId = 501",
            "date = 2026-10-28",
            "totalTasksDue = 1",
            "workloadIntensity = 5",
            "topTaskTitle = \"OS Lab 3\"",
            "month = \"October 2026\""
        ],
        palette=PALETTE_TEAL
    )

    # 8. Notification: notif1 (Bottom Right)
    notif1 = draw_object_box(
        draw, 810, 780, 310, "notification1 : Notification",
        attributes=[
            "notificationId = 601",
            "userId = 101",
            "message = \"rahul_k completed subtask #2\"",
            "type = \"SUBTASK_DONE\"",
            "isRead = false",
            "createdAt = 2026-10-21 09:45"
        ],
        palette=PALETTE_PURPLE
    )

    # 9. admin1 : Admin (Bottom Left)
    admin1 = draw_object_box(
        draw, 40, 780, 240, "admin1 : Admin",
        attributes=[
            "adminId = 901",
            "username = \"sys_admin\"",
            "securityBadge = \"SEC-ROOT-A1\"",
            "accessLevel = 3",
            "activeSessions = 14"
        ],
        palette=PALETTE_ORANGE
    )

    # --- ASSOCIATIONS & LINKS (Matching friend's diagram style) ---
    # student1 to assignment1 (maintains)
    draw.line([(s1[0] + s1[2], s1[1] + 60), (asg1[0], asg1[1] + 60)], fill=COLOR_BORDER, width=2)
    draw.text((s1[0] + s1[2] + 8, s1[1] + 46), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((asg1[0] - 14, asg1[1] + 46), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text(((s1[0] + s1[2] + asg1[0]) // 2, s1[1] + 46), "maintains", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # assignment1 to subtasks (contains)
    # Fork line to sub1, sub2, sub3
    asg_sub_x = asg1[0] + asg1[2]
    asg_sub_y = asg1[1] + 80
    draw.line([(asg_sub_x, asg_sub_y), (750, asg_sub_y)], fill=COLOR_BORDER, width=2)
    draw.text((asg_sub_x + 8, asg_sub_y - 14), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((710, asg_sub_y - 14), "contains", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")
    # Vertical spine
    draw.line([(750, sub1[1] + 40), (750, sub3[1] + 40)], fill=COLOR_BORDER, width=2)
    # Connect to each subtask
    draw.line([(750, sub1[1] + 40), (sub1[0], sub1[1] + 40)], fill=COLOR_BORDER, width=2)
    draw.line([(750, sub2[1] + 40), (sub2[0], sub2[1] + 40)], fill=COLOR_BORDER, width=2)
    draw.line([(750, sub3[1] + 40), (sub3[0], sub3[1] + 40)], fill=COLOR_BORDER, width=2)
    draw.text((sub1[0] - 14, sub1[1] + 28), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((sub2[0] - 14, sub2[1] + 28), "2", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((sub3[0] - 14, sub3[1] + 28), "3", fill=COLOR_TEXT, font=fonts["small_bold"])

    # subtask1 refers to category1
    draw.line([(sub1[0] + sub1[2], sub1[1] + 50), (cat1[0], cat1[1] + 50)], fill=COLOR_BORDER, width=2)
    draw.text(((sub1[0] + sub1[2] + cat1[0]) // 2, sub1[1] + 36), "categorized in", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # student1 has collab1
    draw.line([(s1[0] + 120, s1[1] + s1[3]), (collab1[0], collab1[1] + 40)], fill=COLOR_BORDER, width=2)
    draw.text((s1[0] + 130, s1[1] + s1[3] + 10), "sender", fill=COLOR_TEXT, font=fonts["small_italic"])

    # collabUser1 linked to collab1
    draw.line([(c_user[0] + c_user[2], c_user[1] + 50), (collab1[0], c_user[1] + 50)], fill=COLOR_BORDER, width=2)
    draw.text((c_user[0] + c_user[2] + 8, c_user[1] + 36), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text((collab1[0] - 14, c_user[1] + 36), "1", fill=COLOR_TEXT, font=fonts["small_bold"])
    draw.text(((c_user[0] + c_user[2] + collab1[0]) // 2, c_user[1] + 36), "receiver", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # collab1 linked to assignment1 (direct vertical connection between the two boxes)
    draw.line([(collab1[0] + 145, collab1[1]), (asg1[0] + 145, asg1[1] + asg1[3])], fill=COLOR_BORDER, width=2)
    draw.text((collab1[0] + 155, (collab1[1] + asg1[1] + asg1[3]) // 2), "shares", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="lm")

    # assignment1 linked to calendarDay1 (dogleg around left side of collab1)
    draw.line([(asg1[0], asg1[1] + 120), (340, asg1[1] + 120)], fill=COLOR_BORDER, width=2)
    draw.line([(340, asg1[1] + 120), (340, cal1[1] + 40)], fill=COLOR_BORDER, width=2)
    draw.line([(340, cal1[1] + 40), (cal1[0], cal1[1] + 40)], fill=COLOR_BORDER, width=2)
    draw.text((345, (asg1[1] + 120 + cal1[1] + 40) // 2), "schedules", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="lm")

    # assignment1 linked to spotlight1 (clean top overhead route over subtasks)
    draw.line([(asg1[0] + 240, asg1[1]), (asg1[0] + 240, 115)], fill=COLOR_BORDER, width=2)
    draw.line([(asg1[0] + 240, 115), (spot1[0] + 150, 115)], fill=COLOR_BORDER, width=2)
    draw.line([(spot1[0] + 150, 115), (spot1[0] + 150, spot1[1])], fill=COLOR_BORDER, width=2)
    draw.text(((asg1[0] + 240 + spot1[0] + 150) // 2, 102), "spotlighted by", fill=COLOR_TEXT, font=fonts["small_italic"], anchor="mm")

    # student1 receives notification1 (clean bottom route)
    p_notif1 = (s1[0] + 160, s1[1] + s1[3])
    p_notif2 = (s1[0] + 160, 740)
    p_notif3 = (notif1[0], 740)
    p_notif4 = (notif1[0], notif1[1] + 40)
    draw.line([p_notif1, p_notif2], fill=COLOR_BORDER, width=2)
    draw.line([p_notif2, p_notif3], fill=COLOR_BORDER, width=2)
    draw.line([p_notif3, p_notif4], fill=COLOR_BORDER, width=2)
    draw.text((p_notif2[0] + 40, p_notif2[1] - 12), "receives alert", fill=COLOR_TEXT, font=fonts["small_italic"])

    # Save
    out_dir = r"c:\Users\HOME\Downloads\Assignment-Tracker-main\Assignment-Tracker-main\uml_diagrams"
    out_file = os.path.join(out_dir, "3_object_diagram.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Diagram 3 saved at: {out_file}")

if __name__ == "__main__":
    generate_diagram_3()
