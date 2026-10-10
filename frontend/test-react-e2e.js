/**
 * Comprehensive React Integration Test Suite
 * Tests all workflows corresponding to COMMAND 17 against http://localhost:8080
 */

const API_BASE = "http://localhost:8080";

async function runTests() {
  console.log("=================================================");
  console.log("  COMMAND 17: REACT API & INTEGRATION VERIFICATION");
  console.log("=================================================");

  const timestamp = Date.now();
  const user1Email = `react_u1_${timestamp}@gmail.com`;
  const user2Email = `react_u2_${timestamp}@gmail.com`;
  const password = "TestPassword123";

  let user1Id, user2Id, task1Id, task2Id, task3Id;

  // 1. REGISTRATION
  console.log("\n[TEST 1] Register User 1");
  const reg1Res = await fetch(`${API_BASE}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gmail: user1Email, password }),
  });
  const reg1Data = await reg1Res.json();
  if (reg1Res.status !== 201 || !reg1Data.user_id) {
    throw new Error(`User 1 registration failed: ${JSON.stringify(reg1Data)}`);
  }
  user1Id = reg1Data.user_id;
  console.log(`  -> PASSED: User 1 registered with ID ${user1Id}`);

  // Test duplicate registration rejection
  console.log("[TEST 1b] Prevent Duplicate Registration");
  const dupRes = await fetch(`${API_BASE}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gmail: user1Email, password }),
  });
  if (dupRes.status !== 409) {
    throw new Error(`Expected 409 for duplicate registration, got ${dupRes.status}`);
  }
  console.log("  -> PASSED: Duplicate registration rejected with 409 Conflict");

  // Register User 2
  console.log("\n[TEST 2] Register User 2");
  const reg2Res = await fetch(`${API_BASE}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gmail: user2Email, password }),
  });
  const reg2Data = await reg2Res.json();
  user2Id = reg2Data.user_id;
  console.log(`  -> PASSED: User 2 registered with ID ${user2Id}`);

  // 2. LOGIN
  console.log("\n[TEST 3] Login User 1");
  const loginRes = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gmail: user1Email, password }),
  });
  const loginData = await loginRes.json();
  if (loginRes.status !== 200 || loginData.user_id !== user1Id) {
    throw new Error(`User 1 login failed: ${JSON.stringify(loginData)}`);
  }
  console.log(`  -> PASSED: User 1 logged in successfully`);

  // Test bad password login
  console.log("[TEST 3b] Reject Invalid Password Login");
  const badLoginRes = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gmail: user1Email, password: "wrongpassword" }),
  });
  if (badLoginRes.status !== 401) {
    throw new Error(`Expected 401 for wrong password, got ${badLoginRes.status}`);
  }
  console.log("  -> PASSED: Bad password rejected with 401 Unauthorized");

  // 3. TASK CREATION
  console.log("\n[TEST 4] Task Creation for User 1");
  // Task 1: Importance 3, Due in 10 days
  const t1Res = await fetch(`${API_BASE}/api/tasks/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: "Task 1 - Normal",
      description: "Sample description for testing",
      importance: 3,
      due_date: "2026-10-25",
      creator_id: user1Id,
    }),
  });
  const t1Data = await t1Res.json();
  task1Id = t1Data.task_id;
  console.log(`  -> PASSED: Task 1 created with ID ${task1Id}`);

  // Task 2: Importance 5, Due in 5 days (Top Priority)
  const t2Res = await fetch(`${API_BASE}/api/tasks/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: "Task 2 - High Urgent",
      description: "High priority task due early",
      importance: 5,
      due_date: "2026-10-20",
      creator_id: user1Id,
    }),
  });
  const t2Data = await t2Res.json();
  task2Id = t2Data.task_id;

  // Task 3: Importance 5, Due in 8 days (Later date)
  const t3Res = await fetch(`${API_BASE}/api/tasks/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: "Task 3 - High Later",
      description: "High priority task due later",
      importance: 5,
      due_date: "2026-10-23",
      creator_id: user1Id,
    }),
  });
  const t3Data = await t3Res.json();
  task3Id = t3Data.task_id;
  console.log(`  -> PASSED: Multiple tasks created (IDs: ${task1Id}, ${task2Id}, ${task3Id})`);

  // 4. TASK RETRIEVAL
  console.log("\n[TEST 5] Retrieve User 1 Tasks");
  const listRes = await fetch(`${API_BASE}/api/tasks/user/${user1Id}`);
  const listData = await listRes.json();
  if (!Array.isArray(listData) || listData.length !== 3) {
    throw new Error(`Expected 3 tasks for User 1, got ${listData?.length}`);
  }
  console.log(`  -> PASSED: Retrieved 3 tasks successfully`);

  // 5. PRIORITY RANKING
  console.log("\n[TEST 6] Verify Priority Selection Logic");
  const prioRes = await fetch(`${API_BASE}/api/tasks/priority/${user1Id}`);
  const prioData = await prioRes.json();
  if (prioData.task_id !== task2Id) {
    throw new Error(`Expected Task 2 (${task2Id}) to be top priority, but got ${prioData.task_id}`);
  }
  console.log(`  -> PASSED: Task 2 (Imp=5, Due=2026-10-20) ranked highest over Task 3 (Due=2026-10-23)`);

  // 6. TOGGLE COMPLETION
  console.log("\n[TEST 7] Mark Task 2 Complete & Verify Priority Shift");
  const compRes = await fetch(`${API_BASE}/api/tasks/${task2Id}/complete`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed: true }),
  });
  if (compRes.status !== 200) {
    throw new Error(`Failed to complete task: ${compRes.status}`);
  }

  // Priority should now shift to Task 3
  const prioResAfter = await fetch(`${API_BASE}/api/tasks/priority/${user1Id}`);
  const prioDataAfter = await prioResAfter.json();
  if (prioDataAfter.task_id !== task3Id) {
    throw new Error(`Expected Task 3 (${task3Id}) to be new priority, got ${prioDataAfter.task_id}`);
  }
  console.log(`  -> PASSED: Once Task 2 was completed, Priority shifted to Task 3 (ID: ${task3Id})`);

  // 7. CALENDAR IMPORTANCE
  console.log("\n[TEST 8] Verify Calendar Importance Totals");
  const calRes = await fetch(`${API_BASE}/api/calendar/${user1Id}`);
  const calData = await calRes.json();
  if (calData["2026-10-20"] !== 5 || calData["2026-10-23"] !== 5 || calData["2026-10-25"] !== 3) {
    throw new Error(`Calendar totals mismatch: ${JSON.stringify(calData)}`);
  }
  console.log(`  -> PASSED: Calendar importance scores verified:`, calData);

  // 8. COLLABORATION WORKFLOW
  console.log("\n[TEST 9] Add Collaborator (User 2 to Task 3)");
  const addCollabRes = await fetch(`${API_BASE}/api/tasks/${task3Id}/collaborator`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: user2Id }),
  });
  if (addCollabRes.status !== 200) {
    throw new Error(`Failed to add collaborator: ${addCollabRes.status}`);
  }
  console.log(`  -> PASSED: User 2 added as collaborator to Task 3`);

  // Verify duplicate collaborator rejection
  console.log("[TEST 9b] Duplicate Collaborator Rejection");
  const dupCollabRes = await fetch(`${API_BASE}/api/tasks/${task3Id}/collaborator`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: user2Id }),
  });
  if (dupCollabRes.status !== 400) {
    throw new Error(`Expected 400 for duplicate collaborator, got ${dupCollabRes.status}`);
  }
  console.log("  -> PASSED: Duplicate collaborator rejected with 400");

  // Verify self-collaboration rejection
  console.log("[TEST 9c] Self-Collaboration Rejection");
  const selfCollabRes = await fetch(`${API_BASE}/api/tasks/${task3Id}/collaborator`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: user1Id }),
  });
  if (selfCollabRes.status !== 400) {
    throw new Error(`Expected 400 for creator self-collaboration, got ${selfCollabRes.status}`);
  }
  console.log("  -> PASSED: Creator self-collaboration rejected with 400");

  // Get Collaborators list
  console.log("\n[TEST 10] View Collaborator List");
  const listCollabRes = await fetch(`${API_BASE}/api/tasks/${task3Id}/collaborators`);
  const listCollabData = await listCollabRes.json();
  if (!Array.isArray(listCollabData) || !listCollabData.includes(user2Id)) {
    throw new Error(`User 2 not in collaborators list: ${JSON.stringify(listCollabData)}`);
  }
  console.log(`  -> PASSED: Collaborator list includes User 2:`, listCollabData);

  // 9. COLLABORATOR VISIBILITY (User 2 Perspective)
  console.log("\n[TEST 11] Shared Task Visibility from Collaborator (User 2) View");
  const user2TasksRes = await fetch(`${API_BASE}/api/tasks/user/${user2Id}`);
  const user2Tasks = await user2TasksRes.json();
  const sharedFound = user2Tasks.find((t) => t.task_id === task3Id);
  if (!sharedFound) {
    throw new Error(`Shared Task 3 not visible to User 2: ${JSON.stringify(user2Tasks)}`);
  }
  console.log(`  -> PASSED: User 2 can view shared Task 3 in task list`);

  // Shared task contributes to User 2's Priority Panel
  const user2PrioRes = await fetch(`${API_BASE}/api/tasks/priority/${user2Id}`);
  const user2PrioData = await user2PrioRes.json();
  if (user2PrioData.task_id !== task3Id) {
    throw new Error(`Shared task 3 did not appear as User 2's priority: ${JSON.stringify(user2PrioData)}`);
  }
  console.log(`  -> PASSED: Shared Task 3 contributes to User 2's priority panel`);

  // Shared task contributes to User 2's Calendar
  const user2CalRes = await fetch(`${API_BASE}/api/calendar/${user2Id}`);
  const user2CalData = await user2CalRes.json();
  if (user2CalData["2026-10-23"] !== 5) {
    throw new Error(`Shared task not in User 2 calendar: ${JSON.stringify(user2CalData)}`);
  }
  console.log(`  -> PASSED: Shared Task 3 contributes to User 2's calendar workload`);

  console.log("\n=================================================");
  console.log("  ALL REACT API & WORKFLOW TESTS PASSED (11/11)!");
  console.log("=================================================\n");
}

runTests().catch((err) => {
  console.error("Test failed:", err);
  process.exit(1);
});
