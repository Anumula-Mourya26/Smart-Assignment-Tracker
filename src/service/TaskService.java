package service;

import dao.TaskDAO;
import model.Task;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

public class TaskService {
    private final TaskDAO taskDAO;
    private final CollaboratorService collaboratorService;

    public TaskService(TaskDAO taskDAO) {
        this(taskDAO, new CollaboratorService(taskDAO, new dao.UserDAO(), new dao.CollaboratorDAO()));
    }

    public TaskService(TaskDAO taskDAO, CollaboratorService collaboratorService) {
        this.taskDAO = Objects.requireNonNull(taskDAO, "TaskDAO cannot be null.");
        this.collaboratorService = Objects.requireNonNull(collaboratorService, "CollaboratorService cannot be null.");
    }

    public boolean createTask(Task task) {
        if (task == null || isBlank(task.getTitle()) || task.getImportance() < 1 || task.getImportance() > 5
                || task.getCreatorId() <= 0) {
            return false;
        }

        if (task.getDueDate() != null && task.getDueDate().toLocalDate().isBefore(LocalDate.now())) {
            return false;
        }

        return taskDAO.createTask(task);
    }

    public Task getTask(int taskId) {
        if (taskId <= 0) {
            return null;
        }
        return taskDAO.getTaskById(taskId);
    }

    public List<Task> getUserTasks(int userId) {
        if (userId <= 0) {
            return new ArrayList<>();
        }
        return taskDAO.getTasksCreatedByUser(userId);
    }

    public List<Task> getSharedTasks(int userId) {
        if (userId <= 0) {
            return new ArrayList<>();
        }
        return taskDAO.getTasksSharedWithUser(userId);
    }

    public boolean markTaskCompleted(int taskId, boolean completed) {
        if (taskId <= 0) {
            return false;
        }
        return taskDAO.updateTaskCompletion(taskId, completed);
    }

    public boolean deleteCreatedTask(int taskId) {
        if (taskId <= 0) {
            return false;
        }
        return taskDAO.deleteTask(taskId);
    }

    public Task getHighestPriorityTask(int userId) {
        if (userId <= 0) {
            return null;
        }

        Task highestPriorityTask = null;
        for (Task task : getAllVisibleTasks(userId)) {
            if (task.isCompleted() || task.getImportance() <= 0) {
                continue;
            }
            if (highestPriorityTask == null || isHigherPriority(task, highestPriorityTask)) {
                highestPriorityTask = task;
            }
        }
        return highestPriorityTask;
    }

    private boolean isHigherPriority(Task candidate, Task currentWinner) {
        if (candidate.getImportance() != currentWinner.getImportance()) {
            return candidate.getImportance() > currentWinner.getImportance();
        }

        boolean candidateHasDueDate = candidate.getDueDate() != null;
        boolean currentHasDueDate = currentWinner.getDueDate() != null;
        if (candidateHasDueDate != currentHasDueDate) {
            return candidateHasDueDate;
        }
        if (candidateHasDueDate && currentHasDueDate) {
            int dateComparison = candidate.getDueDate().toLocalDate()
                    .compareTo(currentWinner.getDueDate().toLocalDate());
            if (dateComparison != 0) {
                return dateComparison < 0;
            }
        }
        return candidate.getTaskId() < currentWinner.getTaskId();
    }

    public Map<LocalDate, Integer> getCalendarImportance(int userId) {
        if (userId <= 0) {
            return new HashMap<>();
        }

        Map<LocalDate, Integer> importanceByDate = new HashMap<>();
        for (Task task : getAllVisibleTasks(userId)) {
            if (task.getDueDate() == null) {
                continue;
            }
            LocalDate dueDate = task.getDueDate().toLocalDate();
            importanceByDate.merge(dueDate, task.getImportance(), Integer::sum);
        }

        return importanceByDate;
    }

    public List<Task> getAllVisibleTasks(int userId) {
        if (userId <= 0) {
            return Collections.emptyList();
        }

        List<Task> visibleTasks = new ArrayList<>();
        visibleTasks.addAll(taskDAO.getTasksCreatedByUser(userId));
        visibleTasks.addAll(taskDAO.getTasksSharedWithUser(userId));

        Set<Integer> seenTaskIds = new HashSet<>();
        List<Task> uniqueTasks = new ArrayList<>();
        for (Task task : visibleTasks) {
            if (seenTaskIds.add(task.getTaskId())) {
                uniqueTasks.add(task);
            }
        }
        return uniqueTasks;
    }

    public boolean canAccessTask(int userId, int taskId) {
        if (userId <= 0 || taskId <= 0) {
            return false;
        }

        Task task = taskDAO.getTaskById(taskId);
        if (task == null) {
            return false;
        }

        return task.getCreatorId() == userId || collaboratorService.isCollaborator(taskId, userId);
    }

    public List<Task> getVisibleTasksSortedByDueDate(int userId) {
        List<Task> visibleTasks = getAllVisibleTasks(userId);
        visibleTasks.sort(Comparator
                .comparing((Task task) -> task.getDueDate() == null ? 1 : 0)
                .thenComparing(task -> task.getDueDate() == null ? null : task.getDueDate().toLocalDate(),
                        Comparator.nullsLast(Comparator.naturalOrder()))
                .thenComparingInt(Task::getImportance).reversed()
                .thenComparingInt(Task::getTaskId));
        return visibleTasks;
    }

    private boolean isBlank(String value) {
        return value == null || value.trim().isEmpty();
    }
}
