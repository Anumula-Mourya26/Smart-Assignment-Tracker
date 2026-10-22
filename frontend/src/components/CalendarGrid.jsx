import React, { useState } from 'react';
import {
  ChevronLeft,
  ChevronRight,
  Calendar as CalendarIcon,
  Star,
  CheckCircle2,
  Clock,
  ArrowRight,
  Flame,
  Layers,
  AlertCircle
} from 'lucide-react';

export default function CalendarGrid({ tasks = [], calendarData = {}, onOpenTask }) {
  const today = new Date();
  const [currentYear, setCurrentYear] = useState(today.getFullYear());
  const [currentMonth, setCurrentMonth] = useState(today.getMonth()); // 0-indexed: 0=Jan, 11=Dec
  const [selectedDayTasks, setSelectedDayTasks] = useState(null);
  const [selectedDateStr, setSelectedDateStr] = useState(null);

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const years = [2024, 2025, 2026, 2027, 2028, 2029, 2030];
  const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  // Navigation handlers
  const handlePrevMonth = () => {
    if (currentMonth === 0) {
      setCurrentMonth(11);
      setCurrentYear((prev) => prev - 1);
    } else {
      setCurrentMonth((prev) => prev - 1);
    }
    setSelectedDayTasks(null);
  };

  const handleNextMonth = () => {
    if (currentMonth === 11) {
      setCurrentMonth(0);
      setCurrentYear((prev) => prev + 1);
    } else {
      setCurrentMonth((prev) => prev + 1);
    }
    setSelectedDayTasks(null);
  };

  const handleToday = () => {
    setCurrentYear(today.getFullYear());
    setCurrentMonth(today.getMonth());
    setSelectedDayTasks(null);
  };

  // Days in month logic
  const daysInCurrentMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const firstDayWeekday = new Date(currentYear, currentMonth, 1).getDay(); // 0 for Sunday
  const daysInPrevMonth = new Date(currentYear, currentMonth, 0).getDate();

  // Create grid cells (previous padding + current days + next padding)
  const cells = [];

  // Padding from previous month
  for (let i = firstDayWeekday - 1; i >= 0; i--) {
    cells.push({
      day: daysInPrevMonth - i,
      month: currentMonth - 1,
      year: currentMonth === 0 ? currentYear - 1 : currentYear,
      isCurrentMonth: false,
    });
  }

  // Days of current month
  for (let day = 1; day <= daysInCurrentMonth; day++) {
    cells.push({
      day,
      month: currentMonth,
      year: currentYear,
      isCurrentMonth: true,
    });
  }

  // Padding for remaining cells in 6-row (42 cells) or 5-row (35 cells) grid
  const remainingCells = (7 - (cells.length % 7)) % 7;
  for (let day = 1; day <= remainingCells; day++) {
    cells.push({
      day,
      month: currentMonth + 1,
      year: currentMonth === 11 ? currentYear + 1 : currentYear,
      isCurrentMonth: false,
    });
  }

  // Workload intensity styling helper
  const getWorkloadStyle = (score) => {
    if (!score || score <= 0) return null;
    if (score <= 3) {
      return {
        bg: '#eff6ff',
        border: '#bfdbfe',
        badgeBg: '#dbeafe',
        badgeText: '#1e40af',
        label: 'Low',
      };
    }
    if (score <= 6) {
      return {
        bg: '#f5f3ff',
        border: '#ddd6fe',
        badgeBg: '#ede9fe',
        badgeText: '#6d28d9',
        label: 'Medium',
      };
    }
    return {
      bg: '#fdf2f8',
      border: '#fbcfe8',
      badgeBg: '#fce7f3',
      badgeText: '#be185d',
      label: 'High',
    };
  };

  const formatIsoDate = (year, month, day) => {
    const m = String(month + 1).padStart(2, '0');
    const d = String(day).padStart(2, '0');
    return `${year}-${m}-${d}`;
  };

  const todayIsoStr = formatIsoDate(today.getFullYear(), today.getMonth(), today.getDate());

  const handleCellClick = (cellDateStr, dayTasks) => {
    setSelectedDateStr(cellDateStr);
    const sorted = [...dayTasks].sort(
      (a, b) => (Number(b.importance) || 0) - (Number(a.importance) || 0)
    );
    setSelectedDayTasks(sorted);
  };

  return (
    <div className="calendar-grid-wrapper" style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      {/* Top Header: Controls (Month, Year, Prev/Next, Today) */}
      <div className="panel" style={{ padding: '18px 24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <button
                className="btn btn-outline btn-sm"
                onClick={handlePrevMonth}
                title="Previous Month"
                style={{ padding: '8px 10px' }}
              >
                <ChevronLeft size={16} />
              </button>
              <button
                className="btn btn-outline btn-sm"
                onClick={handleNextMonth}
                title="Next Month"
                style={{ padding: '8px 10px' }}
              >
                <ChevronRight size={16} />
              </button>
            </div>

            <button
              className="btn btn-outline btn-sm"
              onClick={handleToday}
              style={{ fontWeight: 600, padding: '7px 14px' }}
            >
              Today
            </button>

            {/* Month Selector Dropdown */}
            <select
              value={currentMonth}
              onChange={(e) => {
                setCurrentMonth(Number(e.target.value));
                setSelectedDayTasks(null);
              }}
              style={{
                padding: '8px 14px',
                borderRadius: 8,
                border: '1px solid #cbd5e1',
                fontWeight: 600,
                fontSize: '0.95rem',
                backgroundColor: '#ffffff',
                cursor: 'pointer'
              }}
            >
              {months.map((m, idx) => (
                <option key={m} value={idx}>
                  {m}
                </option>
              ))}
            </select>

            {/* Year Selector Dropdown */}
            <select
              value={currentYear}
              onChange={(e) => {
                setCurrentYear(Number(e.target.value));
                setSelectedDayTasks(null);
              }}
              style={{
                padding: '8px 14px',
                borderRadius: 8,
                border: '1px solid #cbd5e1',
                fontWeight: 600,
                fontSize: '0.95rem',
                backgroundColor: '#ffffff',
                cursor: 'pointer'
              }}
            >
              {years.map((y) => (
                <option key={y} value={y}>
                  {y}
                </option>
              ))}
            </select>
          </div>

          {/* Workload Legend */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 14, fontSize: '0.8rem', color: '#64748b' }}>
            <span style={{ fontWeight: 600 }}>Workload Intensity:</span>
            <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
              <span style={{ width: 10, height: 10, borderRadius: 3, background: '#3b82f6' }} /> Low (1-3)
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
              <span style={{ width: 10, height: 10, borderRadius: 3, background: '#8b5cf6' }} /> Med (4-6)
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
              <span style={{ width: 10, height: 10, borderRadius: 3, background: '#ec4899' }} /> High (7+)
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: 5, color: '#dc2626', fontWeight: 600 }}>
              <span style={{ width: 10, height: 10, borderRadius: 3, background: '#ef4444' }} /> Overdue (Past Deadline)
            </span>
          </div>
        </div>
      </div>

      {/* Main Grid View */}
      <div className="panel" style={{ padding: '20px 24px', overflowX: 'auto' }}>
        <div style={{ minWidth: 700 }}>
          {/* Day of Week Header */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(7, 1fr)',
              gap: 8,
              marginBottom: 10,
              textAlign: 'center',
              fontWeight: 700,
              fontSize: '0.85rem',
              color: '#475569',
              textTransform: 'uppercase',
              letterSpacing: '0.05em'
            }}
          >
            {daysOfWeek.map((d) => (
              <div key={d} style={{ padding: '8px 0' }}>
                {d}
              </div>
            ))}
          </div>

          {/* Days Grid Cells */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(7, 1fr)',
              gap: 8
            }}
          >
            {cells.map((cell, idx) => {
              const dateStr = formatIsoDate(cell.year, cell.month, cell.day);
              const dayTasks = tasks
                .filter((t) => t.due_date === dateStr)
                .sort((a, b) => (Number(b.importance) || 0) - (Number(a.importance) || 0));
              const workloadScore = calendarData[dateStr] || dayTasks.reduce((acc, t) => acc + (Number(t.importance) || 0), 0);
              const workloadStyle = getWorkloadStyle(workloadScore);
              const hasOverdueTasks = dayTasks.some((t) => !t.completed && dateStr < todayIsoStr);

              const isTodayCell =
                cell.year === today.getFullYear() &&
                cell.month === today.getMonth() &&
                cell.day === today.getDate();

              const isSelected = selectedDateStr === dateStr;

              return (
                <div
                  key={`${dateStr}-${idx}`}
                  onClick={() => handleCellClick(dateStr, dayTasks)}
                  style={{
                    minHeight: 96,
                    padding: '8px 10px',
                    borderRadius: 10,
                    border: isSelected
                      ? (hasOverdueTasks ? '2px solid #ef4444' : '2px solid #6366f1')
                      : hasOverdueTasks
                      ? '1.5px solid #f87171'
                      : workloadStyle
                      ? `1.5px solid ${workloadStyle.border}`
                      : '1px solid #e2e8f0',
                    backgroundColor: hasOverdueTasks
                      ? '#fff5f5'
                      : workloadStyle
                      ? workloadStyle.bg
                      : (cell.isCurrentMonth ? '#ffffff' : '#f8fafc'),
                    opacity: cell.isCurrentMonth ? 1 : 0.45,
                    cursor: dayTasks.length > 0 ? 'pointer' : 'default',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    transition: 'all 0.15s ease',
                    boxShadow: isSelected
                      ? (hasOverdueTasks ? '0 0 0 3px rgba(239, 68, 68, 0.15)' : '0 0 0 3px rgba(99, 102, 241, 0.15)')
                      : 'none'
                  }}
                  onMouseEnter={(e) => {
                    if (cell.isCurrentMonth) e.currentTarget.style.transform = 'translateY(-2px)';
                  }}
                  onMouseLeave={(e) => {
                    if (cell.isCurrentMonth) e.currentTarget.style.transform = 'translateY(0)';
                  }}
                >
                  {/* Cell Top Row: Date Number and Workload Score Pill */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                      <span
                        style={{
                          fontWeight: isTodayCell ? 800 : 600,
                          fontSize: '0.88rem',
                          color: isTodayCell ? '#ffffff' : (cell.isCurrentMonth ? '#1e293b' : '#94a3b8'),
                          backgroundColor: isTodayCell ? '#6366f1' : 'transparent',
                          width: isTodayCell ? 24 : 'auto',
                          height: isTodayCell ? 24 : 'auto',
                          borderRadius: '50%',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        {cell.day}
                      </span>
                      {hasOverdueTasks && (
                        <span
                          style={{
                            width: 7,
                            height: 7,
                            borderRadius: '50%',
                            backgroundColor: '#ef4444',
                            display: 'inline-block',
                          }}
                          title="Contains uncompleted overdue tasks"
                        />
                      )}
                    </div>

                    {workloadScore > 0 && (
                      <span
                        className="badge"
                        style={{
                          backgroundColor: hasOverdueTasks ? '#fee2e2' : workloadStyle.badgeBg,
                          color: hasOverdueTasks ? '#b91c1c' : workloadStyle.badgeText,
                          fontSize: '0.7rem',
                          fontWeight: 700,
                          padding: '2px 6px',
                          display: 'flex',
                          alignItems: 'center',
                          gap: 3
                        }}
                        title={`Workload score: ${workloadScore}`}
                      >
                        <Flame size={10} fill="currentColor" />
                        {workloadScore}
                      </span>
                    )}
                  </div>

                  {/* Task Pills on this Day */}
                  <div style={{ marginTop: 6, display: 'flex', flexDirection: 'column', gap: 4 }}>
                    {dayTasks.slice(0, 2).map((t) => {
                      const isOverdue = !t.completed && dateStr < todayIsoStr;
                      return (
                        <div
                          key={t.task_id}
                          onClick={(e) => {
                            e.stopPropagation();
                            onOpenTask(t);
                          }}
                          style={{
                            fontSize: '0.72rem',
                            fontWeight: 600,
                            color: isOverdue ? '#991b1b' : '#334155',
                            backgroundColor: isOverdue
                              ? '#fee2e2'
                              : t.completed
                              ? '#e2e8f0'
                              : '#ffffff',
                            padding: '2px 6px',
                            borderRadius: 4,
                            border: isOverdue
                              ? '1px solid #f87171'
                              : '1px solid #cbd5e1',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: 4
                          }}
                          title={`${t.title}${isOverdue ? ' (Overdue uncompleted)' : ''}`}
                        >
                          {isOverdue ? (
                            <AlertCircle size={10} color="#dc2626" style={{ flexShrink: 0 }} />
                          ) : (
                            <span style={{ color: '#f59e0b', flexShrink: 0 }}>★{t.importance}</span>
                          )}
                          <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{t.title}</span>
                          {isOverdue && (
                            <span style={{ color: '#dc2626', fontSize: '0.62rem', fontWeight: 700, marginLeft: 'auto', flexShrink: 0 }}>
                              Overdue
                            </span>
                          )}
                        </div>
                      );
                    })}

                    {dayTasks.length > 2 && (
                      <div style={{ fontSize: '0.68rem', color: hasOverdueTasks ? '#dc2626' : '#64748b', fontWeight: 600, textAlign: 'right' }}>
                        +{dayTasks.length - 2} more
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Selected Day Tasks Preview Drawer / Section */}
      {selectedDateStr && (
        <div className="panel" style={{ padding: '20px 24px' }}>
          <div className="panel-header" style={{ marginBottom: 14 }}>
            <h3 className="panel-title" style={{ fontSize: '1.05rem', fontWeight: 700 }}>
              <CalendarIcon size={18} color="#6366f1" />
              <span>Tasks Due on {selectedDateStr}</span>
            </h3>
            <span className="panel-badge">
              {selectedDayTasks ? selectedDayTasks.length : 0} tasks
            </span>
          </div>

          {selectedDayTasks && selectedDayTasks.length > 0 ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 12 }}>
              {selectedDayTasks.map((task) => {
                const isOverdue = !task.completed && selectedDateStr < todayIsoStr;
                return (
                  <div
                    key={task.task_id}
                    style={{
                      padding: '12px 16px',
                      borderRadius: 8,
                      border: isOverdue ? '1.5px solid #fca5a5' : '1px solid #e2e8f0',
                      backgroundColor: isOverdue ? '#fff5f5' : '#ffffff',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}
                  >
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
                        <span style={{ fontWeight: 600, fontSize: '0.92rem', color: isOverdue ? '#991b1b' : '#0f172a' }}>
                          {task.title}
                        </span>
                        {isOverdue && (
                          <span
                            className="badge"
                            style={{
                              backgroundColor: '#fee2e2',
                              color: '#dc2626',
                              borderColor: '#fca5a5',
                              fontSize: '0.68rem',
                              fontWeight: 700,
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: 3
                            }}
                          >
                            <AlertCircle size={10} />
                            Overdue
                          </span>
                        )}
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 4, fontSize: '0.78rem', color: '#64748b' }}>
                        <span style={{ color: '#f59e0b', fontWeight: 600 }}>Priority {task.importance}</span>
                        <span>•</span>
                        <span style={{ color: task.completed ? '#10b981' : isOverdue ? '#dc2626' : '#64748b', fontWeight: isOverdue ? 600 : 400 }}>
                          {task.completed ? 'Completed' : isOverdue ? 'Uncompleted (Past Deadline)' : 'Pending'}
                        </span>
                      </div>
                    </div>
                  <button
                    className="btn btn-outline btn-sm"
                    onClick={() => onOpenTask(task)}
                    style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}
                  >
                    <span>View</span>
                    <ArrowRight size={14} />
                  </button>
                </div>
              );
            })}
            </div>
          ) : (
            <div style={{ color: '#64748b', fontSize: '0.88rem' }}>
              No tasks scheduled for this day.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
