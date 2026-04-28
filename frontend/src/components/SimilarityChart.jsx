import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale, LinearScale,
  BarElement, Title, Tooltip, Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import styles from './SimilarityChart.module.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const STATUS_COLORS = {
  Authorized: 'rgba(34,197,94,0.75)',
  Suspicious:  'rgba(245,158,11,0.75)',
  'No Match':  'rgba(239,68,68,0.75)',
};

const STATUS_BORDERS = {
  Authorized: '#22c55e',
  Suspicious:  '#f59e0b',
  'No Match':  '#ef4444',
};

export default function SimilarityChart({ matches }) {
  if (!matches || matches.length === 0) return null;

  const top = matches.slice(0, 8);

  const data = {
    labels: top.map((m) =>
      m.dataset_name.length > 18 ? m.dataset_name.slice(0, 16) + '…' : m.dataset_name
    ),
    datasets: [
      {
        label: 'Similarity %',
        data: top.map((m) => m.similarity),
        backgroundColor: top.map((m) => STATUS_COLORS[m.status] || STATUS_COLORS['No Match']),
        borderColor:     top.map((m) => STATUS_BORDERS[m.status] || STATUS_BORDERS['No Match']),
        borderWidth: 1,
        borderRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: 'rgba(8,11,18,0.95)',
        borderColor: 'rgba(255,255,255,0.08)',
        borderWidth: 1,
        titleColor: '#f0f4f8',
        bodyColor: '#8b9ab0',
        callbacks: {
          label: (ctx) => ` ${ctx.raw.toFixed(1)}% similarity`,
        },
      },
    },
    scales: {
      x: {
        ticks: { color: '#8b9ab0', font: { size: 11 } },
        grid:  { color: 'rgba(255,255,255,0.04)' },
      },
      y: {
        min: 0, max: 100,
        ticks: { color: '#8b9ab0', font: { size: 11 }, callback: (v) => v + '%' },
        grid:  { color: 'rgba(255,255,255,0.06)' },
      },
    },
  };

  return (
    <div className={`card ${styles.chartCard}`}>
      <div className={styles.header}>
        <h3 className={styles.title}>Similarity Distribution</h3>
        <span className={styles.sub}>Top {top.length} matches</span>
      </div>
      <div className={styles.chartWrap}>
        <Bar data={data} options={options} />
      </div>
    </div>
  );
}
