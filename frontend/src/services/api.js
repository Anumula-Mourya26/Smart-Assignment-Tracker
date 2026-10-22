const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8080";

/**
 * Helper to handle HTTP responses and error messages gracefully.
 */
async function handleResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  let data = null;

  if (contentType.includes("application/json")) {
    try {
      data = await response.json();
    } catch {
      data = null;
    }
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    const errorMsg =
      (data && typeof data === "object" && data.error) ||
      (typeof data === "string" && data) ||
      `Request failed with status ${response.status}`;
    const error = new Error(errorMsg);
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}

export const api = {
  // Auth endpoints
  async register(gmail, password, username = "") {
    const payload = { gmail: gmail.trim(), password };
    if (username && username.trim()) {
      payload.username = username.trim();
    }
    const response = await fetch(`${API_BASE}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return handleResponse(response);
  },

  async login(gmail, password) {
    const response = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ gmail: gmail.trim(), password }),
    });
    return handleResponse(response);
  },

  // Task endpoints
  async getUserTasks(userId) {
    const response = await fetch(`${API_BASE}/api/tasks/user/${userId}`);
    const data = await handleResponse(response);
    return Array.isArray(data) ? data : [];
  },

  async getTask(taskId, userId) {
    const url = userId ? `${API_BASE}/api/tasks/${taskId}?userId=${userId}` : `${API_BASE}/api/tasks/${taskId}`;
    const response = await fetch(url);
    return handleResponse(response);
  },

  async createTask(taskData) {
    const response = await fetch(`${API_BASE}/api/tasks/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: taskData.title,
        description: taskData.description || "",
        importance: Number(taskData.importance),
        due_date: taskData.dueDate || "",
        creator_id: Number(taskData.creatorId),
      }),
    });
    return handleResponse(response);
  },

  async toggleTaskCompletion(taskId, completed) {
    const response = await fetch(`${API_BASE}/api/tasks/${taskId}/complete`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: Boolean(completed) }),
    });
    return handleResponse(response);
  },

  async getHighestPriorityTask(userId) {
    const response = await fetch(`${API_BASE}/api/tasks/priority/${userId}`);
    if (response.status === 404) {
      return null;
    }
    return handleResponse(response);
  },

  async getCalendarImportance(userId) {
    const response = await fetch(`${API_BASE}/api/calendar/${userId}`);
    const data = await handleResponse(response);
    return data && typeof data === "object" ? data : {};
  },

  // Subtask endpoints
  async getSubtasks(taskId) {
    const response = await fetch(`${API_BASE}/api/tasks/${taskId}/subtasks`);
    const data = await handleResponse(response);
    return Array.isArray(data) ? data : [];
  },

  async createSubtask(taskId, title) {
    const response = await fetch(`${API_BASE}/api/tasks/${taskId}/subtasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: title.trim() }),
    });
    return handleResponse(response);
  },

  async toggleSubtask(subtaskId, completed) {
    const response = await fetch(`${API_BASE}/api/subtasks/${subtaskId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: Boolean(completed) }),
    });
    return handleResponse(response);
  },

  async deleteSubtask(subtaskId) {
    const response = await fetch(`${API_BASE}/api/subtasks/${subtaskId}`, {
      method: "DELETE",
    });
    return handleResponse(response);
  },

  // Collaborator endpoints
  async getCollaborators(taskId) {
    const response = await fetch(`${API_BASE}/api/tasks/${taskId}/collaborators`);
    const data = await handleResponse(response);
    return Array.isArray(data) ? data : [];
  },

  async getCollaboratorDetails(taskId) {
    const response = await fetch(`${API_BASE}/api/tasks/${taskId}/collaborator-details`);
    const data = await handleResponse(response);
    return Array.isArray(data) ? data : [];
  },

  async addCollaborator(taskId, collaboratorIdentifier, status = "PENDING") {
    const payload = {};
    if (typeof collaboratorIdentifier === "string" && collaboratorIdentifier.includes("@")) {
      payload.gmail = collaboratorIdentifier.trim();
    } else {
      payload.user_id = Number(collaboratorIdentifier);
    }
    payload.status = status;

    const response = await fetch(`${API_BASE}/api/tasks/${taskId}/collaborator`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return handleResponse(response);
  },

  async getPendingRequests(userId) {
    const response = await fetch(`${API_BASE}/api/collaborators/requests/${userId}`);
    const data = await handleResponse(response);
    return Array.isArray(data) ? data : [];
  },

  async acceptRequest(taskId, userId) {
    const response = await fetch(`${API_BASE}/api/collaborators/requests/${taskId}/accept`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: Number(userId) }),
    });
    return handleResponse(response);
  },

  async declineRequest(taskId, userId) {
    const response = await fetch(`${API_BASE}/api/collaborators/requests/${taskId}/decline`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: Number(userId) }),
    });
    return handleResponse(response);
  },
};
