package model;

import java.sql.Date;
import java.sql.Timestamp;

public class Task {
    private int taskId;
    private String title;
    private String description;
    private int importance;
    private Date dueDate;
    private boolean completed;
    private int creatorId;
    private Timestamp createdAt;

    public Task() {
    }

    public Task(int taskId, String title, String description, int importance,
                Date dueDate, boolean completed, int creatorId, Timestamp createdAt) {
        this.taskId = taskId;
        this.title = title;
        this.description = description;
        this.importance = importance;
        this.dueDate = dueDate;
        this.completed = completed;
        this.creatorId = creatorId;
        this.createdAt = createdAt;
    }

    public int getTaskId() {
        return taskId;
    }

    public void setTaskId(int taskId) {
        this.taskId = taskId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public int getImportance() {
        return importance;
    }

    public void setImportance(int importance) {
        this.importance = importance;
    }

    public Date getDueDate() {
        return dueDate;
    }

    public void setDueDate(Date dueDate) {
        this.dueDate = dueDate;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }

    public int getCreatorId() {
        return creatorId;
    }

    public void setCreatorId(int creatorId) {
        this.creatorId = creatorId;
    }

    public Timestamp getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Timestamp createdAt) {
        this.createdAt = createdAt;
    }

    @Override
    public String toString() {
        return "Task{" +
                "taskId=" + taskId +
                ", title='" + title + '\'' +
                ", description='" + description + '\'' +
                ", importance=" + importance +
                ", dueDate=" + dueDate +
                ", completed=" + completed +
                ", creatorId=" + creatorId +
                ", createdAt=" + createdAt +
                '}';
    }
}
