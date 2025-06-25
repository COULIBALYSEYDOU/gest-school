import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../components/Scolarite/Login.vue')
  },
  {
    path: '/',
    redirect: '/etudiants'
  },
  {
    path: '/etudiants',
    name: 'etudiants',
    component: () => import('../components/Scolarite/EtudiantList.vue')
  },
  {
    path: '/classes',
    name: 'classes',
    component: () => import('../components/Scolarite/ClasseList.vue')
  },
  {
    path: '/matieres',
    name: 'matieres',
    component: () => import('../components/Scolarite/MatiereList.vue')
  },
  {
    path: '/notes',
    name: 'notes',
    component: () => import('../components/Scolarite/NoteList.vue')
  },
  {
    path: '/professeurs',
    name: 'professeurs',
    component: () => import('../components/Scolarite/ProfesseurList.vue')
  },
  {
    path: '/presences',
    name: 'presences',
    component: () => import('../components/Scolarite/PresenceList.vue')
  },
  {
    path: '/rapports',
    name: 'rapports',
    component: () => import('../components/Scolarite/RapportList.vue')
  },
  {
    path: '/bulletins',
    name: 'bulletins',
    component: () => import('../components/Scolarite/BulletinList.vue')
  }
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
