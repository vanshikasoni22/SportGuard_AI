import axios from 'axios';

const BASE_URL = import.meta.env.DEV ? '' : '/_/backend';

const api = axios.create({ baseURL: BASE_URL });

// Inject JWT on every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('sg_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ── Auth ──────────────────────────────────────────────────────────────────────
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (email, password) => {
    const form = new URLSearchParams();
    form.append('username', email);
    form.append('password', password);
    return api.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },
};

// ── Upload ─────────────────────────────────────────────────────────────────────
export const uploadAPI = {
  upload: (file, onProgress) => {
    const form = new FormData();
    form.append('file', file);
    return api.post('/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        if (onProgress) onProgress(Math.round((e.loaded * 100) / e.total));
      },
    });
  },
};

// ── Results ───────────────────────────────────────────────────────────────────
export const resultsAPI = {
  list: () => api.get('/results'),
  get:  (id) => api.get(`/results/${id}`),
};

export default api;
