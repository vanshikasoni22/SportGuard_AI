import React, { useCallback, useState } from 'react';
import styles from './UploadPanel.module.css';
import { uploadAPI } from '../services/api';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function UploadPanel({ onResult }) {
  const [dragging, setDragging] = useState(false);
  const [loading,  setLoading]  = useState(false);
  const [progress, setProgress] = useState(0);
  const [preview,  setPreview]  = useState(null);
  const [error,    setError]    = useState('');

  const handleFile = useCallback(async (file) => {
    if (!file) return;
    setError('');

    // Preview
    const url = URL.createObjectURL(file);
    setPreview({ url, type: file.type.startsWith('video') ? 'video' : 'image', name: file.name });

    // Upload
    setLoading(true);
    setProgress(0);
    try {
      const { data } = await uploadAPI.upload(file, setProgress);
      onResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Upload failed. Please try again.');
    } finally {
      setLoading(false);
      setProgress(0);
    }
  }, [onResult]);

  const onDrop = useCallback((e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const onInputChange = (e) => {
    const file = e.target.files[0];
    if (file) handleFile(file);
  };

  return (
    <div className={styles.wrapper}>
      {/* Drop zone */}
      <label
        className={`${styles.dropzone} ${dragging ? styles.dragging : ''} ${loading ? styles.loading : ''}`}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        id="upload-dropzone"
      >
        <input
          type="file"
          accept="image/*,video/*"
          onChange={onInputChange}
          className={styles.hiddenInput}
          id="file-input"
          disabled={loading}
        />

        {loading ? (
          <div className={styles.loadingState}>
            <div className={`${styles.scanRing} pulse`} />
            <p className={styles.loadingText}>Fingerprinting media…</p>
            <div className="progress-bar-track" style={{ width: 220 }}>
              <div
                className="progress-bar-fill"
                style={{ width: `${progress}%`, background: '#00e5ff' }}
              />
            </div>
            <span className={styles.progressPct}>{progress}%</span>
          </div>
        ) : preview ? (
          <div className={styles.previewState}>
            {preview.type === 'image'
              ? <img src={preview.url} alt="preview" className={styles.previewImg} />
              : <video src={preview.url} className={styles.previewImg} muted />
            }
            <div className={styles.previewOverlay}>
              <span>📂 Drop a new file to re-scan</span>
            </div>
          </div>
        ) : (
          <div className={styles.emptyState}>
            <div className={styles.uploadIcon}>
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#00e5ff" strokeWidth="1.5">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
            </div>
            <p className={styles.uploadTitle}>Drop media here or <span className={styles.browse}>browse</span></p>
            <p className={styles.uploadSub}>Supports JPG, PNG, MP4, MOV, AVI · Max 100 MB</p>
          </div>
        )}
      </label>

      {error && <p className={styles.error}>{error}</p>}
    </div>
  );
}
