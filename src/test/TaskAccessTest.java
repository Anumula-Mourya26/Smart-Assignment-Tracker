package test;

import dao.CollaboratorDAO;
import dao.TaskDAO;
import dao.UserDAO;
import model.Task;
import model.User;
import service.CollaboratorService;
import service.TaskService;

import java.sql.Timestamp;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

public class TaskAccessTest {
    private static final long RUN_ID = System.currentTimeMillis();

    public static void main(String[] args) {
        UserDAO userDAO = new UserDAO();
        TaskDAO taskDAO = new TaskDAO();
        CollaboratorService collaboratorService = new CollaboratorService(taskDAO, userDAO, new CollaboratorDAO());
        TaskService taskService = new TaskService(taskDAO, collaboratorService);

        long testTime = System.currentTimeMillis();
        User creator = getOrCreateUser(userDAO, "test.access.creator." + RUN_ID + "@gmail.com");
        User collaborator = getOrCreateUser(userDAO, "test.access.collaborator." + RUN_ID + "@gmail.com");
        User otherUser = getOrCreateUser(userDAO, "test.access.other." + RUN_ID + "@gmail.com");

        Task task = new Task();
        task.setTitle("Task Access Test - " + RUN_ID);
        task.setDescription("Shared task for access integration testing.");
        task.setImportance(3);
        LocalDate taskDueDate = LocalDate.now().plusDays(2);
        task.setDueDate(java.sql.Date.valueOf(taskDueDate));
        task.setCompleted(false);
        task.setCreatorId(creator.getUserId());
        task.setCreatedAt(new Timestamp(testTime));
        if (!taskDAO.createTask(task)) {
            throw new IllegalStateException("Unable to create the test task.");
        }

        if (!collaboratorService.addCollaborator(task.getTaskId(), collaborator.getUserId())) {
            throw new IllegalStateException("Could not add collaborator.");
        }
        System.out.println("Created task ID: " + task.getTaskId());

        if (!taskService.canAccessTask(creator.getUserId(), task.getTaskId())) {
            throw new IllegalStateException("Task creator cannot access the task.");
        }
        if (!taskService.canAccessTask(collaborator.getUserId(), task.getTaskId())) {
            throw new IllegalStateException("Collaborator cannot access the task.");
        }
        if (taskService.canAccessTask(otherUser.getUserId(), task.getTaskId())) {
            throw new IllegalStateException("Unrelated user unexpectedly accessed the task.");
        }

        List<Task> creatorVisible = taskService.getAllVisibleTasks(creator.getUserId());
        if (creatorVisible.stream().noneMatch(item -> item.getTaskId() == task.getTaskId())) {
            throw new IllegalStateException("Creator could not see the task.");
        }

        List<Task> collaboratorVisible = taskService.getAllVisibleTasks(collaborator.getUserId());
        if (collaboratorVisible.stream().noneMatch(item -> item.getTaskId() == task.getTaskId())) {
            throw new IllegalStateException("Collaborator could not see the shared task.");
        }

        if (creatorVisible.stream().filter(item -> item.getTaskId() == task.getTaskId()).count() != 1) {
            throw new IllegalStateException("Creator-visible task was duplicated.");
        }

        if (collaboratorService.addCollaborator(task.getTaskId(), collaborator.getUserId())) {
            throw new IllegalStateException("Duplicate collaborator was added.");
        }

        if (!collaboratorService.isCollaborator(task.getTaskId(), collaborator.getUserId())) {
            throw new IllegalStateException("Collaborator was not stored.");
        }

        List<Task> sortedTasks = taskService.getVisibleTasksSortedByDueDate(collaborator.getUserId());
        if (sortedTasks.stream().noneMatch(item -> item.getTaskId() == task.getTaskId())) {
            throw new IllegalStateException("Sorted visible tasks did not include the shared task.");
        }

        Map<LocalDate, Integer> calendar = taskService.getCalendarImportance(collaborator.getUserId());
        if (!calendar.containsKey(taskDueDate)) {
            throw new IllegalStateException("Calendar did not include the shared task.");
        }
        if (calendar.get(taskDueDate) != task.getImportance()) {
            throw new IllegalStateException("Calendar importance was not calculated correctly.");
        }

        Task higherPriorityTask = createTask(taskDAO, creator.getUserId(), "Higher priority shared task " + RUN_ID,
                5, LocalDate.now().plusDays(1));
        if (!collaboratorService.addCollaborator(higherPriorityTask.getTaskId(), collaborator.getUserId())) {
            throw new IllegalStateException("Could not add collaborator to higher priority task.");
        }
        Task highestPriorityTask = taskService.getHighestPriorityTask(collaborator.getUserId());
        System.out.println("Priority candidates: " + task.getTaskId() + "(importance=" + task.getImportance() + ") and "
                + higherPriorityTask.getTaskId() + "(importance=" + higherPriorityTask.getImportance() + ")");
        if (highestPriorityTask == null || highestPriorityTask.getTaskId() != higherPriorityTask.getTaskId()) {
            throw new IllegalStateException("Shared task priority selection failed.");
        }

        if (!cleanupTask(taskDAO, task.getTaskId())) {
            throw new IllegalStateException("Test task deletion failed.");
        }
        if (!cleanupTask(taskDAO, higherPriorityTask.getTaskId())) {
            throw new IllegalStateException("Higher-priority test task deletion failed.");
        }
        System.out.println("Task access integration passed.");
    }

    private static boolean cleanupTask(TaskDAO taskDAO, int taskId) {
        return taskDAO.deleteTask(taskId);
    }

    private static User getOrCreateUser(UserDAO userDAO, String gmail) {
        User user = userDAO.findByGmail(gmail);
        if (user != null) {
            return user;
        }
        User newUser = new User();
        newUser.setGmail(gmail);
        newUser.setPassword("temporary-password");
        newUser.setCreatedAt(new Timestamp(System.currentTimeMillis()));
        if (!userDAO.registerUser(newUser)) {
            throw new IllegalStateException("Unable to create test user: " + gmail);
        }
        return userDAO.findByGmail(gmail);
    }

    private static Task createTask(TaskDAO taskDAO, int creatorId, String title, int importance, LocalDate dueDate) {
        Task task = new Task();
        task.setTitle(title);
        task.setDescription("Temporary task for priority comparison.");
        task.setImportance(importance);
        task.setDueDate(java.sql.Date.valueOf(dueDate));
        task.setCompleted(false);
        task.setCreatorId(creatorId);
        task.setCreatedAt(new Timestamp(System.currentTimeMillis()));
        if (!taskDAO.createTask(task)) {
            throw new IllegalStateException("Unable to create priority task: " + title);
        }
        return task;
    }
}
