import React, { useState, useEffect, useCallback } from 'react';
import Navbar from '../components/Navbar';
import UploadPanel from '../components/UploadPanel';
import ResultCard from '../components/ResultCard';
import SimilarityChart from '../components/SimilarityChart';
import { resultsAPI } from '../services/api';
import styles from './Dashboard.module.css';

const STATUS_MAP = {
  Authorized: { icon: '✅', color: '#22c55e', bg: 'rgba(34,197,94,0.12)' },
  Suspicious:  { icon: '⚠️', color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
  'No Match':  { icon: '❌', color: '#ef4444', bg: 'rgba(239,68,68,0.12)' },
};

export default function Dashboard({ user, onLogout }) {
  const [currentResult, setCurrentResult] = useState(null);
  const [history,       setHistory]       = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  // Fetch upload history on mount
  const fetchHistory = useCallback(async () => {
    setLoadingHistory(true);
    try {
      const { data } = await resultsAPI.list();
      setHistory(data);
    } catch {
      // silently ignore
    } finally {
      setLoadingHistory(false);
    }
  }, []);

  useEffect(() => { fetchHistory(); }, [fetchHistory]);

  // When a new upload result arrives
  const handleResult = (result) => {
    setCurrentResult(result);
    setHistory((prev) => [result, ...prev]);
  };

  const topStatus = currentResult
    ? (STATUS_MAP[currentResult.top_status] || STATUS_MAP['No Match'])
    : null;

  return (
    <div className={styles.page}>
      <Navbar user={user} onLogout={onLogout} />

      <main className={`container ${styles.main}`}>

        {/* ── Page header ─────────────────────────────────────── */}
        <div className={styles.pageHeader}>
          <div>
            <h1 className={styles.pageTitle}>
              Media <span className="gradient-text">Fingerprint</span> Dashboard
            </h1>
            <p className={styles.pageSub}>
              Upload sports media to detect unauthorized copies and modified content
            </p>
          </div>
          <div className={styles.statsRow}>
            {[
              { label: 'Total Scans',   value: history.length },
              { label: 'Authorized',    value: history.filter(h => h.top_status === 'Authorized').length },
              { label: 'Suspicious',    value: history.filter(h => h.top_status === 'Suspicious').length },
            ].map((s) => (
              <div key={s.label} className={`card ${styles.statCard}`}>
                <span className={styles.statValue}>{s.value}</span>
                <span className={styles.statLabel}>{s.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* ── Two-column layout ────────────────────────────────── */}
        <div className={styles.grid}>

          {/* LEFT — Upload */}
          <div className={styles.leftCol}>
            <div className={`card ${styles.panel}`}>
              <div className={styles.panelHeader}>
                <div className={styles.panelDot} />
                <h2 className={styles.panelTitle}>Upload Media</h2>
              </div>
              <UploadPanel onResult={handleResult} />
            </div>

            {/* Result summary card */}
            {currentResult && topStatus && (
              <div
                className={`card ${styles.summaryCard} fade-in`}
                style={{ borderColor: topStatus.color, background: topStatus.bg }}
                id="result-summary"
              >
                <div className={styles.summaryIcon}>{topStatus.icon}</div>
                <div className={styles.summaryBody}>
                  <p className={styles.summaryStatus} style={{ color: topStatus.color }}>
                    {currentResult.top_status}
                  </p>
                  <p className={styles.summaryText}>
                    Best match: <strong>{currentResult.top_similarity?.toFixed(1)}%</strong> similarity
                  </p>
                  <p className={styles.summaryHash}>
                    pHash: <code>{currentResult.phash}</code>
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* RIGHT — Results */}
          <div className={styles.rightCol}>
            {/* Chart */}
            {currentResult?.matches?.length > 0 && (
              <SimilarityChart matches={currentResult.matches} />
            )}

            {/* Match grid */}
            {currentResult?.matches?.length > 0 ? (
              <>
                <div className={styles.sectionHeader}>
                  <h2 className={styles.sectionTitle}>Match Results</h2>
                  <span className={styles.sectionSub}>
                    {currentResult.matches.length} dataset entries compared
                  </span>
                </div>
                <div className={styles.matchGrid}>
                  {currentResult.matches.map((m, i) => (
                    <ResultCard key={i} match={m} index={i} />
                  ))}
                </div>
              </>
            ) : (
              <div className={`card ${styles.emptyRight}`}>
                <div className={styles.emptyIcon}>🔍</div>
                <p className={styles.emptyTitle}>No scan results yet</p>
                <p className={styles.emptySub}>Upload an image or video to begin fingerprint analysis</p>
              </div>
            )}
          </div>
        </div>

        {/* ── Scan history ─────────────────────────────────────── */}
        {history.length > 0 && (
          <div className={styles.historySection}>
            <div className={styles.sectionHeader}>
              <h2 className={styles.sectionTitle}>Scan History</h2>
              <button
                className="btn btn-ghost"
                style={{ fontSize: 13, padding: '6px 14px' }}
                onClick={fetchHistory}
                id="refresh-history-btn"
              >
                ↻ Refresh
              </button>
            </div>
            <div className={styles.historyTable}>
              <div className={styles.historyHeader}>
                <span>File</span><span>Type</span><span>Top Match %</span><span>Status</span><span>Time</span>
              </div>
              {history.slice(0, 20).map((h, i) => {
                const s = STATUS_MAP[h.top_status] || STATUS_MAP['No Match'];
                return (
                  <div key={h.id || i} className={styles.historyRow} id={`history-row-${i}`}>
                    <span className={styles.hFile}>{h.filename}</span>
                    <span className={styles.hType}>{h.media_type}</span>
                    <span className={styles.hSim} style={{ color: s.color }}>
                      {h.top_similarity?.toFixed(1)}%
                    </span>
                    <span className={`badge ${
                      h.top_status === 'Authorized' ? 'badge-authorized' :
                      h.top_status === 'Suspicious' ? 'badge-suspicious' : 'badge-nomatch'
                    }`} style={{ fontSize: 10 }}>
                      {s.icon} {h.top_status}
                    </span>
                    <span className={styles.hTime}>
                      {new Date(h.uploaded_at).toLocaleTimeString()}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
