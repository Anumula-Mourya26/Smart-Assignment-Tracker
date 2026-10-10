import React, { useState } from 'react';
import { BookOpen, Eye, EyeOff, AlertCircle, Check } from 'lucide-react';
import { api } from '../services/api';

export default function Login({ onLoginSuccess, onNavigateToRegister }) {
  const [gmail, setGmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e?.preventDefault?.();
    setError('');
    setSuccess('');

    const trimmedGmail = gmail.trim();
    if (!trimmedGmail || !password) {
      setError('Both Email and password are required.');
      return;
    }

    if (!trimmedGmail.endsWith('@gmail.com')) {
      setError('Email must end with @gmail.com');
      return;
    }

    setIsLoading(true);
    try {
      const data = await api.login(trimmedGmail, password);
      setSuccess('Login successful! Redirecting to workspace...');

      localStorage.setItem('user_id', String(data.user_id));
      localStorage.setItem('user_email', data.gmail || trimmedGmail);
      if (data.username) {
        localStorage.setItem('user_username', data.username);
      } else {
        localStorage.removeItem('user_username');
      }

      setTimeout(() => {
        onLoginSuccess({
          userId: Number(data.user_id),
          gmail: data.gmail || trimmedGmail,
          username: data.username || '',
        });
      }, 500);
    } catch (err) {
      setError(err.message || 'Invalid Gmail or password. Please try again.');
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
            YOUR GATEWAY TO ACADEMIC EXCELLENCE
          </h1>
          <p className="landing-subtitle">
            Ready to conquer your semester? Log in now and let Smart Assignment Tracker organize your deadlines, priorities, and collaborations.
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
            {/* Email Field */}
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
                Email
              </label>
              <input
                type="email"
                className="landing-input"
                placeholder="Input email (e.g. student@gmail.com)"
                value={gmail}
                onChange={(e) => setGmail(e.target.value)}
                required
                disabled={isLoading}
                autoFocus
              />
            </div>

            {/* Password Field with Eye Toggle */}
            <div style={{ marginBottom: 12 }}>
              <label
                style={{
                  display: 'block',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  color: '#1e293b',
                  marginBottom: 6,
                }}
              >
                Password
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

            {/* Link to Register */}
            <div style={{ fontSize: '0.88rem', color: '#475569', marginBottom: 12 }}>
              New to Assignment Tracker?{' '}
              <button
                type="button"
                className="landing-inline-link"
                onClick={onNavigateToRegister}
              >
                Create an Account
              </button>
            </div>

            {/* Remember Me & Forgot Password Row */}
            <div className="landing-sub-row">
              <label
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 8,
                  cursor: 'pointer',
                  userSelect: 'none',
                }}
              >
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  style={{ width: 16, height: 16, cursor: 'pointer', accentColor: '#111a14' }}
                />
                <span>Remember me</span>
              </label>

              <button
                type="button"
                className="landing-inline-link"
                style={{ fontSize: '0.86rem', color: '#64748b', textDecoration: 'none' }}
                onClick={() => alert('To reset your credentials, please register a new student account or contact the system administrator.')}
              >
                Forgot your password?
              </button>
            </div>

            {/* Main Dark Login Button */}
            <button
              type="submit"
              className="landing-btn-dark"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <div className="spinner" />
                  <span>Signing in...</span>
                </>
              ) : (
                <span>Login - Continue Exploring and Planning</span>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
