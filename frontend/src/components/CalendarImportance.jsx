import React from 'react';
import { Calendar, TrendingUp } from 'lucide-react';

export default function CalendarImportance({ calendarData, isLoading }) {
  const dateEntries = Object.entries(calendarData || {}).sort((a, b) =>
    a[0].localeCompare(b[0])
  );

  // Find max importance to calculate relative progress bar fill
  const maxImportance = dateEntries.length > 0
    ? Math.max(...dateEntries.map(([, score]) => Number(score) || 0), 1)
    : 1;

  return (
    <div className="panel" style={{ marginTop: '24px' }}>
      <div className="panel-header">
        <h3 className="panel-title">
          <Calendar size={18} color="#4f46e5" />
          <span>Calendar Workload</span>
        </h3>
        <span className="panel-badge">{dateEntries.length} Dates</span>
      </div>

      {isLoading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '24px 0' }}>
          <div className="spinner spinner-dark" />
        </div>
      ) : dateEntries.length > 0 ? (
        <div style={{ overflowX: 'auto' }}>
          <table className="calendar-summary-table">
            <thead>
              <tr>
                <th>Due Date</th>
                <th>Workload Intensity</th>
                <th style={{ textAlign: 'right' }}>Score</th>
              </tr>
            </thead>
            <tbody>
              {dateEntries.map(([date, score]) => {
                const numericScore = Number(score) || 0;
                const percentage = Math.min(100, Math.round((numericScore / maxImportance) * 100));
                return (
                  <tr key={date}>
                    <td>
                      <span className="calendar-date-badge">
                        <Calendar size={14} color="#64748b" />
                        <span>{date}</span>
                      </span>
                    </td>
                    <td>
                      <div className="importance-bar-wrapper">
                        <div className="importance-bar-bg">
                          <div
                            className="importance-bar-fill"
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <span className="importance-score-pill">
                        {numericScore}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state">
          <TrendingUp size={36} className="empty-icon" />
          <h4>No Dated Deadlines</h4>
          <p>Create tasks with due dates to analyze daily importance workloads.</p>
        </div>
      )}
    </div>
  );
}
