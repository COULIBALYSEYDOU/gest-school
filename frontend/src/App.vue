<template>
  <div id="app">
    <nav v-if="authStore.token">
      <router-link to="/classes">Classes</router-link> |
      <router-link to="/etudiants">Étudiants</router-link> |
      <router-link to="/professeurs">Professeurs</router-link> |
      <router-link to="/matieres">Matières</router-link> |
      <router-link to="/notes">Notes</router-link> |
      <router-link to="/bulletins">Bulletins</router-link> |
      <router-link to="/presences">Présences</router-link>
      <button @click="logout">Déconnexion</button>
    </nav>
    <router-view />
    <router-link to="/rapports">Rapports</router-link>
    <Notification 
      v-if="notification.show"
      :message="notification.message"
      :type="notification.type"
      @close="notification.show = false"
    />
    <Loading v-if="loading" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import Notification from './components/Scolarite/Notification.vue'
import Loading from './components/Scolarite/Loading.vue'

const router = useRouter()
const authStore = useAuthStore()
const notification = ref({
  show: false,
  message: '',
  type: 'success'
})
const loading = ref(false)

const showNotification = (message, type) => {
  notification.value = {
    show: true,
    message,
    type
  }
}

const showLoading = () => {
  loading.value = true
}

const hideLoading = () => {
  loading.value = false
}
    
const logout = () => {
  authStore.logout()
  router.push('/login')
  showNotification('Déconnecté avec succès', 'success')
}

onMounted(() => {
  if (!authStore.token) {
    router.push('/login')
  }
})
</script>

<style>
nav {
  padding: 20px;
  background-color: #f5f5f5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav a {
  margin: 0 10px;
  text-decoration: none;
  color: #333;
}

nav a.router-link-active {
  color: #42b983;
}

button {
  padding: 8px 16px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #cc0000;
}
</style>