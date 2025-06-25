import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    refresh_token: localStorage.getItem('refresh_token') || '',
    user: null
  }),

  actions: {
    setToken(access_token: string, refresh_token: string) {
      this.token = access_token
      this.refresh_token = refresh_token
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    },

    clearToken() {
      this.token = ''
      this.refresh_token = ''
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      axios.defaults.headers.common['Authorization'] = ''
    },

    async login(username: string, password: string) {
      try {
        const response = await axios.post('http://localhost:8000/api/token/', {
          username,
          password
        })
        
        // Stocker les tokens
        this.setToken(response.data.access, response.data.refresh)
        return true
      } catch (error) {
        console.error('Erreur lors de la connexion:', error)
        return false
      }
    },

    async logout() {
      this.clearToken()
    },

    async refreshToken() {
      try {
        if (this.refresh_token) {
          const response = await axios.post('http://localhost:8000/api/token/refresh/', {
            refresh: this.refresh_token
          })
          this.setToken(response.data.access, this.refresh_token)
          return true
        }
        return false
      } catch (error) {
        console.error('Erreur lors du rafraîchissement du token:', error)
        return false
      }
    }
  }
})
