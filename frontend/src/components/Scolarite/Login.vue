<template>
  <div class="login-wrapper">
    <div class="login-box">
      <h2 class="login-title">Connexion</h2>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div v-if="error" class="text-red-400 text-sm text-center">{{ error }}</div>

        <div>
          <label class="block text-sm font-medium text-gray-300 mb-1">Nom d'utilisateur</label>
          <input
            v-model="username"
            type="text"
            placeholder="ex: ali@ecole.com"
            class="login-input"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-300 mb-1">Mot de passe</label>
          <div class="relative">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="••••••••"
              class="login-input pr-12"
              required
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="password-toggle"
            >
              
            </button>
          </div>
        </div>

        <div class="text-right mt-1 mb-2">
          <a href="#" class="text-blue-400 text-sm hover:underline">Mot de passe oublié ?</a>
        </div>

        <button type="submit" class="login-button">
          <span v-if="!loading">Se connecter</span>
          <span v-else class="loading loading-spinner"></span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const password = ref('')
const error = ref('')
const showPassword = ref(false)
const loading = ref(false)

const handleSubmit = async () => {
  try {
    loading.value = true
    error.value = ''

    const success = await authStore.login(username.value, password.value)
    if (success) {
      router.push('/')
    } else {
      error.value = 'Identifiants invalides'
    }
  } catch (error) {
    console.error('Erreur lors de la connexion:', error)
    error.value = error.response?.data?.detail || 'Erreur lors de la connexion'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(145deg,white, white );
  padding: 2rem;
}

.login-box {
  background: #eaebec;
  padding: 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 0 40px white  ;
  max-width: 420px;
  width: 100%;
  border: 1px solid white;
}

.login-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #2577c9;
  text-align: center;
  margin-bottom: 2rem;
}

.login-input {
  width: 94%;
  padding: 0.75rem 1rem;
  padding-right: 0.5rem; /* espace pour l'icône œil */
  border: 1px solid #475569;
  border-radius: 0.5rem;
  background-color: #475569;
  color: #f1f5f9;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.login-input::placeholder {
  color: #94a3b8;
}

.login-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.password-toggle {
  position: absolute;
  top: 50%;
  right: 0.75rem;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 1rem;
}

.password-toggle:hover {
  color: #f1f5f9;
}

.login-button {
  background-color: #3b82f6;
  color:white ;
  font-weight: 600;
  padding: 0.75rem;
  border-radius: 0.5rem;
  transition: background-color 0.3s;
  width: 100%;
  border: none;
  cursor: pointer;
  margin-top: 1rem;
}

.login-button:hover {
  background-color: #2563eb;
}

.loading-spinner {
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  width: 1rem;
  height: 1rem;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
.forgot-password {
  text-align: right;
  margin-top:  0.75rem;
  margin-bottom: 1.5rem;
}

.forgot-link {
  color: #f0f0f1; /* bleu clair */
  font-size: 0.875rem;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: #f2f4f7; /* bleu plus foncé au survol */
  text-decoration: underline;
}

</style>
