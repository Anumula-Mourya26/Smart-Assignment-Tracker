package dao;

import model.Subtask;
import util.DBConnection;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

public class SubtaskDAO {
    private static final String FIND_BY_TASK_SQL =
            "SELECT subtask_id, task_id, title, completed, created_at FROM SUBTASK WHERE task_id = ? ORDER BY subtask_id ASC";
    private static final String INSERT_SUBTASK_SQL =
            "INSERT INTO SUBTASK (task_id, title, completed, created_at) VALUES (?, ?, ?, ?)";
    private static final String UPDATE_COMPLETION_SQL =
            "UPDATE SUBTASK SET completed = ? WHERE subtask_id = ?";
    private static final String DELETE_SUBTASK_SQL =
            "DELETE FROM SUBTASK WHERE subtask_id = ?";
    private static final String COUNT_PROGRESS_SQL =
            "SELECT COUNT(*) AS total, SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) AS completed FROM SUBTASK WHERE task_id = ?";

    public List<Subtask> getSubtasksByTaskId(int taskId) {
        List<Subtask> list = new ArrayList<>();
        if (taskId <= 0) {
            return list;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_BY_TASK_SQL)) {
            statement.setInt(1, taskId);
            try (ResultSet rs = statement.executeQuery()) {
                while (rs.next()) {
                    list.add(new Subtask(
                            rs.getInt("subtask_id"),
                            rs.getInt("task_id"),
                            rs.getString("title"),
                            rs.getBoolean("completed"),
                            rs.getTimestamp("created_at")
                    ));
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to get subtasks: " + exception.getMessage());
        }
        return list;
    }

    public Subtask createSubtask(int taskId, String title) {
        if (taskId <= 0 || title == null || title.trim().isEmpty()) {
            return null;
        }

        Timestamp now = new Timestamp(System.currentTimeMillis());
        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(INSERT_SUBTASK_SQL, Statement.RETURN_GENERATED_KEYS)) {
            statement.setInt(1, taskId);
            statement.setString(2, title.trim());
            statement.setBoolean(3, false);
            statement.setTimestamp(4, now);

            int affected = statement.executeUpdate();
            if (affected == 1) {
                try (ResultSet keys = statement.getGeneratedKeys()) {
                    if (keys.next()) {
                        return new Subtask(keys.getInt(1), taskId, title.trim(), false, now);
                    }
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to create subtask: " + exception.getMessage());
        }
        return null;
    }

    public boolean updateSubtaskCompletion(int subtaskId, boolean completed) {
        if (subtaskId <= 0) {
            return false;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(UPDATE_COMPLETION_SQL)) {
            statement.setBoolean(1, completed);
            statement.setInt(2, subtaskId);
            return statement.executeUpdate() == 1;
        } catch (SQLException exception) {
            System.err.println("Failed to update subtask completion: " + exception.getMessage());
            return false;
        }
    }

    public boolean deleteSubtask(int subtaskId) {
        if (subtaskId <= 0) {
            return false;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(DELETE_SUBTASK_SQL)) {
            statement.setInt(1, subtaskId);
            return statement.executeUpdate() == 1;
        } catch (SQLException exception) {
            System.err.println("Failed to delete subtask: " + exception.getMessage());
            return false;
        }
    }

    public int[] getSubtaskProgress(int taskId) {
        if (taskId <= 0) {
            return new int[]{0, 0};
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(COUNT_PROGRESS_SQL)) {
            statement.setInt(1, taskId);
            try (ResultSet rs = statement.executeQuery()) {
                if (rs.next()) {
                    int total = rs.getInt("total");
                    int completed = rs.getInt("completed");
                    return new int[]{total, completed};
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to count subtasks: " + exception.getMessage());
        }
        return new int[]{0, 0};
    }
}
