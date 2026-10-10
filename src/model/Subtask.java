package model;

import java.sql.Timestamp;

public class Subtask {
    private int subtaskId;
    private int taskId;
    private String title;
    private boolean completed;
    private Timestamp createdAt;

    public Subtask() {
    }

    public Subtask(int subtaskId, int taskId, String title, boolean completed, Timestamp createdAt) {
        this.subtaskId = subtaskId;
        this.taskId = taskId;
        this.title = title;
        this.completed = completed;
        this.createdAt = createdAt;
    }

    public int getSubtaskId() {
        return subtaskId;
    }

    public void setSubtaskId(int subtaskId) {
        this.subtaskId = subtaskId;
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

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }

    public Timestamp getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Timestamp createdAt) {
        this.createdAt = createdAt;
    }
}
