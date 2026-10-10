const API_BASE_URL = "http://localhost:8080";

const getUserId = () => Number(localStorage.getItem("smartTaskUserId"));
const getUserLabel = () => localStorage.getItem("smartTaskUserGmail") || "User";

function showMessage(message, type = "success") {
    const messageBox = document.getElementById("message");
    if (!messageBox) return;

    messageBox.textContent = message;
    messageBox.className = `message visible ${type}`;
}

function clearMessage() {
    const messageBox = document.getElementById("message");
    if (!messageBox) return;
    messageBox.textContent = "";
    messageBox.className = "message";
}

function parseJsonResponse(response) {
    return response.text().then((body) => {
        const data = body ? JSON.parse(body) : {};
        return { status: response.status, data };
    });
}

function validateHtmlForm(form) {
    if (!form || !form.reportValidity()) {
        return false;
    }
    return true;
}

async function registerUser(event) {
    event.preventDefault();
    clearMessage();

    const form = event.currentTarget;
    if (!validateHtmlForm(form)) return;

    const gmail = form.gmail.value.trim();
    const password = form.password.value;

    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ gmail, password })
        });
        const result = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(result.data.error || "Registration failed");
        }

        showMessage(`Registration successful. User ID: ${result.data.task_id || "created"}`, "success");
        form.reset();
    } catch (error) {
        showMessage(error.message || "Unable to register user. Check that the backend is running.", "error");
    }
}

async function loginUser(event) {
    event.preventDefault();
    clearMessage();

    const form = event.currentTarget;
    if (!validateHtmlForm(form)) return;

    const gmail = form.gmail.value.trim();
    const password = form.password.value;

    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ gmail, password })
        });
        const result = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(result.data.error || "Login failed");
        }

        localStorage.setItem("smartTaskUserId", String(result.data.user_id));
        localStorage.setItem("smartTaskUserGmail", result.data.gmail || gmail);
        window.location.href = "dashboard.html";
    } catch (error) {
        showMessage(error.message || "Unable to login. Check that the backend is running.", "error");
    }
}

async function createTask(event) {
    event.preventDefault();
    clearMessage();

    const form = event.currentTarget;
    if (!validateHtmlForm(form)) return;

    const userId = getUserId();
    if (!userId) {
        showMessage("Please login before creating a task.", "error");
        window.location.href = "login.html";
        return;
    }

    const body = {
        title: form.title.value.trim(),
        description: form.description.value.trim(),
        importance: Number(form.importance.value),
        due_date: form.due_date.value || null,
        creator_id: userId
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/tasks/create`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });
        const result = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(result.data.error || "Task creation failed");
        }

        showMessage("Task created successfully.", "success");
        form.reset();
        await loadTasks();
        await loadHighestPriorityTask();
        await loadCalendarImportance();
    } catch (error) {
        showMessage(error.message || "Task creation failed.", "error");
    }
}

async function loadTasks() {
    const userId = getUserId();
    const taskList = document.getElementById("taskList");
    if (!taskList) return;

    if (!userId) {
        taskList.innerHTML = '<tr><td colspan="6" class="empty-state">Please login to view tasks.</td></tr>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/tasks/user/${userId}`);
        const tasks = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(tasks.data.error || "Unable to load tasks");
        }

        if (!Array.isArray(tasks.data) || tasks.data.length === 0) {
            taskList.innerHTML = '<tr><td colspan="6" class="empty-state">No tasks found.</td></tr>';
            return;
        }

        taskList.innerHTML = tasks.data.map((task) => `
            <tr>
                <td><strong>${escapeHtml(task.title)}</strong></td>
                <td>${escapeHtml(task.description || "-")}</td>
                <td><span class="task-badge">${task.importance}</span></td>
                <td>${task.due_date ? formatDate(task.due_date) : "-"}</td>
                <td class="${task.completed ? "status-complete" : "status-incomplete"}">
                    ${task.completed ? "Completed" : "Incomplete"}
                </td>
                <td>
                    <button class="button primary small-button" data-complete-task="${task.task_id}" data-current-status="${task.completed}" type="button">
                        ${task.completed ? "Mark Incomplete" : "Mark Complete"}
                    </button>
                    <div class="collaborator-form">
                        <input data-collaborator-input="${task.task_id}" type="number" min="1" placeholder="Collaborator User ID">
                        <button class="button secondary small-button" data-add-collaborator="${task.task_id}" type="button">Add Collaborator</button>
                    </div>
                    <button class="button secondary small-button" data-load-collaborators="${task.task_id}" type="button">View Collaborators</button>
                    <ul class="collaborator-list" data-collaborator-list="${task.task_id}"></ul>
                </td>
            </tr>
        `).join("");

        bindTaskActionEvents();
    } catch (error) {
        taskList.innerHTML = `<tr><td colspan="6" class="empty-state">${escapeHtml(error.message)}</td></tr>`;
    }
}

async function completeTask(taskId, currentStatus) {
    const userId = getUserId();
    if (!userId || !taskId) return;

    const nextStatus = !currentStatus;

    try {
        const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}/complete`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ completed: nextStatus })
        });
        const result = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(result.data.error || "Unable to complete task");
        }

        showMessage(nextStatus ? "Task marked as completed." : "Task marked as incomplete.", "success");
        await loadTasks();
        await loadHighestPriorityTask();
        await loadCalendarImportance();
    } catch (error) {
        showMessage(error.message || "Unable to update task status.", "error");
    }
}

async function loadHighestPriorityTask() {
    const userId = getUserId();
    const container = document.getElementById("priorityTask");
    if (!container) return;

    if (!userId) {
        container.textContent = "Please login to view the highest priority task.";
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/tasks/priority/${userId}`);
        const result = await parseJsonResponse(response);

        if (response.status === 404) {
            container.textContent = "No incomplete task available.";
            return;
        }

        if (!response.ok) {
            throw new Error(result.data.error || "Unable to load priority task");
        }

        container.innerHTML = `
            <div class="priority-item">
                <strong>${escapeHtml(result.data.title)}</strong>
                <span><strong>Importance:</strong> <span class="priority-badge">${result.data.importance}</span></span>
                <span><strong>Due date:</strong> ${result.data.due_date ? formatDate(result.data.due_date) : "Not set"}</span>
                <span><strong>Status:</strong> ${result.data.completed ? "Completed" : "Incomplete"}</span>
            </div>
        `;
    } catch (error) {
        container.textContent = error.message;
    }
}

async function loadCalendarImportance() {
    const userId = getUserId();
    const tableBody = document.getElementById("calendarTable");
    if (!tableBody) return;

    if (!userId) {
        tableBody.innerHTML = '<tr><td colspan="2" class="empty-state">Please login to view calendar importance.</td></tr>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/calendar/${userId}`);
        const result = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(result.data.error || "Unable to load calendar importance");
        }

        const entries = Object.entries(result.data || {});
        if (entries.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="2" class="empty-state">No task dates available.</td></tr>';
            return;
        }

        tableBody.innerHTML = entries.map(([date, importance]) => `
            <tr>
                <td>${formatDate(date)}</td>
                <td>${importance}</td>
            </tr>
        `).join("");
    } catch (error) {
        tableBody.innerHTML = `<tr><td colspan="2" class="empty-state">${escapeHtml(error.message)}</td></tr>`;
    }
}

async function addCollaborator(taskId, userId) {
    if (!taskId || !userId) {
        showMessage("Enter a valid collaborator user ID.", "error");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}/collaborator`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId })
        });
        const result = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(result.data.error || "Unable to add collaborator");
        }

        showMessage("Collaborator added successfully.", "success");
        await loadTasks();
        await loadCollaborators(taskId);
    } catch (error) {
        showMessage(error.message || "Unable to add collaborator.", "error");
    }
}

async function loadCollaborators(taskId) {
    const list = document.querySelector(`[data-collaborator-list="${taskId}"]`);
    if (!list) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}/collaborators`);
        const result = await parseJsonResponse(response);

        if (!response.ok) {
            throw new Error(result.data.error || "Unable to load collaborators");
        }

        const collaboratorIds = Array.isArray(result.data) ? result.data : [];
        list.innerHTML = collaboratorIds.length === 0
            ? '<li class="empty-state">No collaborators yet.</li>'
            : collaboratorIds.map((id) => `<li>User ID: ${id}</li>`).join("");
    } catch (error) {
        list.innerHTML = `<li class="empty-state">${escapeHtml(error.message)}</li>`;
    }
}

function bindTaskActionEvents() {
    document.querySelectorAll("[data-complete-task]").forEach((button) => {
        button.onclick = () => completeTask(
            Number(button.dataset.completeTask),
            button.dataset.currentStatus === "true"
        );
    });

    document.querySelectorAll("[data-add-collaborator]").forEach((button) => {
        button.onclick = () => {
            const taskId = Number(button.dataset.addCollaborator);
            const input = document.querySelector(`[data-collaborator-input="${taskId}"]`);
            const collaboratorId = Number(input?.value);
            addCollaborator(taskId, collaboratorId);
        };
    });

    document.querySelectorAll("[data-load-collaborators]").forEach((button) => {
        button.onclick = () => loadCollaborators(Number(button.dataset.loadCollaborators));
    });
}

function formatDate(value) {
    if (!value) return "-";
    const date = new Date(`${value}T00:00:00`);
    return new Intl.DateTimeFormat("en-GB", { day: "2-digit", month: "short" }).format(date);
}

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function initializeAuth() {
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");

    if (registerForm) registerForm.addEventListener("submit", registerUser);
    if (loginForm) loginForm.addEventListener("submit", loginUser);
}

function initializeDashboard() {
    const dashboardContainer = document.querySelector(".dashboard");
    if (!dashboardContainer) {
        return;
    }

    const userId = getUserId();
    const userLabel = document.getElementById("userLabel");
    if (userLabel) userLabel.textContent = `Logged in: ${getUserLabel()}`;

    if (!userId) {
        window.location.href = "login.html";
        return;
    }

    const form = document.getElementById("createTaskForm");
    if (form) form.addEventListener("submit", createTask);

    const logoutButton = document.getElementById("logoutButton");
    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            localStorage.removeItem("smartTaskUserId");
            localStorage.removeItem("smartTaskUserGmail");
            window.location.href = "login.html";
        });
    }

    loadTasks();
    loadHighestPriorityTask();
    loadCalendarImportance();
}

document.addEventListener("DOMContentLoaded", () => {
    initializeAuth();
    initializeDashboard();
});
