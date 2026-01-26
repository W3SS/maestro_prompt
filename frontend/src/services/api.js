import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
})

// Albums
export const getAlbums = () => api.get('/albums')
export const getAlbum = (id) => api.get(`/albums/${id}`)
export const designAlbum = (data) => api.post('/albums/design', data)
export const deleteAlbum = (id) => api.delete(`/albums/${id}`)

// Songs
export const getQueue = () => api.get('/songs/queue')
export const getSong = (id) => api.get(`/songs/${id}`)
export const generateSongs = (trackIds = []) => api.post('/songs/generate', { track_ids: trackIds })
export const updateSongStatus = (id, data) => api.patch(`/songs/${id}/status`, data)

// Archetypes
export const getArchetypes = () => api.get('/archetypes')
export const getArchetype = (id) => api.get(`/archetypes/${id}`)

export default api
