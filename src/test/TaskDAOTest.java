package test;

import dao.TaskDAO;
import dao.UserDAO;
import model.Task;
import model.User;
import util.DBConnection;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.List;

public class TaskDAOTest {
    private static final String TEST_GMAIL = "test.task.dao@gmail.com";
    private static final String TEST_PASSWORD = "TaskTestPassword123!";

    public static void main(String[] args) {
        TaskDAO taskDAO = new TaskDAO();
        UserDAO userDAO = new UserDAO();

        User testUser = userDAO.findByGmail(TEST_GMAIL);
        if (testUser == null) {
            testUser = new User();
            testUser.setGmail(TEST_GMAIL);
            testUser.setPassword("temporary-password");
            testUser.setCreatedAt(new Timestamp(System.currentTimeMillis()));
            if (!userDAO.registerUser(testUser)) {
                throw new IllegalStateException("Unable to create the test user.");
            }
            testUser = userDAO.findByGmail(TEST_GMAIL);
        }

        Task task = new Task();
        task.setTitle("Task DAO Test - " + System.currentTimeMillis());
        task.setDescription("Test task created by TaskDAOTest.");
        task.setImportance(3);
        task.setDueDate(null);
        task.setCompleted(false);
        task.setCreatorId(testUser.getUserId());
        task.setCreatedAt(new Timestamp(System.currentTimeMillis()));

        if (!taskDAO.createTask(task)) {
            throw new IllegalStateException("Unable to create the test task.");
        }
        System.out.println("Created task ID: " + task.getTaskId());

        Task savedTask = taskDAO.getTaskById(task.getTaskId());
        if (savedTask == null || !savedTask.getTitle().equals(task.getTitle())) {
            throw new IllegalStateException("Task was not retrieved by ID.");
        }
        System.out.println("Retrieved task by ID: " + savedTask.getTitle());

        List<Task> userTasks = taskDAO.getTasksCreatedByUser(testUser.getUserId());
        if (userTasks.stream().noneMatch(item -> item.getTaskId() == task.getTaskId())) {
            throw new IllegalStateException("Created task was not found for the user.");
        }
        System.out.println("Retrieved " + userTasks.size() + " tasks created by the user.");

        if (!taskDAO.updateTaskCompletion(task.getTaskId(), true)) {
            throw new IllegalStateException("Completion update failed.");
        }
        Task updatedTask = taskDAO.getTaskById(task.getTaskId());
        if (updatedTask == null || !updatedTask.isCompleted()) {
            throw new IllegalStateException("Task completion was not updated.");
        }
        System.out.println("Updated task completion: " + updatedTask.isCompleted());

        addTaskCollaborator(task.getTaskId(), testUser.getUserId());
        List<Task> sharedTasks = taskDAO.getTasksSharedWithUser(testUser.getUserId());
        if (sharedTasks.stream().noneMatch(item -> item.getTaskId() == task.getTaskId())) {
            throw new IllegalStateException("Shared task was not found.");
        }
        System.out.println("Retrieved shared tasks: " + sharedTasks.size());

        if (!taskDAO.deleteTask(task.getTaskId())) {
            throw new IllegalStateException("Task deletion failed.");
        }
        System.out.println("Deleted test task ID: " + task.getTaskId());
    }

    private static void addTaskCollaborator(int taskId, int userId) {
        String sql = "INSERT INTO TASK_COLLABORATOR (task_id, user_id) VALUES (?, ?)";
        try (Connection connection = DBConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, taskId);
            statement.setInt(2, userId);
            statement.executeUpdate();
        } catch (SQLException exception) {
            throw new IllegalStateException("Unable to add test collaborator: " + exception.getMessage(), exception);
        }
    }
}
