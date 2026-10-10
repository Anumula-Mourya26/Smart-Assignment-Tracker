import React from 'react';
import { Plus, Mail } from 'lucide-react';

export default function Header({ user, onOpenCreateModal }) {
  return (
    <header className="top-header">
      <div className="header-left">
        <h2>Productivity Workspace</h2>
        <p className="header-subtitle">
          {user?.username ? `Welcome back, @${user.username}` : (user?.gmail ? `Welcome back, ${user.gmail}` : 'Welcome to your Smart Assignment Tracker')}
        </p>
      </div>

      <div className="header-actions">
        <button className="btn btn-primary" onClick={onOpenCreateModal}>
          <Plus size={18} />
          <span>Create Task</span>
        </button>
      </div>
    </header>
  );
}
