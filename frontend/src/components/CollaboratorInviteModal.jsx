import React from 'react';
import { Users, Check, X, Calendar, AlertCircle, Clock } from 'lucide-react';

export default function CollaboratorInviteModal({
  isOpen,
  requests = [],
  onAccept,
  onDecline,
  onClose,
}) {
  if (!isOpen || requests.length === 0) return null;

  return (
    <div className="modal-overlay" onClick={onClose} style={{ zIndex: 110 }}>
      <div
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: 540, width: '100%', padding: '24px 28px' }}
      >
        {/* Header */}
        <div className="modal-header" style={{ marginBottom: 18, borderBottom: '1px solid #f1f5f9', paddingBottom: 14 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div
              style={{
                width: 40,
                height: 40,
                borderRadius: 10,
                backgroundColor: '#ede9fe',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#7c3aed',
              }}
            >
              <Users size={22} />
            </div>
            <div>
              <h3 style={{ margin: 0, fontSize: '1.2rem', fontWeight: 700, color: '#0f172a' }}>
                Collaboration Invitation
              </h3>
              <p style={{ margin: '2px 0 0 0', fontSize: '0.84rem', color: '#64748b' }}>
                You have {requests.length} pending collaboration {requests.length === 1 ? 'request' : 'requests'}
              </p>
            </div>
          </div>
          <button
            className="modal-close-btn"
            onClick={onClose}
            title="Decide Later"
            style={{
              background: 'transparent',
              border: 'none',
              cursor: 'pointer',
              color: '#94a3b8',
              padding: 6,
              borderRadius: 6,
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Requests List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, maxHeight: '60vh', overflowY: 'auto' }}>
          {requests.map((req) => {
            const senderName = req.creator_username
              ? `@${req.creator_username}`
              : req.creator_gmail || `User #${req.creator_id}`;

            return (
              <div
                key={req.task_id}
                style={{
                  border: '1.5px solid #c7d2fe',
                  borderRadius: 12,
                  padding: '16px 18px',
                  backgroundColor: '#f8faff',
                  boxShadow: '0 2px 8px rgba(99, 102, 241, 0.08)',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 10, marginBottom: 8 }}>
                  <div>
                    <span
                      style={{
                        display: 'inline-block',
                        fontSize: '0.72rem',
                        fontWeight: 700,
                        textTransform: 'uppercase',
                        letterSpacing: '0.04em',
                        color: '#6366f1',
                        backgroundColor: '#e0e7ff',
                        padding: '2px 8px',
                        borderRadius: 4,
                        marginBottom: 6,
                      }}
                    >
                      Task Invitation
                    </span>
                    <h4
                      style={{
                        margin: 0,
                        fontSize: '1.08rem',
                        fontWeight: 700,
                        color: '#1e1b4b',
                        lineHeight: 1.3,
                      }}
                    >
                      {req.title}
                    </h4>
                  </div>
                  <span
                    className="badge"
                    style={{
                      backgroundColor: '#fef3c7',
                      color: '#b45309',
                      fontSize: '0.75rem',
                      fontWeight: 700,
                      padding: '3px 8px',
                    }}
                  >
                    Priority {req.importance}
                  </span>
                </div>

                {/* Sender information banner */}
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 8,
                    fontSize: '0.86rem',
                    color: '#4338ca',
                    backgroundColor: '#eef2ff',
                    padding: '8px 12px',
                    borderRadius: 8,
                    marginTop: 8,
                    marginBottom: 10,
                  }}
                >
                  <Users size={16} />
                  <span>
                    Invited by <strong>{senderName}</strong>
                  </span>
                </div>

                {req.description && (
                  <p
                    style={{
                      fontSize: '0.84rem',
                      color: '#475569',
                      margin: '0 0 10px 0',
                      lineHeight: 1.4,
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden',
                    }}
                  >
                    {req.description}
                  </p>
                )}

                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    flexWrap: 'wrap',
                    gap: 10,
                    paddingTop: 10,
                    borderTop: '1px solid #e0e7ff',
                  }}
                >
                  <div style={{ fontSize: '0.8rem', color: '#64748b', display: 'flex', alignItems: 'center', gap: 5 }}>
                    <Calendar size={14} />
                    <span>Due: {req.due_date ? req.due_date : 'No deadline set'}</span>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <button
                      className="btn btn-sm"
                      onClick={() => onAccept(req.task_id)}
                      style={{
                        backgroundColor: '#10b981',
                        color: '#ffffff',
                        border: 'none',
                        fontWeight: 600,
                        padding: '6px 14px',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: 6,
                        cursor: 'pointer',
                        borderRadius: 6,
                      }}
                    >
                      <Check size={16} />
                      <span>Accept</span>
                    </button>
                    <button
                      className="btn btn-outline btn-sm"
                      onClick={() => onDecline(req.task_id)}
                      style={{
                        borderColor: '#cbd5e1',
                        color: '#64748b',
                        fontWeight: 600,
                        padding: '6px 12px',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: 5,
                        cursor: 'pointer',
                        borderRadius: 6,
                      }}
                    >
                      <X size={16} />
                      <span>Decline</span>
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Modal Footer */}
        <div
          style={{
            marginTop: 18,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: '0.8rem',
            color: '#94a3b8',
            borderTop: '1px solid #f1f5f9',
            paddingTop: 14,
          }}
        >
          <span>You can also manage requests anytime on your Dashboard.</span>
          <button
            type="button"
            className="btn btn-sm btn-outline"
            onClick={onClose}
            style={{ borderColor: '#cbd5e1', color: '#64748b' }}
          >
            Decide Later
          </button>
        </div>
      </div>
    </div>
  );
}
