import React, { useState } from 'react';
import { authAPI } from '../services/api';
import styles from './LoginPage.module.css';

export default function LoginPage({ onAuth }) {
  const [mode,     setMode]     = useState('login');   // 'login' | 'register'
  const [name,     setName]     = useState('');
  const [email,    setEmail]    = useState('');
  const [password, setPassword] = useState('');
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      let res;
      if (mode === 'register') {
        res = await authAPI.register({ name, email, password });
      } else {
        res = await authAPI.login(email, password);
      }
      const { access_token, user } = res.data;
      localStorage.setItem('sg_token', access_token);
      localStorage.setItem('sg_user',  JSON.stringify(user));
      onAuth(user);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      {/* Background orbs */}
      <div className={styles.orb1} />
      <div className={styles.orb2} />

      <div className={`card ${styles.card} fade-in`}>
        {/* Logo */}
        <div className={styles.logoRow}>
          <svg width="36" height="36" viewBox="0 0 28 28" fill="none">
            <circle cx="14" cy="14" r="13" stroke="#00e5ff" strokeWidth="2"/>
            <path d="M8 14 L14 8 L20 14 L14 20 Z" fill="#00e5ff" opacity="0.85"/>
            <circle cx="14" cy="14" r="3" fill="#00e5ff"/>
          </svg>
          <span className={styles.logoText}>
            Sport<span className={styles.accent}>Guard</span> AI
          </span>
        </div>

        <h1 className={styles.heading}>
          {mode === 'login' ? 'Welcome back' : 'Create account'}
        </h1>
        <p className={styles.sub}>
          {mode === 'login'
            ? 'Sign in to your media tracking dashboard'
            : 'Start protecting your sports media today'}
        </p>

        <form onSubmit={submit} className={styles.form} id="auth-form">
          {mode === 'register' && (
            <div className={styles.field}>
              <label className={styles.label}>Full Name</label>
              <input
                id="input-name"
                className="input"
                placeholder="John Smith"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
          )}

          <div className={styles.field}>
            <label className={styles.label}>Email</label>
            <input
              id="input-email"
              className="input"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label}>Password</label>
            <input
              id="input-password"
              className="input"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
            />
          </div>

          {error && <p className={styles.error}>{error}</p>}

          <button
            id="auth-submit-btn"
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', marginTop: 8 }}
            disabled={loading}
          >
            {loading
              ? <><span className="spinner" /> Processing…</>
              : mode === 'login' ? 'Sign In' : 'Create Account'
            }
          </button>
        </form>

        {/* Toggle */}
        <p className={styles.toggle}>
          {mode === 'login' ? "Don't have an account? " : 'Already have an account? '}
          <button
            id="auth-toggle-btn"
            className={styles.toggleBtn}
            onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError(''); }}
            type="button"
          >
            {mode === 'login' ? 'Sign up' : 'Sign in'}
          </button>
        </p>

        {/* Demo hint */}
        <div className={styles.demoHint}>
          <span>🚀 Demo:</span> register any email to get started instantly
        </div>
      </div>
    </div>
  );
}
