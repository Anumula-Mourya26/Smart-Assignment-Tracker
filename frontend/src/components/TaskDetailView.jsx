import React, { useState, useEffect, useCallback } from 'react';
import {
  ArrowLeft,
  CheckCircle2,
  Circle,
  Calendar,
  Star,
  Users,
  Plus,
  Trash2,
  Clock,
  UserPlus,
  AlertCircle,
  Check,
  ShieldCheck,
  X,
  ChevronRight
} from 'lucide-react';
import { api } from '../services/api';

export default function TaskDetailView({ task, currentUserId, onBack, onTaskUpdated, fromTab = 'tasks' }) {
  const [currentTask, setCurrentTask] = useState(task);
  const [subtasks, setSubtasks] = useState([]);
  const [collaborators, setCollaborators] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Form states
  const [newSubtaskTitle, setNewSubtaskTitle] = useState('');
  const [isAddingSubtask, setIsAddingSubtask] = useState(false);
  const [newCollabInput, setNewCollabInput] = useState('');
  const [isAddingCollab, setIsAddingCollab] = useState(false);

  const [notification, setNotification] = useState({ type: '', message: '' });

  const isOwner = currentUserId && currentTask.creator_id === currentUserId;

  const showNotification = (type, message) => {
    setNotification({ type, message });
    setTimeout(() => setNotification({ type: '', message: '' }), 4000);
  };

  // Sync task if prop changes
  useEffect(() => {
    if (task) {
      setCurrentTask(task);
    }
  }, [task]);

  const loadDetails = useCallback(async () => {
    if (!task?.task_id) return;
    setIsLoading(true);
    try {
      const [subs, collabs] = await Promise.all([
        api.getSubtasks(task.task_id),
        api.getCollaboratorDetails(task.task_id),
      ]);
      setSubtasks(subs);
      setCollaborators(collabs);
    } catch (err) {
      console.error('Failed to load task details:', err);
    } finally {
      setIsLoading(false);
    }
  }, [task?.task_id]);

  useEffect(() => {
    loadDetails();
  }, [loadDetails]);

  // Toggle Task Completion (Allowed ONLY from inside this view)
  const handleToggleTaskCompletion = async () => {
    try {
      const newStatus = !currentTask.completed;
      await api.toggleTaskCompletion(currentTask.task_id, newStatus);
      const updated = { ...currentTask, completed: newStatus };
      setCurrentTask(updated);
      showNotification('success', `Task marked as ${newStatus ? 'Completed' : 'Incomplete'}!`);
      if (onTaskUpdated) onTaskUpdated();
    } catch (err) {
      showNotification('error', `Failed to update task: ${err.message}`);
    }
  };

  // Add Subtask
  const handleAddSubtask = async (e) => {
    e.preventDefault();
    if (!newSubtaskTitle.trim()) return;

    setIsAddingSubtask(true);
    try {
      const created = await api.createSubtask(currentTask.task_id, newSubtaskTitle.trim());
      setSubtasks((prev) => [...prev, created]);
      setNewSubtaskTitle('');
      showNotification('success', 'Subtask added successfully!');
      if (onTaskUpdated) onTaskUpdated();
    } catch (err) {
      showNotification('error', `Failed to add subtask: ${err.message}`);
    } finally {
      setIsAddingSubtask(false);
    }
  };

  // Toggle Subtask Completion
  const handleToggleSubtask = async (subtaskId, completed) => {
    try {
      await api.toggleSubtask(subtaskId, !completed);
      setSubtasks((prev) =>
        prev.map((s) => (s.subtask_id === subtaskId ? { ...s, completed: !completed } : s))
      );
      if (onTaskUpdated) onTaskUpdated();
    } catch (err) {
      showNotification('error', `Failed to update subtask: ${err.message}`);
    }
  };

  // Delete Subtask
  const handleDeleteSubtask = async (subtaskId) => {
    try {
      await api.deleteSubtask(subtaskId);
      setSubtasks((prev) => prev.filter((s) => s.subtask_id !== subtaskId));
      showNotification('success', 'Subtask removed.');
      if (onTaskUpdated) onTaskUpdated();
    } catch (err) {
      showNotification('error', `Failed to delete subtask: ${err.message}`);
    }
  };

  // Add Collaborator (Only by Creator)
  const handleAddCollaborator = async (e) => {
    e.preventDefault();
    const val = newCollabInput.trim();
    if (!val) return;

    setIsAddingCollab(true);
    try {
      await api.addCollaborator(currentTask.task_id, val, 'ACCEPTED');
      showNotification('success', `Collaborator "${val}" added successfully!`);
      setNewCollabInput('');
      const updatedCollabs = await api.getCollaboratorDetails(currentTask.task_id);
      setCollaborators(updatedCollabs);
      if (onTaskUpdated) onTaskUpdated();
    } catch (err) {
      showNotification('error', err.message || 'Failed to add collaborator.');
    } finally {
      setIsAddingCollab(false);
    }
  };

  // Subtask progress calculations
  const totalSubtasks = subtasks.length;
  const completedSubtasks = subtasks.filter((s) => s.completed).length;
  const progressPercent = totalSubtasks > 0
    ? Math.round((completedSubtasks / totalSubtasks) * 100)
    : (currentTask.completed ? 100 : 0);

  // Sorting collaborators:
  // 1. Owner first
  // 2. You (if not owner)
  // 3. Others in chronological order of them accepting the collab invite
  const orderedCollaborators = [...collaborators].sort((a, b) => {
    if (a.role === 'OWNER') return -1;
    if (b.role === 'OWNER') return 1;

    const aIsYou = a.user_id === currentUserId;
    const bIsYou = b.user_id === currentUserId;
    if (aIsYou && !bIsYou) return -1;
    if (!aIsYou && bIsYou) return 1;

    const aTime = a.accepted_at ? new Date(a.accepted_at).getTime() : 0;
    const bTime = b.accepted_at ? new Date(b.accepted_at).getTime() : 0;
    return aTime - bTime;
  });

  const getImportanceBadgeClass = (importance) => {
    switch (importance) {
      case 5: return 'badge-imp-5';
      case 4: return 'badge-imp-4';
      case 3: return 'badge-imp-3';
      case 2: return 'badge-imp-2';
      default: return 'badge-imp-1';
    }
  };

  const backLabel = fromTab === 'dashboard' ? 'Back to Dashboard' : 'Back to My Tasks';

  return (
    <div className="task-detail-page" style={{ paddingBottom: 40 }}>
      {/* Top Breadcrumb & Exit Navigation Bar */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 18,
          background: '#ffffff',
          padding: '12px 18px',
          borderRadius: 10,
          border: '1px solid #e2e8f0'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: '0.88rem' }}>
          <button
            className="btn btn-outline btn-sm"
            onClick={onBack}
            style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontWeight: 700 }}
          >
            <ArrowLeft size={16} />
            <span>{backLabel}</span>
          </button>

          <span style={{ color: '#cbd5e1' }}>/</span>

          <span
            onClick={onBack}
            style={{ color: '#6366f1', cursor: 'pointer', fontWeight: 600 }}
            title="Click to go back"
          >
            {fromTab === 'dashboard' ? 'Dashboard' : 'My Tasks'}
          </span>

          <ChevronRight size={14} color="#94a3b8" />

          <span style={{ color: '#0f172a', fontWeight: 700, maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {currentTask.title}
          </span>
        </div>

        <button
          onClick={onBack}
          className="btn btn-outline btn-sm"
          title="Close Task Detail"
          style={{ display: 'inline-flex', alignItems: 'center', gap: 4, color: '#64748b' }}
        >
          <X size={16} />
          <span>Close</span>
        </button>
      </div>

      {notification.message && (
        <div className={`alert ${notification.type === 'error' ? 'alert-danger' : 'alert-success'}`} style={{ marginBottom: 20 }}>
          {notification.type === 'error' ? <AlertCircle size={18} /> : <Check size={18} />}
          <span>{notification.message}</span>
        </div>
      )}

      {/* TOP HEADER SECTION: Detailed Task Information */}
      <div className="panel" style={{ marginBottom: 24, padding: '24px 28px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16 }}>
          <div style={{ flex: '1 1 500px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
              <span className={`badge ${getImportanceBadgeClass(currentTask.importance)}`}>
                <Star size={13} fill="currentColor" />
                Priority {currentTask.importance}
              </span>
              <span className={`badge badge-status ${currentTask.completed ? 'completed' : 'pending'}`}>
                {currentTask.completed ? 'Completed' : 'Pending Action'}
              </span>
              {currentTask.due_date ? (
                <span className="badge-date">
                  <Calendar size={13} />
                  Due: {currentTask.due_date}
                </span>
              ) : (
                <span className="badge-date" style={{ color: '#94a3b8' }}>
                  <Clock size={13} />
                  No deadline
                </span>
              )}
            </div>

            <h1 style={{ fontSize: '1.75rem', fontWeight: 700, color: '#0f172a', margin: '4px 0 12px 0' }}>
              {currentTask.title}
            </h1>

            {/* Owner badge: 'You' in green or 'Username' in yellow */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
              <span style={{ fontSize: '0.85rem', color: '#64748b' }}>Owner:</span>
              {isOwner ? (
                <span
                  className="badge"
                  style={{
                    backgroundColor: '#dcfce7',
                    color: '#15803d',
                    borderColor: '#86efac',
                    fontWeight: 700,
                    padding: '4px 10px',
                    fontSize: '0.82rem'
                  }}
                >
                  You (Task Creator)
                </span>
              ) : (
                <span
                  className="badge"
                  style={{
                    backgroundColor: '#fef9c3',
                    color: '#854d0e',
                    borderColor: '#fde047',
                    fontWeight: 700,
                    padding: '4px 10px',
                    fontSize: '0.82rem'
                  }}
                >
                  {currentTask.creator_username || currentTask.creator_gmail || `User #${currentTask.creator_id}`}
                </span>
              )}
            </div>

            {currentTask.description && (
              <div style={{ background: '#f8fafc', padding: '14px 18px', borderRadius: 10, border: '1px solid #e2e8f0', color: '#334155', fontSize: '0.92rem', lineHeight: 1.6 }}>
                {currentTask.description}
              </div>
            )}
          </div>

          {/* Action button: Complete/Incomplete task inside view */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, alignItems: 'flex-end' }}>
            <button
              className={`btn ${currentTask.completed ? 'btn-outline' : 'btn-primary'}`}
              onClick={handleToggleTaskCompletion}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 8,
                padding: '10px 18px',
                fontSize: '0.95rem',
                backgroundColor: currentTask.completed ? 'transparent' : '#10b981',
                borderColor: currentTask.completed ? '#cbd5e1' : '#10b981'
              }}
            >
              <CheckCircle2 size={18} />
              <span>{currentTask.completed ? 'Mark as Incomplete' : 'Mark as Completed'}</span>
            </button>
          </div>
        </div>

        {/* Progress Bar Component */}
        <div style={{ marginTop: 24, paddingTop: 18, borderTop: '1px solid #f1f5f9' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8, fontSize: '0.85rem' }}>
            <span style={{ fontWeight: 600, color: '#334155' }}>
              Overall Task Progress: {completedSubtasks} of {totalSubtasks} subtasks completed
            </span>
            <span style={{ fontWeight: 700, color: progressPercent === 100 ? '#10b981' : '#6366f1', fontSize: '0.95rem' }}>
              {progressPercent}%
            </span>
          </div>
          <div style={{ height: 10, background: '#f1f5f9', borderRadius: 999, overflow: 'hidden' }}>
            <div
              style={{
                height: '100%',
                width: `${progressPercent}%`,
                background: progressPercent === 100 ? '#10b981' : 'linear-gradient(90deg, #6366f1, #8b5cf6)',
                borderRadius: 999,
                transition: 'width 0.4s ease'
              }}
            />
          </div>
        </div>
      </div>

      {/* TWO-COLUMN GRID: Subtasks (Left/Middle) & Collaborators (Right) */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: 24 }}>
        
        {/* LEFT/MIDDLE: Subtasks Section */}
        <section className="panel" style={{ padding: '22px 24px' }}>
          <div className="panel-header" style={{ marginBottom: 16 }}>
            <h3 className="panel-title" style={{ fontSize: '1.1rem', fontWeight: 700 }}>
              <span>Subtasks Checklist</span>
            </h3>
            <span className="panel-badge">{subtasks.length} items</span>
          </div>

          <p style={{ fontSize: '0.84rem', color: '#64748b', marginBottom: 16 }}>
            Break down this task into smaller milestones. The overall progress of this task updates automatically based on completed subtasks.
          </p>

          {/* Add Subtask Form */}
          <form onSubmit={handleAddSubtask} style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
            <input
              type="text"
              placeholder="Add a new subtask (e.g. Write Introduction)..."
              value={newSubtaskTitle}
              onChange={(e) => setNewSubtaskTitle(e.target.value)}
              className="input-field"
              style={{ flex: 1, padding: '10px 14px', borderRadius: 8, border: '1px solid #cbd5e1', fontSize: '0.9rem' }}
            />
            <button
              type="submit"
              className="btn btn-primary btn-sm"
              disabled={isAddingSubtask || !newSubtaskTitle.trim()}
              style={{ display: 'inline-flex', alignItems: 'center', gap: 6, whiteSpace: 'nowrap' }}
            >
              <Plus size={16} />
              <span>Add</span>
            </button>
          </form>

          {/* Subtasks List */}
          {isLoading ? (
            <div style={{ display: 'flex', justifyContent: 'center', padding: '30px 0' }}>
              <div className="spinner spinner-dark" />
            </div>
          ) : subtasks.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {subtasks.map((sub) => (
                <div
                  key={sub.subtask_id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 14px',
                    borderRadius: 8,
                    background: sub.completed ? '#f8fafc' : '#ffffff',
                    border: sub.completed ? '1px solid #e2e8f0' : '1px solid #cbd5e1',
                    transition: 'all 0.15s ease'
                  }}
                >
                  <div
                    onClick={() => handleToggleSubtask(sub.subtask_id, sub.completed)}
                    style={{ display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer', flex: 1 }}
                  >
                    {sub.completed ? (
                      <CheckCircle2 size={20} color="#10b981" />
                    ) : (
                      <Circle size={20} color="#94a3b8" />
                    )}
                    <span
                      style={{
                        fontSize: '0.92rem',
                        color: sub.completed ? '#94a3b8' : '#1e293b',
                        textDecoration: sub.completed ? 'line-through' : 'none',
                        fontWeight: sub.completed ? 400 : 500
                      }}
                    >
                      {sub.title}
                    </span>
                  </div>

                  <button
                    onClick={() => handleDeleteSubtask(sub.subtask_id)}
                    title="Remove Subtask"
                    style={{
                      background: 'none',
                      border: 'none',
                      cursor: 'pointer',
                      color: '#94a3b8',
                      padding: 4,
                      borderRadius: 4
                    }}
                    onMouseEnter={(e) => (e.currentTarget.style.color = '#ef4444')}
                    onMouseLeave={(e) => (e.currentTarget.style.color = '#94a3b8')}
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state" style={{ padding: '32px 0' }}>
              <CheckCircle2 size={32} className="empty-icon" color="#94a3b8" />
              <h4 style={{ fontSize: '1rem', marginTop: 8 }}>No Subtasks Yet</h4>
              <p style={{ fontSize: '0.84rem' }}>Add your first subtask above to track progress!</p>
            </div>
          )}
        </section>

        {/* RIGHT: Collaborators Section */}
        <section className="panel" style={{ padding: '22px 24px' }}>
          <div className="panel-header" style={{ marginBottom: 16 }}>
            <h3 className="panel-title" style={{ fontSize: '1.1rem', fontWeight: 700 }}>
              <Users size={20} color="#6366f1" />
              <span>Collaborators</span>
            </h3>
            <span className="panel-badge">{orderedCollaborators.length} members</span>
          </div>

          {/* Option to Add Collaborator (ONLY shown to the creator) */}
          {isOwner ? (
            <div style={{ marginBottom: 22, background: '#f8fafc', padding: '16px', borderRadius: 10, border: '1px solid #e2e8f0' }}>
              <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
                <UserPlus size={16} color="#6366f1" />
                <span>Invite New Collaborator</span>
              </div>
              <form onSubmit={handleAddCollaborator} style={{ display: 'flex', gap: 8 }}>
                <input
                  type="text"
                  placeholder="Enter Username, Gmail, or User ID"
                  value={newCollabInput}
                  onChange={(e) => setNewCollabInput(e.target.value)}
                  style={{ flex: 1, padding: '9px 12px', borderRadius: 8, border: '1px solid #cbd5e1', fontSize: '0.86rem' }}
                />
                <button
                  type="submit"
                  className="btn btn-primary btn-sm"
                  disabled={isAddingCollab || !newCollabInput.trim()}
                  style={{ whiteSpace: 'nowrap' }}
                >
                  {isAddingCollab ? 'Adding...' : 'Add'}
                </button>
              </form>
              <div style={{ fontSize: '0.74rem', color: '#64748b', marginTop: 6 }}>
                As the creator, you can share this task with fellow students or team members by username or Gmail.
              </div>
            </div>
          ) : (
            <div style={{ marginBottom: 18, background: '#f1f5f9', padding: '12px 14px', borderRadius: 8, fontSize: '0.82rem', color: '#64748b', display: 'flex', alignItems: 'center', gap: 8 }}>
              <ShieldCheck size={16} color="#64748b" />
              <span>Only the creator ({currentTask.creator_username || currentTask.creator_gmail || `User #${currentTask.creator_id}`}) can add new collaborators.</span>
            </div>
          )}

          {/* Collaborator List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {orderedCollaborators.map((c) => {
              const cIsOwner = c.role === 'OWNER';
              const cIsYou = c.user_id === currentUserId;

              return (
                <div
                  key={c.user_id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 14px',
                    borderRadius: 8,
                    background: cIsOwner ? '#f0fdf4' : (cIsYou ? '#eef2ff' : '#ffffff'),
                    border: cIsOwner ? '1px solid #bbf7d0' : (cIsYou ? '1px solid #c7d2fe' : '1px solid #e2e8f0'),
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    <div
                      style={{
                        width: 34,
                        height: 34,
                        borderRadius: '50%',
                        background: cIsOwner ? '#22c55e' : (cIsYou ? '#6366f1' : '#94a3b8'),
                        color: '#ffffff',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: 700,
                        fontSize: '0.85rem'
                      }}
                    >
                      {c.username ? c.username.charAt(0).toUpperCase() : (c.gmail ? c.gmail.charAt(0).toUpperCase() : 'U')}
                    </div>
                    <div>
                      <div style={{ fontSize: '0.9rem', fontWeight: 600, color: '#1e293b' }}>
                        {c.username ? `@${c.username}` : (c.gmail || `User #${c.user_id}`)}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                        {c.username ? c.gmail : `User ID: #${c.user_id}`}
                      </div>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    {cIsOwner ? (
                      <span
                        className="badge"
                        style={{
                          backgroundColor: '#dcfce7',
                          color: '#15803d',
                          borderColor: '#86efac',
                          fontWeight: 700,
                          fontSize: '0.75rem'
                        }}
                      >
                        Owner
                      </span>
                    ) : cIsYou ? (
                      <span
                        className="badge"
                        style={{
                          backgroundColor: '#e0e7ff',
                          color: '#4338ca',
                          borderColor: '#c7d2fe',
                          fontWeight: 700,
                          fontSize: '0.75rem'
                        }}
                      >
                        You
                      </span>
                    ) : (
                      <span
                        className="badge"
                        style={{
                          backgroundColor: '#f1f5f9',
                          color: '#475569',
                          borderColor: '#cbd5e1',
                          fontSize: '0.75rem'
                        }}
                      >
                        Collaborator
                      </span>
                    )}

                    {c.status === 'PENDING' && (
                      <span className="badge" style={{ backgroundColor: '#fef3c7', color: '#b45309', fontSize: '0.72rem' }}>
                        Pending
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      </div>
    </div>
  );
}
