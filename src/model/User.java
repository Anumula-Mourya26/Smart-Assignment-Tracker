package model;

import java.sql.Timestamp;

public class User {
    private int userId;
    private String username;
    private String gmail;
    private String password;
    private Timestamp createdAt;

    public User() {
    }

    public User(int userId, String gmail, String password, Timestamp createdAt) {
        this(userId, null, gmail, password, createdAt);
    }

    public User(int userId, String username, String gmail, String password, Timestamp createdAt) {
        this.userId = userId;
        this.username = username;
        this.gmail = gmail;
        this.password = password;
        this.createdAt = createdAt;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getGmail() {
        return gmail;
    }

    public void setGmail(String gmail) {
        this.gmail = gmail;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Timestamp getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Timestamp createdAt) {
        this.createdAt = createdAt;
    }

    @Override
    public String toString() {
        return "User{" +
                "userId=" + userId +
                ", username='" + username + '\'' +
                ", gmail='" + gmail + '\'' +
                ", password='[PROTECTED]'" +
                ", createdAt=" + createdAt +
                '}';
    }
}
