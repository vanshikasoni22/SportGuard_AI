import React from 'react';
import styles from './Navbar.module.css';

export default function Navbar({ user, onLogout }) {
  return (
    <nav className={styles.nav}>
      <div className={styles.inner}>
        {/* Logo */}
        <div className={styles.logo}>
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <circle cx="14" cy="14" r="13" stroke="#00e5ff" strokeWidth="2"/>
            <path d="M8 14 L14 8 L20 14 L14 20 Z" fill="#00e5ff" opacity="0.8"/>
            <circle cx="14" cy="14" r="3" fill="#00e5ff"/>
          </svg>
          <span className={styles.logoText}>Sport<span className={styles.logoAccent}>Guard</span> AI</span>
        </div>

        {/* Right side */}
        <div className={styles.right}>
          {user && (
            <>
              <div className={styles.userPill}>
                <div className={styles.avatar}>
                  {(user.name || user.email || 'U')[0].toUpperCase()}
                </div>
                <span className={styles.userName}>{user.name || user.email}</span>
              </div>
              <button className="btn btn-ghost" onClick={onLogout} id="logout-btn">
                Sign out
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
