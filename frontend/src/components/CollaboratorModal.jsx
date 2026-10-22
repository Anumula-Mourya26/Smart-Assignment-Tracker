import React, { useState, useEffect } from 'react';
import { X, UserPlus, Users, AlertCircle, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

export default function CollaboratorModal({ isOpen, onClose, task, onCollaboratorAdded }) {
  const [collaborators, setCollaborators] = useState([]);
  const [collabUserId, setCollabUserId] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    if (isOpen && task) {
      loadCollaborators();
      setError('');
      setSuccess('');
      setCollabUserId('');
    }
  }, [isOpen, task]);

  const loadCollaborators = async () => {
    if (!task) return;
    setIsLoading(true);
    try {
      const ids = await api.getCollaborators(task.task_id);
      setCollaborators(ids);
    } catch (err) {
      setError('Failed to fetch collaborators.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddCollaborator = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const targetId = Number(collabUserId);
    if (!targetId || targetId <= 0) {
      setError('Please enter a valid positive User ID.');
      return;
    }

    if (targetId === task.creator_id) {
      setError('Task creator is already the owner of this task.');
      return;
    }

    setIsSubmitting(true);
    try {
      await api.addCollaborator(task.task_id, targetId, 'PENDING');
      setSuccess(`Collaboration request sent to User #${targetId}! They will receive a popup invitation.`);
      setCollabUserId('');
      await loadCollaborators();
      if (onCollaboratorAdded) {
        onCollaboratorAdded();
      }
    } catch (err) {
      setError(err.message || 'Failed to add collaborator.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen || !task) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <h3>Task Collaboration</h3>
            <p style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '2px' }}>
              Task #{task.task_id}: "{task.title}"
            </p>
          </div>
          <button className="modal-close-btn" onClick={onClose} disabled={isSubmitting}>
            <X size={20} />
          </button>
        </div>

        {error && (
          <div className="alert alert-danger">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="alert alert-success">
            <CheckCircle2 size={18} />
            <span>{success}</span>
          </div>
        )}

        {/* Existing Collaborators Section */}
        <div style={{ marginBottom: 20 }}>
          <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <Users size={15} />
            <span>Current Collaborator User IDs:</span>
          </label>

          {isLoading ? (
            <div style={{ padding: '8px 0' }}>
              <div className="spinner spinner-dark" style={{ width: 16, height: 16 }} />
            </div>
          ) : collaborators.length > 0 ? (
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 6 }}>
              {collaborators.map((id) => (
                <span
                  key={id}
                  style={{
                    backgroundColor: '#eef2ff',
                    color: '#4f46e5',
                    padding: '4px 10px',
                    borderRadius: 999,
                    fontSize: '0.8rem',
                    fontWeight: 600,
                    border: '1px solid #c7d2fe',
                  }}
                >
                  User #{id}
                </span>
              ))}
            </div>
          ) : (
            <p style={{ fontSize: '0.82rem', color: '#94a3b8', fontStyle: 'italic', marginTop: 4 }}>
              No collaborators assigned to this task yet.
            </p>
          )}
        </div>

        {/* Add Collaborator Form */}
        <form onSubmit={handleAddCollaborator}>
          <div className="form-group">
            <label className="form-label">
              Add Collaborator by User ID <span className="required">*</span>
            </label>
            <div style={{ display: 'flex', gap: 8 }}>
              <input
                type="number"
                min="1"
                className="form-control"
                placeholder="e.g. 2"
                value={collabUserId}
                onChange={(e) => setCollabUserId(e.target.value)}
                required
                disabled={isSubmitting}
              />
              <button
                type="submit"
                className="btn btn-primary"
                disabled={isSubmitting}
                style={{ flexShrink: 0 }}
              >
                {isSubmitting ? (
                  <div className="spinner" />
                ) : (
                  <>
                    <UserPlus size={16} />
                    <span>Add</span>
                  </>
                )}
              </button>
            </div>
            <p className="form-hint">
              Enter the numeric ID of another registered user to grant them access to this task.
            </p>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Done
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
