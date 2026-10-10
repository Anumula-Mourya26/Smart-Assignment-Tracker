package test;

import com.sun.net.httpserver.HttpServer;
import dao.CollaboratorDAO;
import dao.TaskDAO;
import dao.UserDAO;
import model.Task;
import model.User;
import service.CollaboratorService;
import service.TaskService;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpTimeoutException;
import java.nio.charset.StandardCharsets;
import java.sql.Date;
import java.sql.Timestamp;
import java.time.Duration;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

public class TaskControllerTest {
    private static final HttpClient HTTP_CLIENT = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(5))
            .build();
    private static final String TEST_EMAIL_PREFIX = "controller.test." + System.currentTimeMillis() + ".";
    private static final int SERVER_PORT = 8080;
    private static final String BASE_URL = "http://localhost:" + SERVER_PORT;

    public static void main(String[] args) throws Exception {
        HttpServer server = null;
        User creator = null;
        User collaborator = null;
        Task createdTask = null;
        Task higherPriorityTask = null;

        try {
            try {
                server = new controller.Server().startServer(SERVER_PORT);
            } catch (java.net.BindException e) {
                System.out.println("HTTP Server already running on port " + SERVER_PORT + ", reusing existing instance.");
            }
            creator = createUser("creator" + TEST_EMAIL_PREFIX + "@gmail.com");
            collaborator = createUser("collaborator" + TEST_EMAIL_PREFIX + "@gmail.com");

            createdTask = createTask(creator.getUserId(), "Controller test task " + System.currentTimeMillis(),
                    "Created through HTTP API", 3, LocalDate.now().plusDays(2));

            HttpResponse<?> getTaskResponse = sendGet(BASE_URL + "/api/tasks/" + createdTask.getTaskId());
            assertStatus(getTaskResponse, 200, "Get task failed");
            assertJsonContains(getTaskResponse, "\"title\": \"Controller test task");

            HttpResponse<?> userTasksResponse = sendGet(BASE_URL + "/api/tasks/user/" + creator.getUserId());
            assertStatus(userTasksResponse, 200, "Get user tasks failed");
            assertJsonContains(userTasksResponse, "\"task_id\":" + createdTask.getTaskId());

            HttpResponse<?> completeResponse = sendPut(
                    BASE_URL + "/api/tasks/" + createdTask.getTaskId() + "/complete",
                    "{\"completed\":true}"
            );
            assertStatus(completeResponse, 200, "Complete task failed");
            assertJsonContains(completeResponse, "\"success\": true");

            higherPriorityTask = createTask(creator.getUserId(), "Higher priority controller task " + System.currentTimeMillis(),
                    "Higher priority task", 5, LocalDate.now().plusDays(1));
            HttpResponse<?> priorityResponse = sendGet(BASE_URL + "/api/tasks/priority/" + creator.getUserId());
            assertStatus(priorityResponse, 200, "Priority endpoint failed");
            assertJsonContains(priorityResponse, "\"task_id\":" + higherPriorityTask.getTaskId());

            HttpResponse<?> calendarResponse = sendGet(BASE_URL + "/api/calendar/" + creator.getUserId());
            assertStatus(calendarResponse, 200, "Calendar endpoint failed");
            assertJsonContains(calendarResponse, "\"" + LocalDate.now().plusDays(1) + "\":");

            HttpResponse<?> addCollaboratorResponse = sendPost(
                    BASE_URL + "/api/tasks/" + createdTask.getTaskId() + "/collaborator",
                    "{\"user_id\":" + collaborator.getUserId() + "}"
            );
            assertStatus(addCollaboratorResponse, 200, "Add collaborator failed");
            assertJsonContains(addCollaboratorResponse, "\"success\": true");

            HttpResponse<?> collaboratorsResponse = sendGet(
                    BASE_URL + "/api/tasks/" + createdTask.getTaskId() + "/collaborators"
            );
            assertStatus(collaboratorsResponse, 200, "Get collaborators failed");
            assertJsonContains(collaboratorsResponse, String.valueOf(collaborator.getUserId()));

            System.out.println("TaskControllerTest: ALL HTTP API TESTS PASSED");
        } finally {
            if (createdTask != null) {
                new TaskDAO().deleteTask(createdTask.getTaskId());
            }
            if (higherPriorityTask != null) {
                new TaskDAO().deleteTask(higherPriorityTask.getTaskId());
            }
            if (collaborator != null && createdTask != null) {
                new CollaboratorDAO().removeCollaborator(createdTask.getTaskId(), collaborator.getUserId());
            }
            if (creator != null) {
                new UserDAO().findByGmail(creator.getGmail());
            }
            if (server != null) {
                server.stop(0);
            }
        }
    }

    private static User createUser(String gmail) {
        UserDAO userDAO = new UserDAO();
        User existing = userDAO.findByGmail(gmail);
        if (existing != null) {
            return existing;
        }

        User user = new User();
        user.setGmail(gmail);
        user.setPassword("temporary-password");
        user.setCreatedAt(new Timestamp(System.currentTimeMillis()));
        if (!userDAO.registerUser(user)) {
            throw new IllegalStateException("Unable to create controller test user: " + gmail);
        }
        return userDAO.findByGmail(gmail);
    }

    private static Task createTask(int creatorId, String title, String description, int importance, LocalDate dueDate)
            throws IOException, InterruptedException {
        Task task = new Task();
        task.setTitle(title);
        task.setDescription(description);
        task.setImportance(importance);
        task.setDueDate(Date.valueOf(dueDate));
        task.setCompleted(false);
        task.setCreatorId(creatorId);
        task.setCreatedAt(new Timestamp(System.currentTimeMillis()));

        HttpResponse<String> response = sendPost(
                BASE_URL + "/api/tasks/create",
                "{\"title\":\"" + title + "\",\"description\":\"" + description + "\","
                        + "\"importance\":" + importance + ",\"due_date\":\"" + dueDate + "\","
                        + "\"creator_id\":" + creatorId + "}"
        );
        assertStatus(response, 200, "Create task failed");
        assertJsonContains(response, "\"success\": true");

        TaskDAO taskDAO = new TaskDAO();
        List<Task> tasks = taskDAO.getTasksCreatedByUser(creatorId);
        return tasks.stream()
                .filter(item -> item.getTitle().equals(title))
                .max((left, right) -> Integer.compare(left.getTaskId(), right.getTaskId()))
                .orElseThrow(() -> new IllegalStateException("Created task not found after API call"));
    }

    private static HttpResponse<String> sendGet(String url) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder(URI.create(url))
                .header("Accept", "application/json")
                .timeout(Duration.ofSeconds(10))
                .GET()
                .build();
        return HTTP_CLIENT.send(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }

    private static HttpResponse<String> sendPost(String url, String body) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder(URI.create(url))
                .header("Content-Type", "application/json")
                .header("Accept", "application/json")
                .timeout(Duration.ofSeconds(10))
                .POST(HttpRequest.BodyPublishers.ofString(body, StandardCharsets.UTF_8))
                .build();
        return HTTP_CLIENT.send(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }

    private static HttpResponse<String> sendPut(String url, String body) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder(URI.create(url))
                .header("Content-Type", "application/json")
                .header("Accept", "application/json")
                .timeout(Duration.ofSeconds(10))
                .PUT(HttpRequest.BodyPublishers.ofString(body, StandardCharsets.UTF_8))
                .build();
        return HTTP_CLIENT.send(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }

    private static void assertStatus(HttpResponse<?> response, int expectedStatus, String message) {
        if (response.statusCode() != expectedStatus) {
            throw new IllegalStateException(message + ": expected HTTP " + expectedStatus
                    + " but was HTTP " + response.statusCode() + " body=" + response.body());
        }
    }

    private static void assertJsonContains(HttpResponse<?> response, String expectedText) {
        String body = String.valueOf(response.body()).replaceAll("\\s+", "");
        String normalizedExpectedText = expectedText.replaceAll("\\s+", "");
        if (!body.contains(normalizedExpectedText)) {
            throw new IllegalStateException("Expected response to contain '" + expectedText + "' but was: " + response.body());
        }
    }
}
