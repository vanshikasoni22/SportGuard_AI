import React from 'react';
import styles from './ResultCard.module.css';

const STATUS_MAP = {
  Authorized: { label: '✅ Authorized', cls: 'badge-authorized', bar: '#22c55e' },
  Suspicious:  { label: '⚠️ Suspicious',  cls: 'badge-suspicious',  bar: '#f59e0b' },
  'No Match':  { label: '❌ No Match',    cls: 'badge-nomatch',     bar: '#ef4444' },
};

export default function ResultCard({ match, index }) {
  const sim = match.similarity ?? 0;
  const status = STATUS_MAP[match.status] || STATUS_MAP['No Match'];

  return (
    <div
      className={`card ${styles.card} fade-in`}
      style={{ animationDelay: `${index * 60}ms` }}
      id={`result-card-${index}`}
    >
      {/* Header row */}
      <div className={styles.header}>
        <span className={styles.rank}>#{index + 1}</span>
        <span className={`badge ${status.cls}`}>{status.label}</span>
      </div>

      {/* Name */}
      <p className={styles.name} title={match.dataset_name}>
        {match.dataset_name}
      </p>

      {/* Similarity bar */}
      <div className={styles.simRow}>
        <span className={styles.simLabel}>Similarity</span>
        <span className={styles.simValue} style={{ color: status.bar }}>
          {sim.toFixed(1)}%
        </span>
      </div>
      <div className="progress-bar-track">
        <div
          className="progress-bar-fill"
          style={{ width: `${sim}%`, background: status.bar }}
        />
      </div>

      {/* Hamming distance */}
      <div className={styles.metaRow}>
        <span className={styles.metaLabel}>Hamming distance</span>
        <span className={styles.metaValue}>{match.hamming_distance ?? '—'} bits</span>
      </div>
    </div>
  );
}
