# Smart Task Tracking System

A full-stack web application designed for task management, dynamic priority ranking, calendar scheduling, and team collaboration. Built as an academic project for **B.Tech CSE** coursework in **Software Engineering**, **Java Object-Oriented Programming (OOP)**, and **Database Management Systems (DBMS)**.

---

## 1. Project Overview

The Smart Task Tracking System provides students and teams with an intuitive tool to manage assignments, deadlines, and shared workloads. It connects a lightweight HTML/CSS/JavaScript frontend directly to a plain Java HTTP backend backed by MySQL database persistence using JDBC.

The architecture emphasizes core Computer Science fundamentals—clean package separation (Model-View-Controller/DAO pattern), prepared SQL statements, secure password hashing, and algorithmic priority calculation—without the overhead or complexity of heavy enterprise frameworks.

---

## 2. Features

- **User Authentication:** Account registration and login with Gmail addresses, utilizing PBKDF2/SHA-256 salted password hashing.
- **Task Management:** Create, view, and mark tasks as Completed or Incomplete with titles, detailed descriptions, importance ratings (1 to 5), and due dates.
- **Dynamic Priority Engine:** Automatically evaluates incomplete tasks to determine and display the highest-priority item (prioritizing highest importance first, breaking ties with earlier due dates).
- **Calendar Importance Aggregation:** Groups tasks by due date and calculates total workload importance per calendar day.
- **Team Collaboration:** Share tasks with other users by User ID. Shared tasks appear dynamically in the collaborator's task list, calendar, and priority queue.
- **Robust Error Handling:** Validates importance bounds (1–5), non-empty titles, valid user and task IDs, and prevents duplicate collaborator assignments.

---

## 3. Technologies Used

- **Backend:** Java 25 (Standard Library `com.sun.net.httpserver.HttpServer`)
- **Database:** MySQL Server 8.4
- **Connectivity:** JDBC with MySQL Connector/J (`mysql-connector-j-9.4.0.jar`)
- **Frontend:** Vanilla HTML5, CSS3, and JavaScript (Fetch API)
- **Security:** Standard Java Cryptography Architecture (JCA) with PBKDF2 with HMAC-SHA256
- **Build Tool:** Apache Maven / Standard `javac` compiler

---

## 4. Project Folder Structure

```
viratcheka CBP/
├── pom.xml                     # Maven project configuration & MySQL driver dependency
├── README.md                   # Project documentation & presentation guide
├── sql/
│   └── schema.sql              # MySQL DDL schema (USER, TASK, TASK_COLLABORATOR)
├── src/
│   ├── controller/
│   │   ├── Server.java         # HTTP server entry point & static resource router
│   │   └── TaskController.java # REST API controller for auth, tasks & collaboration
│   ├── dao/
│   │   ├── CollaboratorDAO.java# JDBC operations for TASK_COLLABORATOR table
│   │   ├── TaskDAO.java        # JDBC operations for TASK table
│   │   └── UserDAO.java        # JDBC operations for USER table
│   ├── model/
│   │   ├── Session.java        # Authenticated user session model
│   │   ├── Task.java           # Task domain model entity
│   │   └── User.java           # User domain model entity
│   ├── service/
│   │   ├── CollaboratorService.java # Business logic for task sharing & permissions
│   │   └── TaskService.java    # Business logic for tasks, priority & calendar totals
│   ├── util/
│   │   ├── ConnectionTest.java # Utility to test MySQL database connectivity
│   │   ├── DBConnection.java   # Centralized JDBC connection provider
│   │   └── PasswordUtil.java   # PBKDF2 password hashing & salt verification
│   ├── test/
│   │   ├── AuthTest.java       # Unit tests for user registration & login
│   │   ├── CollaboratorServiceTest.java # Unit tests for collaboration logic
│   │   ├── IntegrationTestRunner.java   # End-to-end integration & error test runner
│   │   ├── TaskAccessTest.java # Tests for creator/collaborator access control
│   │   ├── TaskControllerTest.java     # HTTP API integration tests
│   │   ├── TaskDAOTest.java    # Database tests for Task persistence
│   │   ├── TaskServiceTest.java# Business logic & priority algorithm tests
│   │   └── UserDAOTest.java    # Database tests for User persistence
│   └── main/
│       └── resources/          # Frontend Web Assets
│           ├── index.html      # Landing page
│           ├── register.html   # User registration page
│           ├── login.html      # User login page
│           ├── dashboard.html  # Main application dashboard
│           ├── css/
│           │   └── style.css   # Responsive UI styles
│           └── js/
│               └── app.js      # Frontend interaction logic & API integration
└── target/                     # Compiled classes & build artifacts
```

---

## 5. MySQL Database Setup

1. Start your local MySQL Server (default port: `3306`).
2. Log into the MySQL client:
   ```powershell
   mysql -u root -p
   ```
3. Create the database and execute `sql/schema.sql`:
   ```sql
   CREATE DATABASE IF NOT EXISTS smart_task_tracker;
   USE smart_task_tracker;
   SOURCE sql/schema.sql;
   ```

### Schema Summary:
- **`USER`:** Stores `user_id` (PK, auto-increment), unique `gmail`, hashed `password`, and timestamp.
- **`TASK`:** Stores `task_id` (PK, auto-increment), `title`, `description`, `importance` (CHECK constraint 1–5), `due_date`, `completed`, `creator_id` (FK to `USER`), and timestamp.
- **`TASK_COLLABORATOR`:** Composite primary key `(task_id, user_id)` with cascading foreign keys to `TASK` and `USER`.

---

## 6. How to Configure the Database Connection

The application reads database credentials from environment variables via `util.DBConnection`. If not set, it defaults to `DB_USER=root` and an empty password.

To set your password in PowerShell before running:
```powershell
$env:DB_USER = "root"
$env:DB_PASSWORD = "your-mysql-password"
```

Verify your connection with the built-in connection tester:
```powershell
java -cp "target\classes;C:\Users\prayu\.m2\repository\com\mysql\mysql-connector-j\9.4.0\mysql-connector-j-9.4.0.jar" util.ConnectionTest
```
Expected output:
```
Database connection successful.
```

---

## 7. How to Compile and Run the Java Backend

### Step 1: Compile the Java Source Files
Using the standard Java compiler (`javac`):
```powershell
javac -cp "target\classes;C:\Users\prayu\.m2\repository\com\mysql\mysql-connector-j\9.4.0\mysql-connector-j-9.4.0.jar" -d target\classes (Get-ChildItem -Recurse -Filter "*.java" src | Select-Object -ExpandProperty FullName)
```

Sync web assets to the target folder:
```powershell
Copy-Item -Path "src\main\resources\*" -Destination "target\classes" -Recurse -Force
```

### Step 2: Start the HTTP Server
```powershell
$env:DB_PASSWORD = "your-mysql-password"
java -cp "target\classes;C:\Users\prayu\.m2\repository\com\mysql\mysql-connector-j\9.4.0\mysql-connector-j-9.4.0.jar" controller.Server
```

Expected console output:
```
Smart Task Tracker HTTP server started on http://localhost:8080
```

---

## 8. How to Open and Run the Frontend

Once the server is running, the frontend is served directly by the Java backend:
1. Open your web browser (Chrome, Edge, or Firefox).
2. Navigate to:
   - **Landing Page:** [http://localhost:8080/](http://localhost:8080/)
   - **Registration:** [http://localhost:8080/register.html](http://localhost:8080/register.html)
   - **Login:** [http://localhost:8080/login.html](http://localhost:8080/login.html)
   - **Dashboard:** [http://localhost:8080/dashboard.html](http://localhost:8080/dashboard.html)
3. Register an account with your Gmail (e.g., `student@gmail.com`) and a password (minimum 6 characters).
4. Login to access the dashboard to create and track tasks.

---

## 9. REST API Endpoint Reference

| Method | Endpoint | Description | Status Codes |
|---|---|---|---|
| `POST` | `/api/auth/register` | Register a new user (`gmail`, `password`) | `201 Created`, `400 Bad Request`, `409 Conflict` |
| `POST` | `/api/auth/login` | Authenticate user (`gmail`, `password`) | `200 OK`, `400 Bad Request`, `401 Unauthorized` |
| `POST` | `/api/tasks/create` | Create a new task (`title`, `importance`, `creator_id`, optional `due_date`, `description`) | `200 OK`, `400 Bad Request` |
| `GET` | `/api/tasks/user/{userId}` | Retrieve all tasks visible to a user (created + shared) | `200 OK`, `400 Bad Request` |
| `GET` | `/api/tasks/{taskId}` | Retrieve single task details (optional `?userId=X` access check) | `200 OK`, `403 Forbidden`, `404 Not Found` |
| `PUT` | `/api/tasks/{taskId}/complete` | Update task completion status (`completed`: true/false) | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `GET` | `/api/tasks/priority/{userId}` | Calculate and return the single highest-priority incomplete task | `200 OK`, `404 Not Found` (when no tasks exist) |
| `GET` | `/api/calendar/{userId}` | Group and aggregate total workload importance by due date | `200 OK`, `400 Bad Request` |
| `POST` | `/api/tasks/{taskId}/collaborator` | Add collaborator to a task (`user_id`) | `200 OK`, `400 Bad Request` |
| `GET` | `/api/tasks/{taskId}/collaborators` | List collaborator user IDs for a given task | `200 OK`, `400 Bad Request` |

---

## 10. Testing Instructions

The project includes unit tests, DAO tests, service tests, and an automated end-to-end integration test runner:

### Run the Full End-to-End Integration Suite:
```powershell
$env:DB_PASSWORD = "your-mysql-password"
java -cp "target\classes;C:\Users\prayu\.m2\repository\com\mysql\mysql-connector-j\9.4.0\mysql-connector-j-9.4.0.jar" test.IntegrationTestRunner
```
This tests:
1. Registration & Login flow
2. Task creation & MySQL database persistence
3. Task completion toggle & MySQL status updates
4. Multi-task priority engine (importance weight & earlier deadline rules)
5. Calendar workload importance date totals
6. Team collaboration & shared task visibility
7. All 8 required error & edge cases (empty title, out-of-range importance, invalid IDs, null dates, duplicate collaborators, unauthorized access).

### Run Individual Unit & Component Tests:
- **Authentication Test:** `java -cp ... test.AuthTest`
- **User DAO Test:** `java -cp ... test.UserDAOTest`
- **Task DAO Test:** `java -cp ... test.TaskDAOTest`
- **Task Service Test:** `java -cp ... test.TaskServiceTest`
- **Collaborator Service Test:** `java -cp ... test.CollaboratorServiceTest`
- **Access Control Test:** `java -cp ... test.TaskAccessTest`
- **Controller API Test:** `java -cp ... test.TaskControllerTest`

---

## 11. Known Limitations & Academic Design Decisions

1. **Stateless Session Management:** User identity is tracked client-side via `localStorage` after a successful login API call. For simplicity in a college demonstration, session tokens/JWTs are not used; endpoints receive user IDs via request paths/payloads.
2. **Plain HTTP Transport:** Standard `HttpServer` runs over plain HTTP (`http://localhost:8080`) rather than HTTPS. For production deployment, TLS/SSL certificates would be terminated via a reverse proxy (e.g., Nginx).
3. **Connection Management:** `DBConnection` issues fresh JDBC connections per query for concurrency safety. In enterprise systems, a connection pool (such as HikariCP) would be used.
4. **Scope Boundaries:** Advanced features such as real-time WebSocket notifications, recurring tasks, and rich-text editing were intentionally omitted to maintain clarity and adhere to core B.Tech CSE project objectives.
