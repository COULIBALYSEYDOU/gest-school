<template>
  <div class="scolarite-container">
    <!-- Header avec Titre et Bouton Ajouter -->
    <header class="header">
      <h1>
        <i class="fas fa-file-alt" aria-hidden="true"></i> Bulletins
      </h1>
    </header>

    <!-- Section Table -->
    <section class="classes-table">
      <!-- Barre de recherche et filtres -->
      <div class="search-container">
        <select v-model="selectedSemestre" class="search-filter">
          <option value="">Tous les semestres</option>
          <option value="1">Semestre 1</option>
          <option value="2">Semestre 2</option>
        </select>
        <select v-model="selectedClasse" class="search-filter">
          <option value="">Toutes les classes</option>
          <option v-for="classe in classes" :key="classe.id" :value="classe.id">
            {{ classe.nom }}
          </option>
        </select>
        <input type="text" v-model="searchTerm" placeholder="Rechercher un étudiant..." class="search-input" />
      </div>

      <!-- Liste des étudiants -->
      <div class="bulletin-list">
        <div v-for="etudiant in filteredEtudiants" :key="etudiant.id" class="bulletin-card">
          <div class="bulletin-header">
            <h2>{{ etudiant.user.last_name }} {{ etudiant.user.first_name }}</h2>
            <div class="bulletin-actions">
              <button @click="generateBulletin(etudiant.id, selectedSemestre)" class="btn-generate">
                <i class="fas fa-file-pdf"></i> Générer PDF
              </button>
              <button @click="viewBulletin(etudiant.id, selectedSemestre)" class="btn-view">
                <i class="fas fa-eye"></i> Voir
              </button>
            </div>
          </div>
          <div class="bulletin-content">
            <div class="bulletin-info">
              <p>Classe: {{ etudiant.classe?.nom }}</p>
              <p>Semestre: {{ selectedSemestre }}</p>
              <p>Moyenne générale: {{ etudiant.moyenne_generale || 'N/A' }}</p>
            </div>
            <div class="bulletin-moyennes">
              <div v-for="moyenne in etudiant.moyennes" :key="moyenne.matiere" class="moyenne-item">
                <span class="moyenne-label">{{ moyenne.matiere }}</span>
                <span class="moyenne-value">{{ moyenne.note }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">← Précédent</button>
        <span>Page {{ currentPage }} sur {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Suivant →</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// États
const route = useRoute()
const selectedSemestre = ref(route.params.semestre || '')
const selectedClasse = ref('')
const searchTerm = ref('')
const currentPage = ref(1)
const pageSize = 10

const etudiants = ref([])
const classes = ref([])
const loading = ref(false)
const error = ref(null)

// Calculs
const totalPages = computed(() => Math.ceil(filteredEtudiants.value.length / pageSize))

const filteredEtudiants = computed(() => {
  return etudiants.value
    .filter(etudiant => {
      const nom = `${etudiant.user.last_name} ${etudiant.user.first_name}`.toLowerCase()
      const classe = etudiant.classe?.nom?.toLowerCase() || ''
      return (
        nom.includes(searchTerm.value.toLowerCase()) ||
        classe.includes(searchTerm.value.toLowerCase()) ||
        (selectedClasse.value ? etudiant.classe?.id === parseInt(selectedClasse.value) : true)
      )
    })
    .slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
})

// Méthodes API
const fetchClasses = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await axios.get('http://localhost:8000/api/classes/')
    classes.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la récupération des classes'
    console.error('Erreur:', err)
  } finally {
    loading.value = false
  }
}

const fetchEtudiants = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await axios.get('http://localhost:8000/api/etudiants/')
    etudiants.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la récupération des étudiants'
    console.error('Erreur:', err)
  } finally {
    loading.value = false
  }
}

// Méthode pour récupérer les notes d'un étudiant
const fetchNotesByStudent = async (etudiantId, semestre) => {
  try {
    loading.value = true
    error.value = null
    const response = await axios.get(`http://localhost:8000/api/etudiant/${etudiantId}/notes/${semestre}/`)
    const notes = response.data
    
    // Calculer les moyennes par matière
    const moyennes = {}
    let totalNotes = 0
    let totalCoefficients = 0

    notes.forEach(note => {
      const matiere = note.matiere.nom
      if (!moyennes[matiere]) {
        moyennes[matiere] = {
          note: note.note,
          coefficient: note.matiere.coefficient
        }
        totalNotes += note.note * note.matiere.coefficient
        totalCoefficients += note.matiere.coefficient
      }
    })

    // Trouver l'étudiant correspondant
    const etudiant = etudiants.value.find(e => e.id === parseInt(etudiantId))
    if (etudiant) {
      etudiant.moyennes = Object.entries(moyennes).map(([matiere, data]) => ({
        matiere,
        note: data.note,
        coefficient: data.coefficient
      }))
      
      // Calculer la moyenne générale
      etudiant.moyenne_generale = totalCoefficients > 0 ? (totalNotes / totalCoefficients).toFixed(2) : 'N/A'
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la récupération des notes'
    console.error('Erreur:', err)
  } finally {
    loading.value = false
  }
}

// Méthode pour générer le PDF
const generateBulletin = async (etudiantId, semestre) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/etudiant/${etudiantId}/bulletin/${semestre}/pdf/`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `bulletin_${etudiantId}_${semestre}.pdf`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la génération du PDF'
    console.error('Erreur:', err)
  }
}

// Méthode pour afficher le bulletin
const viewBulletin = async (etudiantId, semestre) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/etudiant/${etudiantId}/bulletin/${semestre}/`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    window.open(url, '_blank')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de l\'affichage du bulletin'
    console.error('Erreur:', err)
  }
}

// Actions de pagination
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

// Chargement initial des données
onMounted(() => {
  fetchClasses()
  fetchEtudiants()
})

// Watch pour les changements de route
watch(() => route.params, (newParams) => {
  if (newParams.semestre) {
    selectedSemestre.value = newParams.semestre
  }
  if (newParams.etudiantId) {
    fetchNotesByStudent(newParams.etudiantId, newParams.semestre)
  }
})
</script>

<style scoped>
.bulletin-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.bulletin-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.bulletin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.bulletin-actions {
  display: flex;
  gap: 10px;
}

.btn-generate, .btn-view {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.3s ease;
}

.btn-generate {
  background-color: #2563eb;
  color: white;
}

.btn-generate:hover {
  background-color: #1d4ed8;
}

.btn-view {
  background-color: #10b981;
  color: white;
}

.btn-view:hover {
  background-color: #059669;
}

.bulletin-content {
  display: grid;
  gap: 15px;
}

.bulletin-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bulletin-moyennes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
}

.moyenne-item {
  display: flex;
  justify-content: space-between;
  padding: 8px;
  background: #f8fafc;
  border-radius: 6px;
}

.moyenne-label {
  font-weight: 500;
  color: #374151;
}

.moyenne-value {
  font-weight: 600;
  color: #111827;
}

/* Styles existants conservés */
.scolarite-container {
  padding: 30px;
  background: #f9fafb;
  font-family: 'Segoe UI', sans-serif;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  font-weight: bold;
  color: #1f2937;
}

.classes-table {
  background: white;
}

.search-container {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.search-filter {
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  margin-right: 10px;
  transition: border 0.3s ease;
}

.search-filter:focus {
  border-color: #2563eb;
  outline: none;
}

.search-input {
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  width: 220px;
  transition: border 0.3s ease;
}

.search-input:focus {
  border-color: #2563eb;
  outline: none;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 16px;
  border: none;
  background: #034fe9;
  border-radius: 6px;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
