package controller;

import com.sun.net.httpserver.HttpExchange;
import dao.CollaboratorDAO;
import dao.SubtaskDAO;
import dao.TaskDAO;
import dao.UserDAO;
import model.Session;
import model.Subtask;
import model.Task;
import model.User;
import service.CollaboratorService;
import service.TaskService;
import util.PasswordUtil;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.sql.Date;
import java.sql.Timestamp;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

public class TaskController {
    private final TaskService taskService;
    private final CollaboratorService collaboratorService;
    private final UserDAO userDAO;
    private final SubtaskDAO subtaskDAO;

    public TaskController() {
        TaskDAO taskDAO = new TaskDAO();
        this.taskService = new TaskService(taskDAO);
        this.collaboratorService = new CollaboratorService(
                taskDAO,
                new UserDAO(),
                new CollaboratorDAO()
        );
        this.userDAO = new UserDAO();
        this.subtaskDAO = new SubtaskDAO();
    }

    public void handle(HttpExchange exchange) throws IOException {
        String method = exchange.getRequestMethod();
        String path = exchange.getRequestURI().getPath();

        try {
            if ("OPTIONS".equalsIgnoreCase(method)) {
                sendResponse(exchange, 200, "{}", false);
                return;
            }

            if ("POST".equalsIgnoreCase(method) && "/api/auth/register".equals(path)) {
                handleRegisterUser(exchange);
                return;
            }
            if ("POST".equalsIgnoreCase(method) && "/api/auth/login".equals(path)) {
                handleLoginUser(exchange);
                return;
            }
            if ("POST".equalsIgnoreCase(method) && "/api/tasks/create".equals(path)) {
                handleCreateTask(exchange);
                return;
            }
            if ("GET".equalsIgnoreCase(method) && path.startsWith("/api/tasks/user/")) {
                handleGetUserTasks(exchange);
                return;
            }
            if ("GET".equalsIgnoreCase(method) && path.matches("/api/tasks/[0-9]+")) {
                handleGetTask(exchange);
                return;
            }
            if ("PUT".equalsIgnoreCase(method) && path.matches("/api/tasks/[0-9]+/complete")) {
                handleCompleteTask(exchange);
                return;
            }
            if ("GET".equalsIgnoreCase(method) && path.startsWith("/api/tasks/priority/")) {
                handleGetHighestPriorityTask(exchange);
                return;
            }
            if ("GET".equalsIgnoreCase(method) && path.startsWith("/api/calendar/")) {
                handleGetCalendarImportance(exchange);
                return;
            }
            if ("POST".equalsIgnoreCase(method) && path.matches("/api/tasks/[0-9]+/collaborator")) {
                handleAddCollaborator(exchange);
                return;
            }
            if ("GET".equalsIgnoreCase(method) && path.matches("/api/tasks/[0-9]+/collaborators")) {
                handleGetCollaborators(exchange);
                return;
            }
            if ("GET".equalsIgnoreCase(method) && path.matches("/api/tasks/[0-9]+/collaborator-details")) {
                handleGetCollaboratorDetails(exchange);
                return;
            }

            // Subtask routes
            if ("GET".equalsIgnoreCase(method) && path.matches("/api/tasks/[0-9]+/subtasks")) {
                handleGetSubtasks(exchange);
                return;
            }
            if ("POST".equalsIgnoreCase(method) && path.matches("/api/tasks/[0-9]+/subtasks")) {
                handleCreateSubtask(exchange);
                return;
            }
            if ("PUT".equalsIgnoreCase(method) && path.matches("/api/subtasks/[0-9]+")) {
                handleUpdateSubtask(exchange);
                return;
            }
            if ("DELETE".equalsIgnoreCase(method) && path.matches("/api/subtasks/[0-9]+")) {
                handleDeleteSubtask(exchange);
                return;
            }

            // Collaboration request routes
            if ("GET".equalsIgnoreCase(method) && path.startsWith("/api/collaborators/requests/")) {
                handleGetPendingRequests(exchange);
                return;
            }
            if ("POST".equalsIgnoreCase(method) && path.matches("/api/collaborators/requests/[0-9]+/accept")) {
                handleAcceptRequest(exchange);
                return;
            }
            if ("POST".equalsIgnoreCase(method) && path.matches("/api/collaborators/requests/[0-9]+/decline")) {
                handleDeclineRequest(exchange);
                return;
            }

            sendResponse(exchange, 404, jsonError("Endpoint not found"), false);
        } catch (Exception exception) {
            exception.printStackTrace();
            sendResponse(exchange, 500, jsonError("Internal server error: " + exception.getMessage()), true);
        }
    }

    private void handleRegisterUser(HttpExchange exchange) throws IOException {
        Map<String, String> requestData = readJsonObject(exchange);
        String username = requestData.get("username");
        String gmail = requestData.get("gmail");
        String password = requestData.get("password");

        if (isBlank(gmail) || isBlank(password)) {
            sendResponse(exchange, 400, jsonError("Gmail and password are required"), false);
            return;
        }

        String trimmedGmail = gmail.trim();
        if (!trimmedGmail.endsWith("@gmail.com")) {
            sendResponse(exchange, 400, jsonError("Gmail must end with @gmail.com"), false);
            return;
        }

        if (userDAO.gmailExists(trimmedGmail)) {
            sendResponse(exchange, 409, jsonError("An account with this Gmail already exists"), false);
            return;
        }

        try {
            User user = new User();
            if (!isBlank(username)) {
                user.setUsername(username.trim());
            } else {
                int at = trimmedGmail.indexOf('@');
                user.setUsername(at > 0 ? trimmedGmail.substring(0, at) : trimmedGmail);
            }
            user.setGmail(trimmedGmail);
            user.setPassword(PasswordUtil.hashPassword(password));
            user.setCreatedAt(new Timestamp(System.currentTimeMillis()));

            if (userDAO.registerUser(user)) {
                User savedUser = userDAO.findByGmail(trimmedGmail);
                String body = "{\n"
                        + "  \"success\": true,\n"
                        + "  \"message\": \"Registration successful\",\n"
                        + "  \"user_id\": " + savedUser.getUserId() + ",\n"
                        + "  \"username\": \"" + escapeJson(savedUser.getUsername()) + "\",\n"
                        + "  \"task_id\": " + savedUser.getUserId() + "\n"
                        + "}";
                sendResponse(exchange, 201, body, true);
                return;
            }
            sendResponse(exchange, 400, jsonError("Registration failed"), true);
        } catch (IllegalArgumentException exception) {
            sendResponse(exchange, 400, jsonError("Invalid password"), false);
        } catch (Exception exception) {
            sendResponse(exchange, 500, jsonError("Registration failed"), false);
        }
    }

    private void handleLoginUser(HttpExchange exchange) throws IOException {
        Map<String, String> requestData = readJsonObject(exchange);
        String gmail = requestData.get("gmail");
        String password = requestData.get("password");

        if (isBlank(gmail) || isBlank(password)) {
            sendResponse(exchange, 400, jsonError("Gmail and password are required"), false);
            return;
        }

        User user = userDAO.findByGmail(gmail.trim());
        if (user == null || !PasswordUtil.verifyPassword(password, user.getPassword())) {
            sendResponse(exchange, 401, jsonError("Invalid Gmail or password"), false);
            return;
        }

        Session session = new Session(user.getUserId(), user.getGmail());
        String uname = user.getUsername() != null && !user.getUsername().isBlank()
                ? user.getUsername()
                : user.getGmail();
        String body = "{\n"
                + "  \"success\": true,\n"
                + "  \"message\": \"Login successful\",\n"
                + "  \"user_id\": " + session.getUserId() + ",\n"
                + "  \"username\": \"" + escapeJson(uname) + "\",\n"
                + "  \"gmail\": \"" + escapeJson(session.getGmail()) + "\"\n"
                + "}";
        sendResponse(exchange, 200, body, true);
    }

    private void handleCreateTask(HttpExchange exchange) throws IOException {
        Map<String, String> requestData = readJsonObject(exchange);
        String title = requestData.get("title");
        String description = requestData.get("description");
        String importanceValue = requestData.get("importance");
        String dueDateValue = requestData.get("due_date");
        String creatorIdValue = requestData.get("creator_id");

        if (isBlank(title) || isBlank(importanceValue) || isBlank(creatorIdValue)) {
            sendResponse(exchange, 400, jsonError("title, importance, and creator_id are required"), false);
            return;
        }

        try {
            Task task = new Task();
            task.setTitle(title.trim());
            task.setDescription(description == null ? "" : description);
            task.setImportance(Integer.parseInt(importanceValue));
            task.setDueDate(isBlank(dueDateValue) ? null : Date.valueOf(LocalDate.parse(dueDateValue)));
            task.setCompleted(false);
            task.setCreatorId(Integer.parseInt(creatorIdValue));
            task.setCreatedAt(new Timestamp(System.currentTimeMillis()));

            boolean created = taskService.createTask(task);
            if (created) {
                sendResponse(exchange, 200, jsonSuccess("Task created", task.getTaskId()), true);
                return;
            }
            sendResponse(exchange, 400, jsonError("Task creation failed. Check the input values."), false);
        } catch (IllegalArgumentException exception) {
            sendResponse(exchange, 400, jsonError("Invalid request data"), false);
        }
    }

    private void handleGetUserTasks(HttpExchange exchange) throws IOException {
        int userId = readPathId(exchange.getRequestURI().getPath(), "/api/tasks/user/");
        if (userId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid userId is required"), false);
            return;
        }

        List<Task> tasks = taskService.getAllVisibleTasks(userId);
        sendResponse(exchange, 200, toTaskArrayJson(tasks), true);
    }

    private void handleGetTask(HttpExchange exchange) throws IOException {
        int taskId = readPathId(exchange.getRequestURI().getPath(), "/api/tasks/");
        if (taskId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid taskId is required"), true);
            return;
        }

        String query = exchange.getRequestURI().getQuery();
        int userId = -1;
        if (query != null && query.contains("userId=")) {
            for (String param : query.split("&")) {
                if (param.startsWith("userId=")) {
                    try {
                        userId = Integer.parseInt(param.substring("userId=".length()));
                    } catch (NumberFormatException ignored) {}
                }
            }
        }

        if (userId > 0 && !taskService.canAccessTask(userId, taskId)) {
            sendResponse(exchange, 403, jsonError("Access denied: You do not have permission to view this task"), true);
            return;
        }

        Task task = taskService.getTask(taskId);
        if (task == null) {
            sendResponse(exchange, 404, jsonError("Task not found"), true);
            return;
        }
        sendResponse(exchange, 200, toTaskJson(task), true);
    }

    private void handleCompleteTask(HttpExchange exchange) throws IOException {
        int taskId = readPathId(exchange.getRequestURI().getPath(), "/api/tasks/");
        String path = exchange.getRequestURI().getPath();
        int completeIndex = path.lastIndexOf("/complete");
        if (completeIndex <= 0 || taskId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid taskId is required"), false);
            return;
        }

        Map<String, String> requestData = readJsonObject(exchange);
        String completedValue = requestData.get("completed");
        if (completedValue == null) {
            sendResponse(exchange, 400, jsonError("completed is required"), false);
            return;
        }

        boolean completed = Boolean.parseBoolean(completedValue);
        boolean updated = taskService.markTaskCompleted(taskId, completed);
        if (updated) {
            sendResponse(exchange, 200, jsonSuccess("Task completion updated", taskId), true);
            return;
        }
        sendResponse(exchange, 404, jsonError("Task not found or update failed"), false);
    }

    private void handleGetHighestPriorityTask(HttpExchange exchange) throws IOException {
        int userId = readPathId(exchange.getRequestURI().getPath(), "/api/tasks/priority/");
        if (userId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid userId is required"), false);
            return;
        }

        Task task = taskService.getHighestPriorityTask(userId);
        if (task == null) {
            sendResponse(exchange, 404, jsonError("No incomplete tasks available"), false);
            return;
        }
        sendResponse(exchange, 200, toTaskJson(task), true);
    }

    private void handleGetCalendarImportance(HttpExchange exchange) throws IOException {
        int userId = readPathId(exchange.getRequestURI().getPath(), "/api/calendar/");
        if (userId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid userId is required"), false);
            return;
        }

        Map<LocalDate, Integer> importanceByDate = taskService.getCalendarImportance(userId);
        sendResponse(exchange, 200, toCalendarJson(importanceByDate), true);
    }

    private void handleAddCollaborator(HttpExchange exchange) throws IOException {
        int taskId = readPathId(exchange.getRequestURI().getPath(), "/api/tasks/");
        Map<String, String> requestData = readJsonObject(exchange);
        String userIdValue = requestData.get("user_id");
        String gmailValue = requestData.get("gmail");
        String status = requestData.get("status");

        int userId = -1;
        if (!isBlank(userIdValue)) {
            try {
                userId = Integer.parseInt(userIdValue);
            } catch (NumberFormatException ignored) {}
        } else if (!isBlank(gmailValue)) {
            User found = userDAO.findByGmail(gmailValue.trim());
            if (found == null) {
                found = userDAO.findByUsername(gmailValue.trim());
            }
            if (found != null) {
                userId = found.getUserId();
            } else {
                sendResponse(exchange, 404, jsonError("User with Gmail or Username '" + gmailValue + "' not found"), false);
                return;
            }
        }

        if (taskId <= 0 || userId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid taskId and user_id, username, or gmail are required"), false);
            return;
        }

        String actualStatus = isBlank(status) ? "ACCEPTED" : status;
        boolean added = collaboratorService.addCollaborator(taskId, userId, actualStatus);
        if (added) {
            sendResponse(exchange, 200, jsonSuccess("Collaborator added", taskId), true);
            return;
        }
        sendResponse(exchange, 400, jsonError("Collaborator could not be added"), false);
    }

    private void handleGetCollaborators(HttpExchange exchange) throws IOException {
        int taskId = readPathId(exchange.getRequestURI().getPath(), "/api/tasks/");
        if (taskId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid taskId is required"), false);
            return;
        }

        List<Integer> collaboratorIds = collaboratorService.getCollaboratorIds(taskId);
        sendResponse(exchange, 200, toIntegerArrayJson(collaboratorIds), true);
    }

    private void handleGetCollaboratorDetails(HttpExchange exchange) throws IOException {
        int taskId = readPathId(exchange.getRequestURI().getPath(), "/api/tasks/");
        if (taskId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid taskId is required"), false);
            return;
        }

        Task task = taskService.getTask(taskId);
        if (task == null) {
            sendResponse(exchange, 404, jsonError("Task not found"), false);
            return;
        }

        User owner = userDAO.findByUserId(task.getCreatorId());
        String ownerGmail = owner != null ? owner.getGmail() : ("User #" + task.getCreatorId());
        String ownerUsername = owner != null && owner.getUsername() != null && !owner.getUsername().isBlank()
                ? owner.getUsername()
                : ownerGmail;

        List<Map<String, Object>> collabs = collaboratorService.getCollaboratorDetails(taskId);

        StringBuilder sb = new StringBuilder();
        sb.append("[\n");
        // Always include owner first
        sb.append("  {\n");
        sb.append("    \"user_id\": ").append(task.getCreatorId()).append(",\n");
        sb.append("    \"gmail\": \"").append(escapeJson(ownerGmail)).append("\",\n");
        sb.append("    \"username\": \"").append(escapeJson(ownerUsername)).append("\",\n");
        sb.append("    \"role\": \"OWNER\",\n");
        sb.append("    \"status\": \"ACCEPTED\",\n");
        sb.append("    \"accepted_at\": \"").append(task.getCreatedAt()).append("\"\n");
        sb.append("  }");

        for (Map<String, Object> c : collabs) {
            int uid = (int) c.get("user_id");
            if (uid == task.getCreatorId()) continue;
            String cUsername = (String) c.get("username");
            if (cUsername == null || cUsername.isBlank()) {
                cUsername = (String) c.get("gmail");
            }
            sb.append(",\n  {\n");
            sb.append("    \"user_id\": ").append(uid).append(",\n");
            sb.append("    \"gmail\": \"").append(escapeJson((String) c.get("gmail"))).append("\",\n");
            sb.append("    \"username\": \"").append(escapeJson(cUsername)).append("\",\n");
            sb.append("    \"role\": \"COLLABORATOR\",\n");
            sb.append("    \"status\": \"").append(escapeJson((String) c.get("status"))).append("\",\n");
            sb.append("    \"accepted_at\": ").append(c.get("accepted_at") == null ? "null" : ("\"" + c.get("accepted_at") + "\"")).append(",\n");
            sb.append("    \"created_at\": \"").append(c.get("created_at")).append("\"\n");
            sb.append("  }");
        }
        sb.append("\n]");
        sendResponse(exchange, 200, sb.toString(), true);
    }

    // Subtask Handlers
    private void handleGetSubtasks(HttpExchange exchange) throws IOException {
        int taskId = readPathId(exchange.getRequestURI().getPath(), "/api/tasks/");
        if (taskId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid taskId is required"), false);
            return;
        }

        List<Subtask> subtasks = subtaskDAO.getSubtasksByTaskId(taskId);
        StringBuilder sb = new StringBuilder();
        sb.append("[\n");
        for (int i = 0; i < subtasks.size(); i++) {
            if (i > 0) sb.append(",\n");
            Subtask s = subtasks.get(i);
            sb.append("  {\n");
            sb.append("    \"subtask_id\": ").append(s.getSubtaskId()).append(",\n");
            sb.append("    \"task_id\": ").append(s.getTaskId()).append(",\n");
            sb.append("    \"title\": \"").append(escapeJson(s.getTitle())).append("\",\n");
            sb.append("    \"completed\": ").append(s.isCompleted()).append("\n");
            sb.append("  }");
        }
        sb.append("\n]");
        sendResponse(exchange, 200, sb.toString(), true);
    }

    private void handleCreateSubtask(HttpExchange exchange) throws IOException {
        int taskId = readPathId(exchange.getRequestURI().getPath(), "/api/tasks/");
        if (taskId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid taskId is required"), false);
            return;
        }

        Map<String, String> data = readJsonObject(exchange);
        String title = data.get("title");
        if (isBlank(title)) {
            sendResponse(exchange, 400, jsonError("Subtask title is required"), false);
            return;
        }

        Subtask created = subtaskDAO.createSubtask(taskId, title.trim());
        if (created != null) {
            String json = "{\n"
                    + "  \"success\": true,\n"
                    + "  \"subtask_id\": " + created.getSubtaskId() + ",\n"
                    + "  \"task_id\": " + created.getTaskId() + ",\n"
                    + "  \"title\": \"" + escapeJson(created.getTitle()) + "\",\n"
                    + "  \"completed\": " + created.isCompleted() + "\n"
                    + "}";
            sendResponse(exchange, 201, json, true);
            return;
        }
        sendResponse(exchange, 400, jsonError("Failed to create subtask"), false);
    }

    private void handleUpdateSubtask(HttpExchange exchange) throws IOException {
        int subtaskId = readPathId(exchange.getRequestURI().getPath(), "/api/subtasks/");
        if (subtaskId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid subtaskId is required"), false);
            return;
        }

        Map<String, String> data = readJsonObject(exchange);
        String completedVal = data.get("completed");
        if (completedVal == null) {
            sendResponse(exchange, 400, jsonError("completed is required"), false);
            return;
        }

        boolean comp = Boolean.parseBoolean(completedVal);
        boolean updated = subtaskDAO.updateSubtaskCompletion(subtaskId, comp);
        if (updated) {
            sendResponse(exchange, 200, "{\"success\":true,\"subtask_id\":" + subtaskId + ",\"completed\":" + comp + "}", true);
            return;
        }
        sendResponse(exchange, 404, jsonError("Subtask not found or update failed"), false);
    }

    private void handleDeleteSubtask(HttpExchange exchange) throws IOException {
        int subtaskId = readPathId(exchange.getRequestURI().getPath(), "/api/subtasks/");
        if (subtaskId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid subtaskId is required"), false);
            return;
        }

        boolean deleted = subtaskDAO.deleteSubtask(subtaskId);
        if (deleted) {
            sendResponse(exchange, 200, "{\"success\":true}", true);
            return;
        }
        sendResponse(exchange, 404, jsonError("Subtask not found"), false);
    }

    // Pending Requests Handlers
    private void handleGetPendingRequests(HttpExchange exchange) throws IOException {
        int userId = readPathId(exchange.getRequestURI().getPath(), "/api/collaborators/requests/");
        if (userId <= 0) {
            sendResponse(exchange, 400, jsonError("Valid userId is required"), false);
            return;
        }

        List<Map<String, Object>> requests = collaboratorService.getPendingRequests(userId);
        StringBuilder sb = new StringBuilder();
        sb.append("[\n");
        for (int i = 0; i < requests.size(); i++) {
            if (i > 0) sb.append(",\n");
            Map<String, Object> r = requests.get(i);
            sb.append("  {\n");
            sb.append("    \"task_id\": ").append(r.get("task_id")).append(",\n");
            sb.append("    \"title\": \"").append(escapeJson((String) r.get("title"))).append("\",\n");
            sb.append("    \"description\": \"").append(escapeJson((String) r.get("description"))).append("\",\n");
            sb.append("    \"importance\": ").append(r.get("importance")).append(",\n");
            sb.append("    \"due_date\": ").append(r.get("due_date") == null ? "null" : ("\"" + r.get("due_date") + "\"")).append(",\n");
            String cUsername = (String) r.get("creator_username");
            if (cUsername == null || cUsername.isBlank()) {
                cUsername = (String) r.get("creator_gmail");
            }
            sb.append("    \"creator_id\": ").append(r.get("creator_id")).append(",\n");
            sb.append("    \"creator_gmail\": \"").append(escapeJson((String) r.get("creator_gmail"))).append("\",\n");
            sb.append("    \"creator_username\": \"").append(escapeJson(cUsername)).append("\",\n");
            sb.append("    \"created_at\": \"").append(r.get("created_at")).append("\"\n");
            sb.append("  }");
        }
        sb.append("\n]");
        sendResponse(exchange, 200, sb.toString(), true);
    }

    private void handleAcceptRequest(HttpExchange exchange) throws IOException {
        int taskId = readPathId(exchange.getRequestURI().getPath(), "/api/collaborators/requests/");
        Map<String, String> data = readJsonObject(exchange);
        String userIdVal = data.get("user_id");
        if (taskId <= 0 || isBlank(userIdVal)) {
            sendResponse(exchange, 400, jsonError("Valid taskId and user_id are required"), false);
            return;
        }

        int userId = Integer.parseInt(userIdVal);
        boolean updated = collaboratorService.updateCollaboratorStatus(taskId, userId, "ACCEPTED");
        if (updated) {
            sendResponse(exchange, 200, "{\"success\":true,\"message\":\"Collaboration request accepted\"}", true);
            return;
        }
        sendResponse(exchange, 400, jsonError("Could not accept request"), false);
    }

    private void handleDeclineRequest(HttpExchange exchange) throws IOException {
        int taskId = readPathId(exchange.getRequestURI().getPath(), "/api/collaborators/requests/");
        Map<String, String> data = readJsonObject(exchange);
        String userIdVal = data.get("user_id");
        if (taskId <= 0 || isBlank(userIdVal)) {
            sendResponse(exchange, 400, jsonError("Valid taskId and user_id are required"), false);
            return;
        }

        int userId = Integer.parseInt(userIdVal);
        boolean removed = collaboratorService.removeCollaborator(taskId, userId);
        if (removed) {
            sendResponse(exchange, 200, "{\"success\":true,\"message\":\"Collaboration request declined\"}", true);
            return;
        }
        sendResponse(exchange, 400, jsonError("Could not decline request"), false);
    }

    private Map<String, String> readJsonObject(HttpExchange exchange) throws IOException {
        try (InputStream inputStream = exchange.getRequestBody()) {
            String body = new String(inputStream.readAllBytes(), StandardCharsets.UTF_8);
            return parseJsonObject(body);
        }
    }

    private Map<String, String> parseJsonObject(String body) {
        if (body == null || body.trim().isEmpty()) {
            return Map.of();
        }

        String trimmed = body.trim();
        if (trimmed.startsWith("{") && trimmed.endsWith("}")) {
            String content = trimmed.substring(1, trimmed.length() - 1);
            Map<String, String> values = new java.util.LinkedHashMap<>();
            List<String> pairs = splitTopLevel(content);
            for (String pair : pairs) {
                String[] parts = pair.split(":", 2);
                if (parts.length == 2) {
                    String key = unquote(parts[0].trim());
                    String value = unquote(parts[1].trim());
                    values.put(key, value);
                }
            }
            return values;
        }
        return Map.of();
    }

    private List<String> splitTopLevel(String content) {
        List<String> pairs = new java.util.ArrayList<>();
        StringBuilder current = new StringBuilder();
        boolean inQuotes = false;
        boolean escape = false;

        for (int i = 0; i < content.length(); i++) {
            char c = content.charAt(i);
            if (escape) {
                current.append(c);
                escape = false;
            } else if (c == '\\') {
                current.append(c);
                escape = true;
            } else if (c == '"') {
                inQuotes = !inQuotes;
                current.append(c);
            } else if (c == ',' && !inQuotes) {
                pairs.add(current.toString());
                current.setLength(0);
            } else {
                current.append(c);
            }
        }
        if (current.length() > 0) {
            pairs.add(current.toString());
        }
        return pairs;
    }

    private String unquote(String value) {
        String trimmed = value.trim();
        if (trimmed.length() >= 2 && trimmed.startsWith("\"") && trimmed.endsWith("\"")) {
            return trimmed.substring(1, trimmed.length() - 1)
                    .replace("\\\"", "\"")
                    .replace("\\n", "\n");
        }
        return trimmed;
    }

    private int readPathId(String path, String prefix) {
        String remaining = path.substring(prefix.length());
        int slashIndex = remaining.indexOf('/');
        if (slashIndex >= 0) {
            remaining = remaining.substring(0, slashIndex);
        }
        try {
            return Integer.parseInt(remaining);
        } catch (NumberFormatException exception) {
            return -1;
        }
    }

    private String toTaskJson(Task task) {
        User creator = userDAO.findByUserId(task.getCreatorId());
        String creatorGmail = creator != null ? creator.getGmail() : ("User #" + task.getCreatorId());
        String creatorUsername = creator != null && creator.getUsername() != null && !creator.getUsername().isBlank()
                ? creator.getUsername()
                : creatorGmail;
        int[] subtaskCounts = subtaskDAO.getSubtaskProgress(task.getTaskId());

        StringBuilder builder = new StringBuilder();
        builder.append("{\n");
        builder.append("  \"task_id\": ").append(task.getTaskId()).append(",\n");
        builder.append("  \"title\": \"").append(escapeJson(task.getTitle())).append("\",\n");
        builder.append("  \"description\": \"").append(escapeJson(task.getDescription())).append("\",\n");
        builder.append("  \"importance\": ").append(task.getImportance()).append(",\n");
        builder.append("  \"due_date\": ")
                .append(task.getDueDate() == null ? "null" : "\"" + task.getDueDate().toLocalDate() + "\"")
                .append(",\n");
        builder.append("  \"completed\": ").append(task.isCompleted()).append(",\n");
        builder.append("  \"creator_id\": ").append(task.getCreatorId()).append(",\n");
        builder.append("  \"creator_gmail\": \"").append(escapeJson(creatorGmail)).append("\",\n");
        builder.append("  \"creator_username\": \"").append(escapeJson(creatorUsername)).append("\",\n");
        builder.append("  \"subtasks_total\": ").append(subtaskCounts[0]).append(",\n");
        builder.append("  \"subtasks_completed\": ").append(subtaskCounts[1]).append("\n");
        builder.append("}");
        return builder.toString();
    }

    private String toTaskArrayJson(List<Task> tasks) {
        StringBuilder builder = new StringBuilder();
        builder.append("[\n");
        for (int index = 0; index < tasks.size(); index++) {
            if (index > 0) {
                builder.append(",\n");
            }
            builder.append("  ").append(toTaskJson(tasks.get(index)).replace("\n", "\n  "));
        }
        builder.append("\n]");
        return builder.toString();
    }

    private String toCalendarJson(Map<LocalDate, Integer> importanceByDate) {
        StringBuilder builder = new StringBuilder();
        builder.append("{\n");
        int index = 0;
        Set<Map.Entry<LocalDate, Integer>> entries = importanceByDate.entrySet();
        for (Map.Entry<LocalDate, Integer> entry : entries) {
            if (index > 0) {
                builder.append(",\n");
            }
            builder.append("  \"").append(entry.getKey()).append("\": ").append(entry.getValue());
            index++;
        }
        builder.append("\n}");
        return builder.toString();
    }

    private String toIntegerArrayJson(List<Integer> values) {
        StringBuilder builder = new StringBuilder();
        builder.append("[\n");
        for (int index = 0; index < values.size(); index++) {
            if (index > 0) {
                builder.append(",\n");
            }
            builder.append("  ").append(values.get(index));
        }
        builder.append("\n]");
        return builder.toString();
    }

    private String jsonSuccess(String message, int taskId) {
        return "{\n"
                + "  \"success\": true,\n"
                + "  \"message\": \"" + escapeJson(message) + "\",\n"
                + "  \"task_id\": " + taskId + "\n"
                + "}";
    }

    private String jsonError(String message) {
        return "{\n"
                + "  \"success\": false,\n"
                + "  \"error\": \"" + escapeJson(message) + "\"\n"
                + "}";
    }

    private String escapeJson(String value) {
        if (value == null) {
            return "";
        }
        return value.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }

    private void sendResponse(HttpExchange exchange, int statusCode, String body, boolean includeCors)
            throws IOException {
        byte[] response = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type, Accept");
        exchange.sendResponseHeaders(statusCode, response.length);
        try (var output = exchange.getResponseBody()) {
            output.write(response);
        }
    }

    private boolean isBlank(String value) {
        return value == null || value.trim().isEmpty();
    }
}
