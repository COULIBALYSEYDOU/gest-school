import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../components/Scolarite/Login.vue')
  },
  {
    path: '/',
    name: 'home',
    component: () => import('../components/Scolarite/ClasseList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/classes',
    name: 'classes',
    component: () => import('../components/Scolarite/ClasseList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/classes',
    name: 'classes',
    component: () => import('../components/Scolarite/ClasseList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/etudiants',
    name: 'etudiants',
    component: () => import('../components/Scolarite/EtudiantList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/professeurs',
    name: 'professeurs',
    component: () => import('../components/Scolarite/ProfesseurList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/matieres',
    name: 'matieres',
    component: () => import('../components/Scolarite/MatiereList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/notes',
    name: 'notes',
    component: () => import('../components/Scolarite/NoteList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/bulletins',
    name: 'bulletins',
    component: () => import('../components/Scolarite/Bulletin.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/bulletins/:etudiantId/:semestre',
    name: 'bulletin',
    component: () => import('../components/Scolarite/Bulletin.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/presences',
    name: 'presences',
    component: () => import('../components/Scolarite/PresenceList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/rapports',
    name: 'rapports',
    component: () => import('../components/Scolarite/RapportList.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// Middleware pour la protection des routes
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const authStore = useAuthStore()

  if (requiresAuth && !authStore.token) {
    next('/login')
  } else {
    next()
  }
})

export default router