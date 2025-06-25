import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import './index.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import { createPinia } from 'pinia'
import { useAuthStore } from './stores/auth'

// Configuration globale d'axios
axios.defaults.baseURL = 'http://localhost:8000/api/'

// Créer l'application et le store Pinia
const app = createApp(App)
const pinia = createPinia()

// Installer les plugins
app.use(router)
app.use(pinia)

// Initialiser le store auth
const authStore = useAuthStore()

// Configuration de l'intercepteur axios pour l'authentification
axios.interceptors.request.use((config) => {
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

// Intercepteur pour le rafraîchissement du token
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        await authStore.refreshToken()
        return axios(originalRequest)
      } catch (refreshError) {
        authStore.logout()
        throw refreshError
      }
    }
    return Promise.reject(error)
  }
)

// Intercepteur pour le rafraîchissement du token
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        await authStore.refreshToken()
        return axios(originalRequest)
      } catch (refreshError) {
        authStore.logout()
        throw refreshError
      }
    }
    return Promise.reject(error)
  }
)

app.mount('#app')