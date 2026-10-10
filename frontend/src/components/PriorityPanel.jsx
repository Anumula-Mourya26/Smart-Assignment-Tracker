import React from 'react';
import { Flame, Star, Calendar, CheckCircle2, Clock, ArrowRight } from 'lucide-react';

export default function PriorityPanel({ priorityTask, isLoading, onOpenTask }) {
  return (
    <div className="panel">
      <div className="panel-header">
        <h3 className="panel-title">
          <Flame size={18} color="#ef4444" />
          <span>Highest Priority Task</span>
        </h3>
        {priorityTask && (
          <span className="badge badge-imp-5">Top Priority</span>
        )}
      </div>

      {isLoading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '24px 0' }}>
          <div className="spinner spinner-dark" />
        </div>
      ) : priorityTask ? (
        <div 
          className="priority-highlight-card"
          onClick={() => onOpenTask && onOpenTask(priorityTask)}
          style={{ cursor: onOpenTask ? 'pointer' : 'default', transition: 'transform 0.15s ease' }}
        >
          <div className="priority-badge-flair">
            <Star size={12} fill="currentColor" />
            Rank 1 • Importance {priorityTask.importance}/5
          </div>

          <h4 className="priority-title">{priorityTask.title}</h4>
          {priorityTask.description && (
            <p className="priority-desc">{priorityTask.description}</p>
          )}

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 12 }}>
            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', fontSize: '0.8rem', color: '#64748b' }}>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                <Calendar size={14} />
                {priorityTask.due_date ? `Due: ${priorityTask.due_date}` : 'No due date set'}
              </span>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                <Clock size={14} />
                Status: {priorityTask.completed ? 'Completed' : 'Pending Action'}
              </span>
            </div>

            {onOpenTask && (
              <span style={{ fontSize: '0.78rem', fontWeight: 600, color: '#6366f1', display: 'inline-flex', alignItems: 'center', gap: 3 }}>
                <span>Open</span>
                <ArrowRight size={13} />
              </span>
            )}
          </div>
        </div>
      ) : (
        <div className="empty-state">
          <CheckCircle2 size={36} className="empty-icon" color="#10b981" />
          <h4>All Caught Up!</h4>
          <p>No pending incomplete tasks found. You're completely up to date.</p>
        </div>
      )}
    </div>
  );
}
