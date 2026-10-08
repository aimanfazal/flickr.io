import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
})

export const getRatings   = (params) => api.get('/api/ratings',  { params })
export const getGenres    = (params) => api.get('/api/genres',   { params })
export const getReleases  = (params) => api.get('/api/releases', { params })
export const getTrends    = (params) => api.get('/api/trends',   { params })
export const searchTitles = (q, params) => api.get('/api/search', { params: { q, ...params } })

export async function login(username, password) {
  // OAuth2PasswordRequestForm expects application/x-www-form-urlencoded
  const body = new URLSearchParams({ username, password })
  const { data } = await api.post('/api/auth/login', body)
  return data
}

export default api
