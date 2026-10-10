import React from 'react';
import { LayoutDashboard, CheckSquare, Calendar, LogOut, CheckCircle2 } from 'lucide-react';

export default function Sidebar({ currentTab, onTabSelect, isTaskDetailOpen, user, onLogout }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'tasks', label: 'My Tasks', icon: CheckSquare },
    { id: 'calendar', label: 'Calendar', icon: Calendar },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="brand-icon">
          <CheckCircle2 size={22} />
        </div>
        <div className="brand-text">
          <h1>Smart Assignment Tracker</h1>
          <span className="brand-badge">Academic Edition</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          // Only show active highlight if matching tab and NOT currently drill-down inside a task detail
          const isActive = currentTab === item.id && !isTaskDetailOpen;
          return (
            <button
              key={item.id}
              className={`nav-link ${isActive ? 'active' : ''}`}
              onClick={() => onTabSelect(item.id)}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        {user && (
          <div className="user-profile-badge">
            <div className="user-avatar">
              {user.username ? user.username.charAt(0).toUpperCase() : (user.gmail ? user.gmail.charAt(0).toUpperCase() : 'U')}
            </div>
            <div className="user-details">
              <div className="user-email-text" title={user.username ? `@${user.username} (${user.gmail})` : user.gmail}>
                {user.username ? `@${user.username}` : user.gmail}
              </div>
              <div className="user-id-text">{user.username ? user.gmail : `User #${user.userId}`}</div>
            </div>
          </div>
        )}

        <button className="logout-btn" onClick={onLogout}>
          <LogOut size={16} />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}
