package service;

import dao.CollaboratorDAO;
import dao.TaskDAO;
import dao.UserDAO;
import model.Task;
import model.User;

import java.util.List;
import java.util.Map;
import java.util.Objects;

public class CollaboratorService {
    private final TaskDAO taskDAO;
    private final UserDAO userDAO;
    private final CollaboratorDAO collaboratorDAO;

    public CollaboratorService(TaskDAO taskDAO, UserDAO userDAO, CollaboratorDAO collaboratorDAO) {
        this.taskDAO = Objects.requireNonNull(taskDAO, "TaskDAO cannot be null.");
        this.userDAO = Objects.requireNonNull(userDAO, "UserDAO cannot be null.");
        this.collaboratorDAO = Objects.requireNonNull(collaboratorDAO, "CollaboratorDAO cannot be null.");
    }

    public boolean addCollaborator(int taskId, int userId) {
        return addCollaborator(taskId, userId, "ACCEPTED");
    }

    public boolean addCollaborator(int taskId, int userId, String status) {
        if (!isValidTaskAndUser(taskId, userId)) {
            return false;
        }
        Task task = taskDAO.getTaskById(taskId);
        if (task != null && task.getCreatorId() == userId) {
            return false;
        }
        if (collaboratorDAO.isCollaborator(taskId, userId)) {
            return false;
        }
        return collaboratorDAO.addCollaborator(taskId, userId, status);
    }

    public boolean updateCollaboratorStatus(int taskId, int userId, String status) {
        if (taskId <= 0 || userId <= 0) {
            return false;
        }
        return collaboratorDAO.updateCollaboratorStatus(taskId, userId, status);
    }

    public boolean removeCollaborator(int taskId, int userId) {
        if (taskId <= 0 || userId <= 0) {
            return false;
        }
        if (taskDAO.getTaskById(taskId) == null) {
            return false;
        }
        if (userDAO.findByUserId(userId) == null) {
            return false;
        }
        return collaboratorDAO.removeCollaborator(taskId, userId);
    }

    public List<Integer> getCollaboratorIds(int taskId) {
        if (taskId <= 0 || taskDAO.getTaskById(taskId) == null) {
            return List.of();
        }
        return collaboratorDAO.getCollaboratorIds(taskId);
    }

    public List<Map<String, Object>> getCollaboratorDetails(int taskId) {
        if (taskId <= 0 || taskDAO.getTaskById(taskId) == null) {
            return List.of();
        }
        return collaboratorDAO.getCollaboratorDetails(taskId);
    }

    public List<Map<String, Object>> getPendingRequests(int userId) {
        if (userId <= 0) {
            return List.of();
        }
        return collaboratorDAO.getPendingRequestsForUser(userId);
    }

    public boolean isCollaborator(int taskId, int userId) {
        if (taskId <= 0 || userId <= 0) {
            return false;
        }
        if (taskDAO.getTaskById(taskId) == null) {
            return false;
        }
        if (userDAO.findByUserId(userId) == null) {
            return false;
        }
        return collaboratorDAO.isCollaborator(taskId, userId);
    }

    private boolean isValidTaskAndUser(int taskId, int userId) {
        if (taskId <= 0 || userId <= 0) {
            return false;
        }
        Task task = taskDAO.getTaskById(taskId);
        User user = userDAO.findByUserId(userId);
        return task != null && user != null;
    }
}
