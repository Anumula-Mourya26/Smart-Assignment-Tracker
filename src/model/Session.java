package model;

public class Session {
    private final int userId;
    private final String gmail;

    public Session(int userId, String gmail) {
        this.userId = userId;
        this.gmail = gmail;
    }

    public int getUserId() {
        return userId;
    }

    public String getGmail() {
        return gmail;
    }

    @Override
    public String toString() {
        return "Session{" +
                "userId=" + userId +
                ", gmail='" + gmail + '\'' +
                '}';
    }
}
