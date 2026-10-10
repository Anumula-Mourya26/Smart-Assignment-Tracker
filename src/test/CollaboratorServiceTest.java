package test;

import dao.CollaboratorDAO;
import dao.TaskDAO;
import dao.UserDAO;
import model.Task;
import model.User;
import service.CollaboratorService;

import java.sql.Timestamp;
import java.util.List;

public class CollaboratorServiceTest {
    private static final String TEST_GMAIL = "test.collaborator.primary@gmail.com";
    private static final String SECOND_TEST_GMAIL = "test.collaborator.secondary@gmail.com";

    public static void main(String[] args) {
        UserDAO userDAO = new UserDAO();
        TaskDAO taskDAO = new TaskDAO();
        CollaboratorDAO collaboratorDAO = new CollaboratorDAO();
        CollaboratorService collaboratorService = new CollaboratorService(taskDAO, userDAO, collaboratorDAO);

        User primaryUser = getOrCreateUser(userDAO, TEST_GMAIL);
        User secondaryUser = getOrCreateUser(userDAO, SECOND_TEST_GMAIL);

        Task task = getOrCreateTask(taskDAO, primaryUser.getUserId());
        System.out.println("Using task ID: " + task.getTaskId());

        if (!collaboratorService.addCollaborator(task.getTaskId(), secondaryUser.getUserId())) {
            throw new IllegalStateException("Could not add collaborator.");
        }
        System.out.println("Added collaborator: " + secondaryUser.getUserId());

        if (!collaboratorService.isCollaborator(task.getTaskId(), secondaryUser.getUserId())) {
            throw new IllegalStateException("Collaborator was not found.");
        }

        if (collaboratorService.addCollaborator(task.getTaskId(), secondaryUser.getUserId())) {
            throw new IllegalStateException("Duplicate collaborator was added.");
        }

        List<Integer> collaborators = collaboratorService.getCollaboratorIds(task.getTaskId());
        if (collaborators.stream().noneMatch(id -> id == secondaryUser.getUserId())) {
            throw new IllegalStateException("Collaborator ID was missing from the task.");
        }
        if (collaborators.size() != 1) {
            throw new IllegalStateException("Expected one collaborator, found " + collaborators.size());
        }
        System.out.println("Collaborators: " + collaborators);

        List<Task> sharedTasks = taskDAO.getTasksSharedWithUser(secondaryUser.getUserId());
        if (sharedTasks.stream().noneMatch(item -> item.getTaskId() == task.getTaskId())) {
            throw new IllegalStateException("Shared task was not returned.");
        }
        System.out.println("Shared task retrieved for collaborator: " + task.getTaskId());

        if (!collaboratorService.removeCollaborator(task.getTaskId(), secondaryUser.getUserId())) {
            throw new IllegalStateException("Collaborator removal failed.");
        }
        if (collaboratorService.isCollaborator(task.getTaskId(), secondaryUser.getUserId())) {
            throw new IllegalStateException("Collaborator still exists after removal.");
        }
        System.out.println("Removed collaborator: " + secondaryUser.getUserId());
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

    private static Task getOrCreateTask(TaskDAO taskDAO, int creatorId) {
        List<Task> tasks = taskDAO.getTasksCreatedByUser(creatorId);
        for (Task task : tasks) {
            if (task.getTitle().startsWith("Collaborator Service Test")) {
                return task;
            }
        }

        Task task = new Task();
        task.setTitle("Collaborator Service Test - " + System.currentTimeMillis());
        task.setDescription("Temporary task for collaborator testing.");
        task.setImportance(3);
        task.setDueDate(null);
        task.setCompleted(false);
        task.setCreatorId(creatorId);
        task.setCreatedAt(new Timestamp(System.currentTimeMillis()));
        if (!taskDAO.createTask(task)) {
            throw new IllegalStateException("Unable to create the test task.");
        }
        return task;
    }
}
