package test;

import dao.TaskDAO;
import dao.UserDAO;
import model.Task;
import model.User;
import service.TaskService;

import java.sql.Timestamp;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

public class TaskServiceTest {
    private static final String TEST_GMAIL = "test.task.dao@gmail.com";

    public static void main(String[] args) {
        UserDAO userDAO = new UserDAO();
        TaskDAO taskDAO = new TaskDAO();
        TaskService service = new TaskService(taskDAO);
        User testUser = userDAO.findByGmail(TEST_GMAIL);
        if (testUser == null) {
            throw new IllegalStateException("Test user does not exist: " + TEST_GMAIL);
        }

        Task invalidImportance = new Task();
        invalidImportance.setTitle("Invalid importance");
        invalidImportance.setImportance(0);
        invalidImportance.setCreatorId(testUser.getUserId());
        invalidImportance.setCreatedAt(new Timestamp(System.currentTimeMillis()));
        System.out.println("Invalid importance: " + service.createTask(invalidImportance));

        Task task = new Task();
        task.setTitle("Service test task");
        task.setDescription("TaskService verification");
        task.setImportance(3);
        task.setDueDate(java.sql.Date.valueOf(LocalDate.now().plusDays(2)));
        task.setCompleted(false);
        task.setCreatorId(testUser.getUserId());
        task.setCreatedAt(new Timestamp(System.currentTimeMillis()));
        if (!service.createTask(task)) {
            throw new IllegalStateException("Could not create service test task.");
        }

        Task retrieved = service.getTask(task.getTaskId());
        if (retrieved == null || !retrieved.getTitle().equals(task.getTitle())) {
            throw new IllegalStateException("Created task was not retrieved.");
        }
        System.out.println("Created and retrieved task: " + retrieved.getTaskId());

        List<Task> userTasks = service.getUserTasks(testUser.getUserId());
        if (userTasks.stream().noneMatch(item -> item.getTaskId() == task.getTaskId())) {
            throw new IllegalStateException("Created task is missing from user tasks.");
        }
        System.out.println("User task count: " + userTasks.size());

        if (!service.markTaskCompleted(task.getTaskId(), true)) {
            throw new IllegalStateException("Could not mark task completed.");
        }
        Task completed = service.getTask(task.getTaskId());
        if (completed == null || !completed.isCompleted()) {
            throw new IllegalStateException("Task completion was not updated.");
        }
        System.out.println("Completion update: " + completed.isCompleted());

        Task higherTask = createTask(service, testUser.getUserId(), "Higher priority", 5, LocalDate.now().plusDays(1));
        Task equalDateTask = createTask(service, testUser.getUserId(), "Equal date priority", 5, LocalDate.now().plusDays(1));
        Task lowerTask = createTask(service, testUser.getUserId(), "Lower priority", 3, LocalDate.now().plusDays(3));
        Task noDueDateTask = createTask(service, testUser.getUserId(), "No due date", 5, null);

        Task highest = service.getHighestPriorityTask(testUser.getUserId());
        if (highest == null || highest.getTaskId() != higherTask.getTaskId()) {
            throw new IllegalStateException("Highest priority task selection failed.");
        }
        System.out.println("Highest priority task: " + highest.getTaskId());

        Map<LocalDate, Integer> calendar = service.getCalendarImportance(testUser.getUserId());
        if (calendar.isEmpty()) {
            throw new IllegalStateException("Calendar importance returned no entries.");
        }
        System.out.println("Calendar entries: " + calendar.size());

        service.deleteCreatedTask(task.getTaskId());
        service.deleteCreatedTask(higherTask.getTaskId());
        service.deleteCreatedTask(equalDateTask.getTaskId());
        service.deleteCreatedTask(lowerTask.getTaskId());
        service.deleteCreatedTask(noDueDateTask.getTaskId());
        System.out.println("Temporary test tasks removed.");
    }

    private static Task createTask(TaskService service, int userId, String title, int importance, LocalDate dueDate) {
        Task task = new Task();
        task.setTitle(title);
        task.setDescription("Temporary task for priority and calendar testing.");
        task.setImportance(importance);
        task.setDueDate(dueDate == null ? null : java.sql.Date.valueOf(dueDate));
        task.setCompleted(false);
        task.setCreatorId(userId);
        task.setCreatedAt(new Timestamp(System.currentTimeMillis()));

        if (!service.createTask(task)) {
            throw new IllegalStateException("Could not create temporary test task: " + title);
        }
        return task;
    }
}
