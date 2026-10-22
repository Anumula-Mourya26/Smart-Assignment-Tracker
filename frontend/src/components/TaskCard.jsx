import React from 'react';
import { Calendar, Clock, Star, ArrowRight, CheckCircle2, ListChecks, AlertCircle } from 'lucide-react';

export default function TaskCard({ task, onOpenTask, currentUserId }) {
  const getImportanceBadgeClass = (importance) => {
    switch (importance) {
      case 5: return 'badge-imp-5';
      case 4: return 'badge-imp-4';
      case 3: return 'badge-imp-3';
      case 2: return 'badge-imp-2';
      default: return 'badge-imp-1';
    }
  };

  const isOwner = currentUserId && task.creator_id === currentUserId;
  const ownerLabel = isOwner ? 'You' : (task.creator_username || task.creator_gmail || `User #${task.creator_id}`);

  const todayObj = new Date();
  const todayStr = `${todayObj.getFullYear()}-${String(todayObj.getMonth() + 1).padStart(2, '0')}-${String(todayObj.getDate()).padStart(2, '0')}`;
  const isOverdue = !task.completed && task.due_date && task.due_date < todayStr;

  const totalSubs = Number(task.subtasks_total) || 0;
  const doneSubs = Number(task.subtasks_completed) || 0;
  const progressPercent = totalSubs > 0 
    ? Math.round((doneSubs / totalSubs) * 100) 
    : (task.completed ? 100 : 0);

  return (
    <div 
      className={`task-card clickable ${task.completed ? 'completed' : ''} ${isOverdue ? 'overdue' : ''}`}
      onClick={() => onOpenTask(task)}
      style={{
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        borderColor: isOverdue ? '#fca5a5' : undefined,
        backgroundColor: isOverdue ? '#fffbfb' : undefined,
      }}
    >
      <div className="task-card-header">
        <div className="task-title-group" style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div className="task-icon-status">
            {task.completed ? (
              <CheckCircle2 size={20} color="#10b981" />
            ) : (
              <ListChecks size={20} color="#6366f1" />
            )}
          </div>
          <span className="task-title">{task.title}</span>
        </div>

        <div className="task-header-badges">
          <span className={`badge ${getImportanceBadgeClass(task.importance)}`}>
            <Star size={12} fill="currentColor" />
            Priority {task.importance}
          </span>
        </div>
      </div>

      {task.description && (
        <p className="task-description">{task.description}</p>
      )}

      {/* Task Progress based on subtasks marked as done */}
      <div className="task-subtask-progress-box" style={{ margin: '12px 0 10px 0' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.78rem', color: '#64748b', marginBottom: 4 }}>
          <span>
            {totalSubs > 0 ? (
              <span>Subtasks: <strong>{doneSubs}/{totalSubs}</strong> done</span>
            ) : (
              <span>Progress: {task.completed ? '100%' : '0%'}</span>
            )}
          </span>
          <span style={{ fontWeight: 600, color: progressPercent === 100 ? '#10b981' : '#6366f1' }}>
            {progressPercent}%
          </span>
        </div>
        <div style={{ height: 6, background: '#f1f5f9', borderRadius: 999, overflow: 'hidden' }}>
          <div 
            style={{ 
              height: '100%', 
              width: `${progressPercent}%`, 
              background: progressPercent === 100 ? '#10b981' : 'linear-gradient(90deg, #6366f1, #8b5cf6)',
              borderRadius: 999,
              transition: 'width 0.3s ease'
            }} 
          />
        </div>
      </div>

      <div className="task-meta-footer">
        <div className="task-meta-left" style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 8 }}>
          {/* Owner badge: 'You' in green or 'Username' in yellow */}
          {isOwner ? (
            <span 
              className="badge" 
              style={{ 
                backgroundColor: '#dcfce7', 
                color: '#15803d', 
                borderColor: '#86efac', 
                fontWeight: 600,
                padding: '3px 8px'
              }}
            >
              Owner: You
            </span>
          ) : (
            <span 
              className="badge" 
              style={{ 
                backgroundColor: '#fef9c3', 
                color: '#854d0e', 
                borderColor: '#fde047', 
                fontWeight: 600,
                padding: '3px 8px'
              }}
            >
              Owner: {ownerLabel}
            </span>
          )}

          {task.completed ? (
            <span className="badge badge-status completed">Completed</span>
          ) : isOverdue ? (
            <span
              className="badge badge-status"
              style={{
                backgroundColor: '#fee2e2',
                color: '#dc2626',
                borderColor: '#fca5a5',
                display: 'inline-flex',
                alignItems: 'center',
                gap: 4,
                fontWeight: 700
              }}
            >
              <AlertCircle size={12} />
              Pending (Overdue)
            </span>
          ) : (
            <span
              className="badge badge-status"
              style={{
                backgroundColor: '#eff6ff',
                color: '#2563eb',
                borderColor: '#bfdbfe',
                display: 'inline-flex',
                alignItems: 'center',
                gap: 4,
                fontWeight: 600
              }}
            >
              <Clock size={12} />
              Active
            </span>
          )}

          {task.due_date ? (
            <span className="badge-date">
              <Calendar size={13} />
              Due: {task.due_date}
            </span>
          ) : (
            <span className="badge-date" style={{ color: '#94a3b8' }}>
              <Clock size={13} />
              No due date
            </span>
          )}
        </div>

        <div className="task-meta-right">
          <button
            className="btn btn-outline btn-sm"
            onClick={(e) => {
              e.stopPropagation();
              onOpenTask(task);
            }}
            title="Open Task"
            style={{ display: 'flex', alignItems: 'center', gap: 4 }}
          >
            <span>View Task</span>
            <ArrowRight size={14} />
          </button>
        </div>
      </div>
    </div>
  );
}
