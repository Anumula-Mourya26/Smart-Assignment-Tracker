package test;

import dao.CollaboratorDAO;
import dao.TaskDAO;
import dao.UserDAO;
import model.Task;
import model.User;
import service.CollaboratorService;
import service.TaskService;
import util.DBConnection;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.time.Duration;
import java.time.LocalDate;
import java.util.Map;

public class IntegrationTestRunner {
    private static final String BASE_URL = "http://localhost:8080";
    private static final HttpClient CLIENT = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(5))
            .build();

    public static void main(String[] args) throws Exception {
        System.out.println("=================================================================");
        System.out.println("  COMMAND 13: FRONTEND <-> BACKEND INTEGRATION TEST SUITE");
        System.out.println("=================================================================\n");

        long timestamp = System.currentTimeMillis();
        String user1Email = "cmd13.user1." + timestamp + "@gmail.com";
        String user2Email = "cmd13.user2." + timestamp + "@gmail.com";
        String password = "Password123!";

        int user1Id = -1;
        int user2Id = -1;
        int task1Id = -1;
        int taskAId = -1;
        int taskBId = -1;
        int taskCId = -1;
        int taskDId = -1;
        int taskNoDateId = -1;

        // 1. Open the registration page
        System.out.println("[TEST 1] Open registration page");
        HttpResponse<String> regPageResp = sendGet(BASE_URL + "/register.html");
        assertEquals(200, regPageResp.statusCode(), "Registration page HTTP status");
        assertTrue(regPageResp.body().contains("Register"), "Registration page content check");
        System.out.println("  -> PASSED: register.html served with 200 OK\n");

        // 2. Create clearly identifiable test user 1
        System.out.println("[TEST 2] Create test user 1: " + user1Email);
        String reg1Json = String.format("{\"gmail\":\"%s\",\"password\":\"%s\"}", user1Email, password);
        HttpResponse<String> reg1Resp = sendPost(BASE_URL + "/api/auth/register", reg1Json);
        assertEquals(201, reg1Resp.statusCode(), "User 1 registration status");
        user1Id = extractInt(reg1Resp.body(), "task_id"); // endpoint returns task_id as id in jsonSuccess
        assertTrue(user1Id > 0, "User 1 ID > 0");
        System.out.println("  -> PASSED: User 1 created with ID: " + user1Id + "\n");

        // 3. Login using test user 1's Gmail and password
        System.out.println("[TEST 3] Login using user 1 credentials");
        String login1Json = String.format("{\"gmail\":\"%s\",\"password\":\"%s\"}", user1Email, password);
        HttpResponse<String> login1Resp = sendPost(BASE_URL + "/api/auth/login", login1Json);
        assertEquals(200, login1Resp.statusCode(), "User 1 login status");
        int loggedInUser1Id = extractInt(login1Resp.body(), "user_id");
        assertEquals(user1Id, loggedInUser1Id, "Logged in user ID match");
        System.out.println("  -> PASSED: Login successful for user 1\n");

        // 4. Open dashboard
        System.out.println("[TEST 4] Open dashboard page");
        HttpResponse<String> dashResp = sendGet(BASE_URL + "/dashboard.html");
        assertEquals(200, dashResp.statusCode(), "Dashboard page HTTP status");
        assertTrue(dashResp.body().contains("Dashboard"), "Dashboard page content check");
        System.out.println("  -> PASSED: dashboard.html served with 200 OK\n");

        // 5. Create a task with Title, Description, Importance, Due date
        System.out.println("[TEST 5] Create Task 1 (Importance=3, DueDate in 5 days)");
        LocalDate dueDate1 = LocalDate.now().plusDays(5);
        String createTask1Json = String.format(
                "{\"title\":\"Integration Task Alpha\",\"description\":\"First integration task for user 1\",\"importance\":3,\"due_date\":\"%s\",\"creator_id\":%d}",
                dueDate1, user1Id
        );
        HttpResponse<String> create1Resp = sendPost(BASE_URL + "/api/tasks/create", createTask1Json);
        assertEquals(200, create1Resp.statusCode(), "Task 1 creation HTTP status");
        task1Id = extractInt(create1Resp.body(), "task_id");
        assertTrue(task1Id > 0, "Task 1 ID > 0");
        System.out.println("  -> PASSED: Task 1 created with ID: " + task1Id + "\n");

        // 6. Verify task 1 is stored in MySQL
        System.out.println("[TEST 6] Verify Task 1 stored in MySQL directly");
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement("SELECT * FROM TASK WHERE task_id = ?")) {
            stmt.setInt(1, task1Id);
            try (ResultSet rs = stmt.executeQuery()) {
                assertTrue(rs.next(), "Task 1 found in MySQL");
                assertEquals("Integration Task Alpha", rs.getString("title"), "Task 1 title in MySQL");
                assertEquals(3, rs.getInt("importance"), "Task 1 importance in MySQL");
                assertEquals(dueDate1.toString(), rs.getDate("due_date").toString(), "Task 1 due date in MySQL");
                assertEquals(0, rs.getInt("completed"), "Task 1 completed status initially 0");
                assertEquals(user1Id, rs.getInt("creator_id"), "Task 1 creator_id in MySQL");
            }
        }
        System.out.println("  -> PASSED: Task 1 verified in MySQL\n");

        // 7. Verify task appears in the task list
        System.out.println("[TEST 7] Verify Task 1 appears in user task list");
        HttpResponse<String> userTasksResp = sendGet(BASE_URL + "/api/tasks/user/" + user1Id);
        assertEquals(200, userTasksResp.statusCode(), "Get user tasks status");
        assertTrue(userTasksResp.body().contains("\"task_id\": " + task1Id), "Task list contains task 1 ID");
        assertTrue(userTasksResp.body().contains("Integration Task Alpha"), "Task list contains task 1 title");
        System.out.println("  -> PASSED: Task 1 appears in user task list\n");

        // 8. Mark the task as completed
        System.out.println("[TEST 8] Mark Task 1 as completed");
        HttpResponse<String> completeResp = sendPut(BASE_URL + "/api/tasks/" + task1Id + "/complete", "{\"completed\":true}");
        assertEquals(200, completeResp.statusCode(), "Complete task status");
        System.out.println("  -> PASSED: Mark complete returned 200 OK\n");

        // 9. Verify completion status changes in the database
        System.out.println("[TEST 9] Verify Task 1 completion updated in MySQL");
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement("SELECT completed FROM TASK WHERE task_id = ?")) {
            stmt.setInt(1, task1Id);
            try (ResultSet rs = stmt.executeQuery()) {
                assertTrue(rs.next(), "Task 1 found");
                assertEquals(1, rs.getInt("completed"), "Task 1 completion is 1 (true) in MySQL");
            }
        }
        System.out.println("  -> PASSED: Completion status is 1 (true) in MySQL\n");

        // 10. Create multiple tasks with different importance values and due dates
        System.out.println("[TEST 10] Create multiple tasks with different importance & due dates");
        LocalDate dateA = LocalDate.now().plusDays(4);
        String taskAJson = String.format("{\"title\":\"Task A - Med\",\"description\":\"Imp 4\",\"importance\":4,\"due_date\":\"%s\",\"creator_id\":%d}", dateA, user1Id);
        HttpResponse<String> taskAResp = sendPost(BASE_URL + "/api/tasks/create", taskAJson);
        taskAId = extractInt(taskAResp.body(), "task_id");

        LocalDate dateB = LocalDate.now().plusDays(8);
        String taskBJson = String.format("{\"title\":\"Task B - High Late\",\"description\":\"Imp 5, due later\",\"importance\":5,\"due_date\":\"%s\",\"creator_id\":%d}", dateB, user1Id);
        HttpResponse<String> taskBResp = sendPost(BASE_URL + "/api/tasks/create", taskBJson);
        taskBId = extractInt(taskBResp.body(), "task_id");

        LocalDate dateC = LocalDate.now().plusDays(2);
        String taskCJson = String.format("{\"title\":\"Task C - High Early\",\"description\":\"Imp 5, due earlier\",\"importance\":5,\"due_date\":\"%s\",\"creator_id\":%d}", dateC, user1Id);
        HttpResponse<String> taskCResp = sendPost(BASE_URL + "/api/tasks/create", taskCJson);
        taskCId = extractInt(taskCResp.body(), "task_id");

        System.out.println("  -> Created Task A (ID=" + taskAId + ", Imp=4, Due=" + dateA + ")");
        System.out.println("  -> Created Task B (ID=" + taskBId + ", Imp=5, Due=" + dateB + ")");
        System.out.println("  -> Created Task C (ID=" + taskCId + ", Imp=5, Due=" + dateC + ")");
        System.out.println("  -> PASSED: Multiple tasks created\n");

        // 11. Verify the Highest Priority Task panel
        System.out.println("[TEST 11] Verify Highest Priority Task panel endpoint");
        HttpResponse<String> prioResp = sendGet(BASE_URL + "/api/tasks/priority/" + user1Id);
        assertEquals(200, prioResp.statusCode(), "Priority task HTTP status");
        System.out.println("  -> Priority task response: " + prioResp.body().trim());

        // 12. Verify higher importance is selected first
        // 13. Verify earlier due date wins when importance is equal
        System.out.println("[TEST 12 & 13] Verify Priority Logic (Higher Imp first, Earlier Due Date wins)");
        int priorityTaskId = extractInt(prioResp.body(), "task_id");
        assertEquals(taskCId, priorityTaskId, "Task C must win priority (Imp=5 and earlier date than Task B)");
        System.out.println("  -> PASSED: Task C (ID=" + taskCId + ") won over Task B (same Imp=5, later date) and Task A (Imp=4)\n");

        // 14. Verify the calendar importance totals
        System.out.println("[TEST 14] Verify Calendar Importance totals");
        HttpResponse<String> calResp = sendGet(BASE_URL + "/api/calendar/" + user1Id);
        assertEquals(200, calResp.statusCode(), "Calendar endpoint HTTP status");
        System.out.println("  -> Calendar response: " + calResp.body().trim());
        assertTrue(calResp.body().contains("\"" + dateA + "\": 4"), "Calendar includes Date A with importance 4");
        assertTrue(calResp.body().contains("\"" + dateB + "\": 5"), "Calendar includes Date B with importance 5");
        assertTrue(calResp.body().contains("\"" + dateC + "\": 5"), "Calendar includes Date C with importance 5");
        System.out.println("  -> PASSED: Calendar importance totals verified\n");

        // 15. Create a second test user
        System.out.println("[TEST 15] Create second test user: " + user2Email);
        String reg2Json = String.format("{\"gmail\":\"%s\",\"password\":\"%s\"}", user2Email, password);
        HttpResponse<String> reg2Resp = sendPost(BASE_URL + "/api/auth/register", reg2Json);
        assertEquals(201, reg2Resp.statusCode(), "User 2 registration status");
        user2Id = extractInt(reg2Resp.body(), "task_id");
        assertTrue(user2Id > 0, "User 2 ID > 0");
        System.out.println("  -> PASSED: User 2 created with ID: " + user2Id + "\n");

        // 16. Add second user as collaborator to Task C
        System.out.println("[TEST 16] Add User 2 as collaborator to Task C (ID=" + taskCId + ")");
        String addCollabJson = String.format("{\"user_id\":%d}", user2Id);
        HttpResponse<String> addCollabResp = sendPost(BASE_URL + "/api/tasks/" + taskCId + "/collaborator", addCollabJson);
        assertEquals(200, addCollabResp.statusCode(), "Add collaborator HTTP status");

        // Verify in MySQL
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement("SELECT * FROM TASK_COLLABORATOR WHERE task_id = ? AND user_id = ?")) {
            stmt.setInt(1, taskCId);
            stmt.setInt(2, user2Id);
            try (ResultSet rs = stmt.executeQuery()) {
                assertTrue(rs.next(), "Collaborator entry found in MySQL TASK_COLLABORATOR table");
            }
        }
        System.out.println("  -> PASSED: User 2 added as collaborator and verified in MySQL\n");

        // 17. Login as second user
        System.out.println("[TEST 17] Login as second user");
        String login2Json = String.format("{\"gmail\":\"%s\",\"password\":\"%s\"}", user2Email, password);
        HttpResponse<String> login2Resp = sendPost(BASE_URL + "/api/auth/login", login2Json);
        assertEquals(200, login2Resp.statusCode(), "User 2 login status");
        System.out.println("  -> PASSED: User 2 login successful\n");

        // 18. Verify that shared task is visible to second user
        System.out.println("[TEST 18] Verify shared Task C is visible to User 2");
        HttpResponse<String> user2TasksResp = sendGet(BASE_URL + "/api/tasks/user/" + user2Id);
        assertEquals(200, user2TasksResp.statusCode(), "User 2 tasks status");
        assertTrue(user2TasksResp.body().contains("\"task_id\": " + taskCId), "User 2 visible tasks includes Task C");
        System.out.println("  -> PASSED: Shared Task C is visible in User 2's task list\n");

        // 19. Verify shared task is included in second user's calendar importance
        System.out.println("[TEST 19] Verify shared task included in User 2 calendar");
        HttpResponse<String> user2CalResp = sendGet(BASE_URL + "/api/calendar/" + user2Id);
        assertEquals(200, user2CalResp.statusCode(), "User 2 calendar status");
        assertTrue(user2CalResp.body().contains("\"" + dateC + "\": 5"), "User 2 calendar includes Date C importance 5");
        System.out.println("  -> PASSED: Shared task appears in User 2's calendar\n");

        // 20. Verify shared task can appear in second user's priority panel
        System.out.println("[TEST 20] Verify shared task in User 2 priority panel");
        HttpResponse<String> user2PrioResp = sendGet(BASE_URL + "/api/tasks/priority/" + user2Id);
        assertEquals(200, user2PrioResp.statusCode(), "User 2 priority status");
        int user2PriorityTaskId = extractInt(user2PrioResp.body(), "task_id");
        assertEquals(taskCId, user2PriorityTaskId, "Shared Task C appears in User 2 priority panel");
        System.out.println("  -> PASSED: Shared Task C appears in User 2 priority panel\n");

        // =================================================================
        // ERROR CASES TESTING
        // =================================================================
        System.out.println("=================================================================");
        System.out.println("  ERROR CASES TESTING");
        System.out.println("=================================================================\n");

        // Case 1: Empty task title
        System.out.println("[ERROR CASE 1] Empty task title");
        String emptyTitleJson = String.format("{\"title\":\"\",\"description\":\"Empty title\",\"importance\":3,\"creator_id\":%d}", user1Id);
        HttpResponse<String> err1Resp = sendPost(BASE_URL + "/api/tasks/create", emptyTitleJson);
        assertEquals(400, err1Resp.statusCode(), "Empty title should return 400 Bad Request");
        System.out.println("  -> PASSED: Handled empty title with 400 Bad Request\n");

        // Case 2: Importance 0
        System.out.println("[ERROR CASE 2] Importance 0");
        String imp0Json = String.format("{\"title\":\"Zero Importance\",\"description\":\"imp 0\",\"importance\":0,\"creator_id\":%d}", user1Id);
        HttpResponse<String> err2Resp = sendPost(BASE_URL + "/api/tasks/create", imp0Json);
        assertEquals(400, err2Resp.statusCode(), "Importance 0 should return 400 Bad Request");
        System.out.println("  -> PASSED: Handled importance 0 with 400 Bad Request\n");

        // Case 3: Importance 6
        System.out.println("[ERROR CASE 3] Importance 6");
        String imp6Json = String.format("{\"title\":\"Six Importance\",\"description\":\"imp 6\",\"importance\":6,\"creator_id\":%d}", user1Id);
        HttpResponse<String> err3Resp = sendPost(BASE_URL + "/api/tasks/create", imp6Json);
        assertEquals(400, err3Resp.statusCode(), "Importance 6 should return 400 Bad Request");
        System.out.println("  -> PASSED: Handled importance 6 with 400 Bad Request\n");

        // Case 4: Invalid user ID
        System.out.println("[ERROR CASE 4] Invalid user ID");
        HttpResponse<String> err4aResp = sendGet(BASE_URL + "/api/tasks/user/-1");
        assertEquals(400, err4aResp.statusCode(), "User ID -1 should return 400 Bad Request");
        String nonExistentUserTaskJson = "{\"title\":\"NonExistent Creator\",\"description\":\"no user\",\"importance\":3,\"creator_id\":999999}";
        HttpResponse<String> err4bResp = sendPost(BASE_URL + "/api/tasks/create", nonExistentUserTaskJson);
        assertEquals(400, err4bResp.statusCode(), "Nonexistent user task creation handled safely with 400 Bad Request");
        System.out.println("  -> PASSED: Handled invalid user IDs safely\n");

        // Case 5: Invalid task ID
        System.out.println("[ERROR CASE 5] Invalid task ID");
        HttpResponse<String> err5aResp = sendGet(BASE_URL + "/api/tasks/-1");
        assertTrue(err5aResp.statusCode() == 400 || err5aResp.statusCode() == 404, "Task ID -1 should return 400 or 404");
        HttpResponse<String> err5bResp = sendGet(BASE_URL + "/api/tasks/999999");
        assertEquals(404, err5bResp.statusCode(), "Nonexistent task ID should return 404 Not Found");
        System.out.println("  -> PASSED: Handled invalid task IDs safely with error status (" + err5aResp.statusCode() + " and 404)\n");

        // Case 6: Task without a due date
        System.out.println("[ERROR CASE 6] Task without a due date");
        String noDateJson = String.format("{\"title\":\"Task Without Due Date\",\"description\":\"No deadline\",\"importance\":2,\"creator_id\":%d}", user1Id);
        HttpResponse<String> err6Resp = sendPost(BASE_URL + "/api/tasks/create", noDateJson);
        assertEquals(200, err6Resp.statusCode(), "Task without due date should be created successfully");
        taskNoDateId = extractInt(err6Resp.body(), "task_id");
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement("SELECT due_date FROM TASK WHERE task_id = ?")) {
            stmt.setInt(1, taskNoDateId);
            try (ResultSet rs = stmt.executeQuery()) {
                assertTrue(rs.next(), "Task found");
                assertTrue(rs.getDate("due_date") == null, "due_date is NULL in MySQL");
            }
        }
        System.out.println("  -> PASSED: Task without due date successfully stored with NULL date in MySQL\n");

        // Case 7: Duplicate collaborator
        System.out.println("[ERROR CASE 7] Duplicate collaborator");
        HttpResponse<String> err7Resp = sendPost(BASE_URL + "/api/tasks/" + taskCId + "/collaborator", addCollabJson);
        assertEquals(400, err7Resp.statusCode(), "Duplicate collaborator should return 400 Bad Request");
        System.out.println("  -> PASSED: Handled duplicate collaborator with 400 Bad Request\n");

        // Case 8: Accessing a task that user does not own or collaborate on
        System.out.println("[ERROR CASE 8] Accessing task user does not own or collaborate on");
        String taskDJson = String.format("{\"title\":\"Task D - Private to User 1\",\"description\":\"Private\",\"importance\":3,\"creator_id\":%d}", user1Id);
        HttpResponse<String> taskDResp = sendPost(BASE_URL + "/api/tasks/create", taskDJson);
        taskDId = extractInt(taskDResp.body(), "task_id");

        // User 2 tries to access Task D
        HttpResponse<String> err8Resp = sendGet(BASE_URL + "/api/tasks/" + taskDId + "?userId=" + user2Id);
        assertEquals(403, err8Resp.statusCode(), "User 2 cannot access private Task D -> 403 Forbidden");

        // Also verify service layer directly
        TaskDAO taskDAO = new TaskDAO();
        UserDAO userDAO = new UserDAO();
        CollaboratorDAO collaboratorDAO = new CollaboratorDAO();
        CollaboratorService collaboratorService = new CollaboratorService(taskDAO, userDAO, collaboratorDAO);
        TaskService taskService = new TaskService(taskDAO, collaboratorService);
        boolean canAccess = taskService.canAccessTask(user2Id, taskDId);
        assertTrue(!canAccess, "taskService.canAccessTask must return false for unrelated user");
        System.out.println("  -> PASSED: Unauthorized task access returned 403 Forbidden and service returned false\n");

        System.out.println("=================================================================");
        System.out.println("  ALL 20 USER FLOW STEPS AND 8 ERROR CASES PASSED SUCCESSFULLY!");
        System.out.println("=================================================================");
    }

    private static HttpResponse<String> sendGet(String url) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();
        return CLIENT.send(request, HttpResponse.BodyHandlers.ofString());
    }

    private static HttpResponse<String> sendPost(String url, String json) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();
        return CLIENT.send(request, HttpResponse.BodyHandlers.ofString());
    }

    private static HttpResponse<String> sendPut(String url, String json) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .PUT(HttpRequest.BodyPublishers.ofString(json))
                .build();
        return CLIENT.send(request, HttpResponse.BodyHandlers.ofString());
    }

    private static int extractInt(String body, String key) {
        String pattern = "\"" + key + "\":";
        int idx = body.indexOf(pattern);
        if (idx == -1) {
            pattern = "\"" + key + "\" :";
            idx = body.indexOf(pattern);
        }
        if (idx == -1) return -1;
        int start = idx + pattern.length();
        while (start < body.length() && (body.charAt(start) == ' ' || body.charAt(start) == '\n' || body.charAt(start) == '\r')) {
            start++;
        }
        int end = start;
        while (end < body.length() && Character.isDigit(body.charAt(end))) {
            end++;
        }
        return Integer.parseInt(body.substring(start, end));
    }

    private static void assertEquals(Object expected, Object actual, String message) {
        if (!expected.equals(actual)) {
            throw new AssertionError(message + " - Expected: " + expected + ", Actual: " + actual);
        }
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError("Assertion failed: " + message);
        }
    }
}
