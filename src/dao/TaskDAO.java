package dao;

import model.Task;
import util.DBConnection;

import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

public class TaskDAO {
    private static final String INSERT_TASK_SQL =
            "INSERT INTO TASK (title, description, importance, due_date, completed, creator_id, created_at) " +
                    "VALUES (?, ?, ?, ?, ?, ?, ?)";
    private static final String FIND_BY_ID_SQL =
            "SELECT task_id, title, description, importance, due_date, completed, creator_id, created_at " +
                    "FROM TASK WHERE task_id = ?";
    private static final String FIND_BY_CREATOR_SQL =
            "SELECT task_id, title, description, importance, due_date, completed, creator_id, created_at " +
                    "FROM TASK WHERE creator_id = ? ORDER BY due_date, created_at";
    private static final String FIND_SHARED_SQL =
            "SELECT DISTINCT t.task_id, t.title, t.description, t.importance, t.due_date, t.completed, " +
                    "t.creator_id, t.created_at FROM TASK t INNER JOIN TASK_COLLABORATOR tc " +
                    "ON t.task_id = tc.task_id WHERE tc.user_id = ? ORDER BY t.due_date, t.created_at";
    private static final String UPDATE_COMPLETION_SQL =
            "UPDATE TASK SET completed = ? WHERE task_id = ?";
    private static final String DELETE_TASK_SQL =
            "DELETE FROM TASK WHERE task_id = ?";

    public boolean createTask(Task task) {
        if (task == null) {
            return false;
        }

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(INSERT_TASK_SQL, Statement.RETURN_GENERATED_KEYS)) {
            statement.setString(1, task.getTitle());
            statement.setString(2, task.getDescription());
            statement.setInt(3, task.getImportance());
            statement.setDate(4, task.getDueDate());
            statement.setBoolean(5, task.isCompleted());
            statement.setInt(6, task.getCreatorId());
            statement.setTimestamp(7, task.getCreatedAt());

            int affectedRows = statement.executeUpdate();
            if (affectedRows != 1) {
                return false;
            }

            try (ResultSet generatedKeys = statement.getGeneratedKeys()) {
                if (generatedKeys.next()) {
                    task.setTaskId(generatedKeys.getInt(1));
                    return true;
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to create task: " + exception.getMessage());
        }

        return false;
    }

    public Task getTaskById(int taskId) {
        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_BY_ID_SQL)) {
            statement.setInt(1, taskId);

            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return mapTask(resultSet);
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to find task by ID: " + exception.getMessage());
        }

        return null;
    }

    public List<Task> getTasksCreatedByUser(int creatorId) {
        List<Task> tasks = new ArrayList<>();

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_BY_CREATOR_SQL)) {
            statement.setInt(1, creatorId);

            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
                    tasks.add(mapTask(resultSet));
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to find tasks created by user: " + exception.getMessage());
        }

        return tasks;
    }

    public List<Task> getTasksSharedWithUser(int userId) {
        List<Task> tasks = new ArrayList<>();

        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(FIND_SHARED_SQL)) {
            statement.setInt(1, userId);

            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
                    tasks.add(mapTask(resultSet));
                }
            }
        } catch (SQLException exception) {
            System.err.println("Failed to find tasks shared with user: " + exception.getMessage());
        }

        return tasks;
    }

    public boolean updateTaskCompletion(int taskId, boolean completed) {
        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(UPDATE_COMPLETION_SQL)) {
            statement.setBoolean(1, completed);
            statement.setInt(2, taskId);
            return statement.executeUpdate() == 1;
        } catch (SQLException exception) {
            System.err.println("Failed to update task completion: " + exception.getMessage());
            return false;
        }
    }

    public boolean deleteTask(int taskId) {
        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(DELETE_TASK_SQL)) {
            statement.setInt(1, taskId);
            return statement.executeUpdate() == 1;
        } catch (SQLException exception) {
            System.err.println("Failed to delete task: " + exception.getMessage());
            return false;
        }
    }

    private Task mapTask(ResultSet resultSet) throws SQLException {
        Task task = new Task();
        task.setTaskId(resultSet.getInt("task_id"));
        task.setTitle(resultSet.getString("title"));
        task.setDescription(resultSet.getString("description"));
        task.setImportance(resultSet.getInt("importance"));
        task.setDueDate(resultSet.getDate("due_date"));
        task.setCompleted(resultSet.getBoolean("completed"));
        task.setCreatorId(resultSet.getInt("creator_id"));
        task.setCreatedAt(resultSet.getTimestamp("created_at"));
        return task;
    }
}
