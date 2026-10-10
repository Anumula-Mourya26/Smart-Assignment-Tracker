import React, { useState } from 'react';
import { BookOpen, Eye, EyeOff, AlertCircle, Check, ArrowRight, UserPlus } from 'lucide-react';
import { api } from '../services/api';

export default function Register({ onNavigateToLogin, onRegisterSuccess }) {
  const [username, setUsername] = useState('');
  const [gmail, setGmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const trimmedGmail = gmail.trim();
    if (!trimmedGmail) {
      setError('Email address is required.');
      return;
    }

    if (!trimmedGmail.endsWith('@gmail.com')) {
      setError('Email address must end with @gmail.com');
      return;
    }

    if (!password) {
      setError('Password is required.');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match. Please re-enter.');
      return;
    }

    setIsLoading(true);
    try {
      await api.register(trimmedGmail, password, username.trim());
      setSuccess('Account created successfully! Redirecting to login...');
      setTimeout(() => {
        onRegisterSuccess ? onRegisterSuccess(trimmedGmail) : onNavigateToLogin();
      }, 700);
    } catch (err) {
      setError(err.message || 'Registration failed. Please try a different email.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="landing-frame">
        {/* Left Column: Visual Artwork & Inspirational Banner */}
        <div className="landing-visual-col">
          {/* Main Top Card: Study Desk & Books & To-do Workspace */}
          <div className="landing-main-image-card">
            <div className="landing-image-tag">
              <BookOpen size={14} />
              <span>Smart Assignment Tracker</span>
            </div>
            <img
              src="/study_todo_workspace.jpg"
              alt="Aesthetic student study desk with books and to-do list"
            />
          </div>

          {/* Bottom Card: Atmospheric University Library with Text Overlay */}
          <div className="landing-banner-card">
            <img
              src="/study_library_banner.jpg"
              alt="Grand university library bookshelves"
            />
            <div className="landing-banner-overlay">
              <h2 className="landing-banner-text">
                WHETHER YOU'RE CRUNCHING MIDTERMS, MANAGING ASSIGNMENTS, OR COLLABORATING ON PROJECTS, YOUR ACADEMIC SUCCESS STARTS HERE.
              </h2>
            </div>
          </div>
        </div>

        {/* Right Column: Clean White Form Card */}
        <div className="landing-form-card">
          <h1 className="landing-title">
            START YOUR JOURNEY TO TOP GRADES
          </h1>
          <p className="landing-subtitle">
            Create your account to organize assignments, track workload, and collaborate with classmates.
          </p>

          {error && (
            <div className="alert alert-danger" style={{ marginBottom: 16 }}>
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          )}

          {success && (
            <div className="alert alert-success" style={{ marginBottom: 16 }}>
              <Check size={18} />
              <span>{success}</span>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {/* Optional Username Field */}
            <div style={{ marginBottom: 14 }}>
              <label
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  color: '#1e293b',
                  marginBottom: 6,
                }}
              >
                <span>Username</span>
                <span style={{ color: '#64748b', fontWeight: 400, fontSize: '0.8rem' }}>Optional</span>
              </label>
              <input
                type="text"
                className="landing-input"
                placeholder="Choose a username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={isLoading}
                autoFocus
              />
            </div>

            {/* Gmail Field */}
            <div style={{ marginBottom: 14 }}>
              <label
                style={{
                  display: 'block',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  color: '#1e293b',
                  marginBottom: 6,
                }}
              >
                Gmail Address <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <input
                type="email"
                className="landing-input"
                placeholder="student@gmail.com"
                value={gmail}
                onChange={(e) => setGmail(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>

            {/* Password Field with Eye Toggle */}
            <div style={{ marginBottom: 14 }}>
              <label
                style={{
                  display: 'block',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  color: '#1e293b',
                  marginBottom: 6,
                }}
              >
                Password <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <div className="landing-input-wrap">
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="landing-input"
                  placeholder="••••••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={isLoading}
                  style={{ paddingRight: 44 }}
                />
                <button
                  type="button"
                  className="landing-password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  title={showPassword ? 'Hide password' : 'Show password'}
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* Confirm Password Field with Eye Toggle */}
            <div style={{ marginBottom: 16 }}>
              <label
                style={{
                  display: 'block',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  color: '#1e293b',
                  marginBottom: 6,
                }}
              >
                Confirm Password <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <div className="landing-input-wrap">
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  className="landing-input"
                  placeholder="••••••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  disabled={isLoading}
                  style={{ paddingRight: 44 }}
                />
                <button
                  type="button"
                  className="landing-password-toggle"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  title={showConfirmPassword ? 'Hide password' : 'Show password'}
                  tabIndex={-1}
                >
                  {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* Link to Login */}
            <div style={{ fontSize: '0.88rem', color: '#475569', marginBottom: 16 }}>
              Already have an account?{' '}
              <button
                type="button"
                className="landing-inline-link"
                onClick={onNavigateToLogin}
              >
                Sign in
              </button>
            </div>

            {/* Main Dark Register Button */}
            <button
              type="submit"
              className="landing-btn-dark"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <div className="spinner" />
                  <span>Creating Account...</span>
                </>
              ) : (
                <span>Register - Begin Your Academic Journey</span>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
