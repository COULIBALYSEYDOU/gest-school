<template>
  <div v-if="token" class="min-h-screen bg-gray-100">
    <!-- Navbar -->
    <nav class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo et bouton menu mobile -->
          <div class="flex items-center">
            <button 
              @click="isMobileMenuOpen = !isMobileMenuOpen" 
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-500 hover:text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:hidden"
            >
              <span class="sr-only">Ouvrir le menu</span>
              <!-- Icône menu (hamburger) -->
              <svg v-if="!isMobileMenuOpen" class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <!-- Icône fermer (X) -->
              <svg v-else class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <div class="flex-shrink-0 flex items-center">
              <img class="h-8 w-auto" src="@/assets/logo.svg" alt="GestSchool">
            </div>
          </div>
          
          <!-- Menu pour desktop -->
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <router-link 
              v-for="item in menuItems" 
              :key="item.path" 
              :to="item.path"
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200"
              :class="[$route.path === item.path ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700']"
            >
              <span class="flex items-center">
                <component :is="item.icon" class="h-5 w-5 mr-1" />
                {{ item.name }}
              </span>
            </router-link>
          </div>
          
          <!-- Profil et déconnexion -->
          <div class="flex items-center space-x-4">
            <div class="relative">
              <button 
                @click="isProfileMenuOpen = !isProfileMenuOpen"
                class="flex items-center space-x-2 text-gray-500 hover:text-gray-700 focus:outline-none"
              >
                <div class="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center text-white font-semibold">
                  {{ userInitials }}
                </div>
                <span class="hidden md:block">Mon profil</span>
                <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              <!-- Menu déroulant du profil -->
              <div 
                v-if="isProfileMenuOpen" 
                class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50"
              >
                <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Mon compte</a>
                <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Paramètres</a>
                <button @click="logout" class="w-full text-left block px-4 py-2 text-sm text-red-600 hover:bg-gray-100">
                  Déconnexion
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Menu mobile -->
      <div 
        v-if="isMobileMenuOpen" 
        class="sm:hidden transition-all duration-300 ease-in-out"
      >
        <div class="pt-2 pb-3 space-y-1">
          <router-link 
            v-for="item in menuItems" 
            :key="item.path" 
            :to="item.path"
            class="flex items-center px-3 py-2 text-base font-medium rounded-md transition-colors duration-200"
            :class="[$route.path === item.path ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']"
            @click="isMobileMenuOpen = false"
          >
            <component :is="item.icon" class="h-5 w-5 mr-3" />
            {{ item.name }}
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100">
      <div class="container mx-auto px-4 py-8">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const token = ref(localStorage.getItem('token'))
const isMobileMenuOpen = ref(false)
const isProfileMenuOpen = ref(false)

// Icônes SVG pour le menu (composants fonctionnels)
const ClassIcon = () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'h-5 w-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4' })
])

const StudentIcon = () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'h-5 w-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z' })
])

const SubjectIcon = () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'h-5 w-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' })
])

const GradeIcon = () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'h-5 w-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01' })
])

const TeacherIcon = () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'h-5 w-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' })
])

const AttendanceIcon = () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'h-5 w-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4' })
])

const ReportIcon = () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', class: 'h-5 w-5' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })
])

// Éléments du menu avec leurs icônes
const menuItems = [
  { name: 'Classes', path: '/classes', icon: ClassIcon },
  { name: 'Étudiants', path: '/etudiants', icon: StudentIcon },
  { name: 'Matières', path: '/matieres', icon: SubjectIcon },
  { name: 'Notes', path: '/notes', icon: GradeIcon },
  { name: 'Professeurs', path: '/professeurs', icon: TeacherIcon },
  { name: 'Présences', path: '/presences', icon: AttendanceIcon },
  { name: 'Rapports', path: '/rapports', icon: ReportIcon }
]

// Initiales de l'utilisateur pour l'avatar (à remplacer par les données réelles de l'utilisateur)
const userInitials = computed(() => {
  // Simuler les initiales de l'utilisateur (à remplacer par les données réelles)
  return 'AD' // Par exemple pour "Admin"
})

// Fermer les menus si on clique en dehors
const handleClickOutside = (event) => {
  if (isProfileMenuOpen.value && !event.target.closest('.profile-menu')) {
    isProfileMenuOpen.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(() => {
  if (!token.value) {
    router.push('/login')
  }
  
  // Ajouter un écouteur pour fermer les menus en cliquant en dehors
  document.addEventListener('click', handleClickOutside)
})

// Nettoyer les écouteurs d'événements
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Animation pour le menu mobile */
.sm\:hidden {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-in-out;
}

.sm\:hidden.open {
  max-height: 500px;
}

/* Animation pour les liens du menu */
.router-link-active {
  position: relative;
}

/* Effet de survol sur les éléments du menu */
.hover\:bg-gray-50:hover {
  transition: background-color 0.2s ease;
}

/* Animation pour le menu déroulant du profil */
.origin-top-right {
  transform-origin: top right;
  animation: dropdown 0.2s ease-out;
}

@keyframes dropdown {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>
