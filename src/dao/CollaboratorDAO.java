package dao;

import util.DBConnection;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CollaboratorDAO {
    private static final String INSERT_COLLABORATOR_SQL =
            "INSERT INTO TASK_COLLABORATOR (task_id, user_id, status, created_at, accepted_at) VALUES (?, ?, ?, ?, ?)";
    private static final String DELETE_COLLABORATOR_SQL =
            "DELETE FROM TASK_COLLABORATOR WHERE task_id = ? AND user_id = ?";
    private static final String UPDATE_STATUS_SQL =
            "UPDATE TASK_COLLABORATOR SET status = ?, accepted_at = ? WHERE task_id = ? AND user_id = ?";
    private static final String FIND_COLLABORATORS_SQL =
            "SELECT user_id FROM TASK_COLLABORATOR WHERE task_id = ? ORDER BY user_id";
    private static final String CHECK_COLLABORATOR_SQL =
            "SELECT 1 FROM TASK_COLLABORATOR WHERE task_id = ? AND user_id = ?";
    private static final String FIND_COLLABORATOR_DETAILS_SQL =
            "SELECT tc.user_id, u.gmail, u.username, tc.status, tc.created_at, tc.accepted_at " +
            "FROM TASK_COLLABORATOR tc " +
            "JOIN `USER` u ON tc.user_id = u.user_id " +
            "WHERE tc.task_id = ? " +
            "ORDER BY tc.accepted_at ASC, tc.created_at ASC";
    private static final String FIND_PENDING_REQUESTS_SQL =
            "SELECT tc.task_id, t.title, t.description, t.importance, t.due_date, t.creator_id, u.gmail AS creator_gmail, u.username AS creator_username, tc.created_at " +
            "FROM TASK_COLLABORATOR tc " +
            "JOIN TASK t ON tc.task_id = t.task_id " +
            "JOIN `USER` u ON t.creator_id = u.user_id " +
            "WHERE tc.user_id = ? AND tc.status = 'PENDING' " +
            "ORDER BY tc.created_at DESC";

    public boolean addCollaborator(int taskId, int userId) {
        return addCollaborator(taskId, userId, "ACCEPTED");
    }

    public boolean addCollaborator(int taskId, int userId, String status) {
        if (taskId <= 0 || userId <= 0) {
            return false;
        }

        String actualStatus = (status == null || status.isBlank()) ? "ACCEPTED" : status.toUpperCase();
        Timestamp now = new Timestamp(System.currentTimeMillis());
        Timestamp acceptedAt = "ACCEPTED".equals(actualStatus) ? now : null;

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(INSERT_COLLABORATOR_SQL)) {
            statement.setInt(1, taskId);
            statement.setInt(2, userId);
            statement.setString(3, actualStatus);
            statement.setTimestamp(4, now);
            statement.setTimestamp(5, acceptedAt);
            return statement.executeUpdate() == 1;
        } catch (SQLException exception) {
            System.err.println("Failed to add collaborator: " + exception.getMessage());
            return false;
        }
    }

    public boolean updateCollaboratorStatus(int taskId, int userId, String status) {
        if (taskId <= 0 || userId <= 0 || status == null) {
            return false;
        }

        String actualStatus = status.toUpperCase();
        Timestamp acceptedAt = "ACCEPTED".equals(actualStatus) ? new Timestamp(System.currentTimeMillis()) : null;

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(UPDATE_STATUS_SQL)) {
            statement.setString(1, actualStatus);
            statement.setTimestamp(2, acceptedAt);
            statement.setInt(3, taskId);
            statement.setInt(4, userId);
            return statement.executeUpdate() == 1;
        } catch (SQLException exception) {
            System.err.println("Failed to update collaborator status: " + exception.getMessage());
            return false;
        }
    }

    public boolean removeCollaborator(int taskId, int userId) {
        if (taskId <= 0 || userId <= 0) {
            return false;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(DELETE_COLLABORATOR_SQL)) {
            statement.setInt(1, taskId);
            statement.setInt(2, userId);
            return statement.executeUpdate() == 1;
        } catch (SQLException exception) {
            System.err.println("Failed to remove collaborator: " + exception.getMessage());
            return false;
        }
    }

    public List<Integer> getCollaboratorIds(int taskId) {
        List<Integer> collaboratorIds = new ArrayList<>();
        if (taskId <= 0) {
            return collaboratorIds;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_COLLABORATORS_SQL)) {
            statement.setInt(1, taskId);

            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
                    collaboratorIds.add(resultSet.getInt("user_id"));
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to find collaborators: " + exception.getMessage());
        }

        return collaboratorIds;
    }

    public List<Map<String, Object>> getCollaboratorDetails(int taskId) {
        List<Map<String, Object>> details = new ArrayList<>();
        if (taskId <= 0) {
            return details;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_COLLABORATOR_DETAILS_SQL)) {
            statement.setInt(1, taskId);

            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
                    Map<String, Object> map = new HashMap<>();
                    map.put("user_id", resultSet.getInt("user_id"));
                    map.put("gmail", resultSet.getString("gmail"));
                    map.put("username", resultSet.getString("username"));
                    map.put("status", resultSet.getString("status"));
                    map.put("created_at", resultSet.getTimestamp("created_at"));
                    map.put("accepted_at", resultSet.getTimestamp("accepted_at"));
                    details.add(map);
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to find collaborator details: " + exception.getMessage());
        }

        return details;
    }

    public List<Map<String, Object>> getPendingRequestsForUser(int userId) {
        List<Map<String, Object>> requests = new ArrayList<>();
        if (userId <= 0) {
            return requests;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_PENDING_REQUESTS_SQL)) {
            statement.setInt(1, userId);

            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
                    Map<String, Object> map = new HashMap<>();
                    map.put("task_id", resultSet.getInt("task_id"));
                    map.put("title", resultSet.getString("title"));
                    map.put("description", resultSet.getString("description"));
                    map.put("importance", resultSet.getInt("importance"));
                    map.put("due_date", resultSet.getDate("due_date"));
                    map.put("creator_id", resultSet.getInt("creator_id"));
                    map.put("creator_gmail", resultSet.getString("creator_gmail"));
                    map.put("creator_username", resultSet.getString("creator_username"));
                    map.put("created_at", resultSet.getTimestamp("created_at"));
                    requests.add(map);
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to find pending requests: " + exception.getMessage());
        }

        return requests;
    }

    public boolean isCollaborator(int taskId, int userId) {
        if (taskId <= 0 || userId <= 0) {
            return false;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(CHECK_COLLABORATOR_SQL)) {
            statement.setInt(1, taskId);
            statement.setInt(2, userId);

            try (ResultSet resultSet = statement.executeQuery()) {
                return resultSet.next();
            }
        } catch (SQLException exception) {
            System.err.println("Failed to check collaborator: " + exception.getMessage());
            return false;
        }
    }
}
