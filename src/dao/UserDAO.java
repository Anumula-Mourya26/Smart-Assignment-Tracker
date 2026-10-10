package dao;

import model.User;
import util.DBConnection;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class UserDAO {
    private static final String INSERT_USER_SQL =
            "INSERT INTO `USER` (username, gmail, password, created_at) VALUES (?, ?, ?, ?)";
    private static final String FIND_BY_GMAIL_SQL =
            "SELECT user_id, username, gmail, password, created_at FROM `USER` WHERE gmail = ?";
    private static final String FIND_BY_ID_SQL =
            "SELECT user_id, username, gmail, password, created_at FROM `USER` WHERE user_id = ?";
    private static final String FIND_BY_USERNAME_SQL =
            "SELECT user_id, username, gmail, password, created_at FROM `USER` WHERE username = ?";

    public boolean registerUser(User user) {
        if (user == null || user.getGmail() == null || user.getPassword() == null) {
            return false;
        }

        String username = user.getUsername();
        if (username == null || username.trim().isEmpty()) {
            String g = user.getGmail();
            int atIdx = g.indexOf('@');
            username = atIdx > 0 ? g.substring(0, atIdx) : g;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(INSERT_USER_SQL)) {
            statement.setString(1, username.trim());
            statement.setString(2, user.getGmail());
            statement.setString(3, user.getPassword());
            statement.setTimestamp(4, user.getCreatedAt());

            return statement.executeUpdate() == 1;
        } catch (SQLException exception) {
            System.err.println("Failed to register user: " + exception.getMessage());
            return false;
        }
    }

    public User findByGmail(String gmail) {
        if (gmail == null || gmail.trim().isEmpty()) {
            return null;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_BY_GMAIL_SQL)) {
            statement.setString(1, gmail.trim());

            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return mapUser(resultSet);
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to find user by Gmail: " + exception.getMessage());
        }

        return null;
    }

    public User findByUsername(String username) {
        if (username == null || username.trim().isEmpty()) {
            return null;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_BY_USERNAME_SQL)) {
            statement.setString(1, username.trim());

            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return mapUser(resultSet);
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to find user by username: " + exception.getMessage());
        }

        return null;
    }

    public boolean gmailExists(String gmail) {
        if (gmail == null || gmail.trim().isEmpty()) {
            return false;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_BY_GMAIL_SQL)) {
            statement.setString(1, gmail.trim());

            try (ResultSet resultSet = statement.executeQuery()) {
                return resultSet.next();
            }
        } catch (SQLException exception) {
            System.err.println("Failed to check Gmail: " + exception.getMessage());
            return false;
        }
    }

    public User findByUserId(int userId) {
        if (userId <= 0) {
            return null;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_BY_ID_SQL)) {
            statement.setInt(1, userId);

            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return mapUser(resultSet);
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to find user by ID: " + exception.getMessage());
        }

        return null;
    }

    private User mapUser(ResultSet rs) throws SQLException {
        User user = new User();
        user.setUserId(rs.getInt("user_id"));
        user.setUsername(rs.getString("username"));
        user.setGmail(rs.getString("gmail"));
        user.setPassword(rs.getString("password"));
        user.setCreatedAt(rs.getTimestamp("created_at"));
        return user;
    }
}
