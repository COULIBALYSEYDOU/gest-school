<template>
  <div class="scolarite-container">
    <!-- Header avec Titre et Bouton Ajouter -->
    <header class="header">
      <h1>
      <i class="fas fa-sticky-note" aria-hidden="true"></i> Gestion des Notes
      </h1>
      <button class="btn-add" @click="openCreateModal">
        <i class="fas fa-plus-circle"></i> Ajouter une note
      </button>
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
        <select v-model="selectedType" class="search-filter">
          <option value="">Tous les types</option>
          <option value="DEVOIR">Devoir</option>
          <option value="CONTROLE">Contrôle</option>
          <option value="EXAMEN">Examen</option>
        </select>
        <select v-model="selectedMatiere" class="search-filter">
          <option value="">Toutes les matières</option>
          <option v-for="matiere in matieres" :key="matiere.id" :value="matiere.id">
            {{ matiere.nom }}
          </option>
        </select>
        <input type="text" v-model="searchTerm" placeholder="Rechercher par étudiant ou matière..." class="search-input" />
      </div>

      <!-- Tableau des notes -->
      <table>
        <thead>
          <tr>
            <th>Étudiant</th>
            <th>Matière</th>
            <th>Note</th>
            <th>Type</th>
            <th>Semestre</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="note in filteredNotes" :key="note.id">
            <td>{{ note.etudiant?.user?.last_name }} {{ note.etudiant?.user?.first_name }}</td>
            <td>{{ note.matiere?.nom }}</td>
            <td>{{ note.note }}</td>
            <td>{{ note.type }}</td>
            <td>{{ note.semestre }}</td>
            <td>{{ formatDate(note.date) }}</td>
            <td>
               <div class="actions">
                 <button @click="openEditModal(note)" class="btn-edit">
                   <i class="fas fa-edit"></i>
                 </button>
                 <button @click="deleteNote(note.id)" class="btn-delete">
                   <i class="fas fa-trash-alt"></i>
                 </button>
                 <template v-if="note.semestre">
                   <router-link :to="{ name: 'bulletin', params: { etudiantId: note.etudiant.id, semestre: note.semestre } }" class="btn-bulletin">
                     <i class="fas fa-file-alt"></i>
                   </router-link>
                 </template>
                 <template v-else>
                   <span class="text-gray-500">Aucun semestre</span>
                 </template>
               </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">← Précédent</button>
        <span>Page {{ currentPage }} sur {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Suivant →</button>
      </div>
    </section>

    <!-- Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2 class="modal-title">{{ isEditing ? 'Modifier' : 'Ajouter' }} une note</h2>
        <form @submit.prevent="saveNote">
          <div class="form-group">
            <label>Étudiant</label>
            <select v-model="currentNote.etudiant" required>
              <option v-for="etudiant in etudiants" :key="etudiant.id" :value="etudiant.id">
                {{ etudiant.user.last_name }} {{ etudiant.user.first_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Matière</label>
            <select v-model="currentNote.matiere" required>
              <option v-for="matiere in matieres" :key="matiere.id" :value="matiere.id">
                {{ matiere.nom }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Type de note</label>
            <select v-model="currentNote.type" required>
              <option value="DEVOIR">Devoir</option>
              <option value="CONTROLE">Contrôle</option>
              <option value="EXAMEN">Examen</option>
            </select>
          </div>
          <div class="form-group">
            <label>Semestre</label>
            <select v-model="currentNote.semestre" required>
              <option value="1">Semestre 1</option>
              <option value="2">Semestre 2</option>
            </select>
          </div>
          <div class="form-group">
            <label>Note</label>
            <input v-model="currentNote.note" type="number" step="0.01" min="0" max="20" required>
          </div>
          <div class="form-group">
            <label>Date</label>
            <input v-model="currentNote.date" type="date" required>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-submit">
              {{ isEditing ? 'Enregistrer' : 'Créer' }}
            </button>
            <button @click="closeModal" type="button" class="btn-cancel">Annuler</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// Configuration axios avec token
axios.defaults.headers.common['Authorization'] = `Bearer ${authStore.token}`

const selectedSemestre = ref('')
const selectedClasse = ref('')
const searchTerm = ref('')
const currentPage = ref(1)
const pageSize = 10

const classes = ref([])
const etudiants = ref([])
const matieres = ref([])
const notes = ref([])

// Computed properties
const totalPages = computed(() => Math.ceil(filteredNotes.value.length / pageSize))

const filteredNotes = computed(() => {
  return notes.value.filter(note => {
    const etudiant = etudiants.value.find(e => e.id === note.etudiant)
    const matiere = matieres.value.find(m => m.id === note.matiere)
    
    return (
      (!selectedSemestre.value || note.semestre === parseInt(selectedSemestre.value)) &&
      (!selectedClasse.value || etudiant?.classe?.id === parseInt(selectedClasse.value)) &&
      (etudiant?.user?.last_name?.toLowerCase()?.includes(searchTerm.value.toLowerCase()) ||
       etudiant?.user?.first_name?.toLowerCase()?.includes(searchTerm.value.toLowerCase()) ||
       matiere?.nom?.toLowerCase()?.includes(searchTerm.value.toLowerCase()))
    )
  }).slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
})

// API calls
const fetchClasses = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/classes/')
    classes.value = response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des classes:', error)
    if (error.response?.status === 401) {
      console.error('Accès non autorisé. Vérifiez votre token d\'authentification.')
    }
  }
}

const fetchEtudiants = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/etudiants/')
    etudiants.value = response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des étudiants:', error)
    if (error.response?.status === 401) {
      console.error('Accès non autorisé. Vérifiez votre token d\'authentification.')
    }
  }
}

const fetchMatieres = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/matieres/')
    matieres.value = response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des matières:', error)
    if (error.response?.status === 401) {
      console.error('Accès non autorisé. Vérifiez votre token d\'authentification.')
    }
  }
}

const fetchNotes = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/notes/')
    notes.value = response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des notes:', error)
    if (error.response?.status === 401) {
      console.error('Accès non autorisé. Vérifiez votre token d\'authentification.')
    }
  }
}

const fetchBulletin = async (etudiantId, semestre) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/bulletin/${etudiantId}/${semestre}/`)
    return response.data
  } catch (error) {
    console.error('Erreur lors de la récupération du bulletin:', error)
    if (error.response?.status === 401) {
      console.error('Accès non autorisé. Vérifiez votre token d\'authentification.')
    }
    return null
  }
}

// Actions
const searchNotes = async () => {
  await Promise.all([
    fetchClasses(),
    fetchEtudiants(),
    fetchMatieres(),
    fetchNotes()
  ])
}

const generatePDF = async (etudiantId, semestre) => {
  try {
    const bulletin = await fetchBulletin(etudiantId, semestre)
    if (bulletin) {
      // Ici on pourrait ouvrir une nouvelle fenêtre avec le PDF
      console.log('Générer PDF:', bulletin)
    }
  } catch (error) {
    console.error('Erreur lors de la génération du PDF:', error)
  }
}

const viewBulletin = async (etudiantId, semestre) => {
  try {
    const bulletin = await fetchBulletin(etudiantId, semestre)
    if (bulletin) {
      router.push({
        name: 'bulletin',
        params: { etudiantId, semestre }
      })
    }
  } catch (error) {
    console.error('Erreur lors de l\'affichage du bulletin:', error)
  }
}

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

const openCreateModal = () => {
  currentNote.value = {
    etudiant: null,
    matiere: null,
    note: null,
    date: new Date().toISOString().split('T')[0]
  }
  isEditing.value = false
  showModal.value = true
}

const editNote = (note) => {
  currentNote.value = { ...note }
  isEditing.value = true
  showModal.value = true
}

const saveNote = async () => {
  try {
    if (isEditing.value) {
      await axios.put(`http://localhost:8000/api/notes/${currentNote.value.id}/`, currentNote.value)
    } else {
      await axios.post('http://localhost:8000/api/notes/', currentNote.value)
    }
    await fetchNotes()
    closeModal()
  } catch (error) {
    console.error('Erreur lors de la sauvegarde de la note:', error)
  }
}

const deleteNote = async (id) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cette note ?')) {
    try {
      await axios.delete(`http://localhost:8000/api/notes/${id}/`)
      await fetchNotes()
    } catch (error) {
      console.error('Erreur lors de la suppression de la note:', error)
    }
  }
}

const closeModal = () => {
  showModal.value = false
}

const currentNote = ref({
  etudiant: null,
  matiere: null,
  note: null,
  type: 'DEVOIR',
  semestre: 1,
  date: new Date().toISOString().split('T')[0]
})
const showModal = ref(false)
const isEditing = ref(false)

// Initialisation
onMounted(async () => {
  await searchNotes()
})
</script>

<style scoped>
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

.btn-add {
  background-color: #2563eb;
  color: white;
  padding: 10px 18px;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s ease;
}
.btn-add:hover {
  background-color: #1d4ed8;
}

.classes-table {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
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

.search-container input {
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  width: 220px;
  transition: border 0.3s ease;
}
.search-container input:focus {
  border-color: #2563eb;
  outline: none;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

table th, table td {
  padding: 14px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

table th {
  background-color: #f3f4f6;
  color: #374151;
  font-weight: 600;
}

.btn-edit, .btn-delete {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
  margin: 0 4px;
  transition: 0.3s ease;
  border: none;
}

.btn-edit {
  background-color: #10b981;
  color: white;
}
.btn-edit:hover {
  background-color: #059669;
}

.btn-delete {
  background-color: #ef4444;
  color: white;
}

.btn-bulletin {
  background-color: #6366f1;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
  margin: 0 4px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: 0.3s ease;
}

.btn-bulletin:hover {
  background-color: #4f46e5;
}

.btn-bulletin i {
  font-size: 14px;
}
.btn-delete:hover {
  background-color: #dc2626;
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
  opacity: 10;
  cursor: not-allowed;
  background-color: red;
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 30px;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  animation: fadeIn 0.3s ease;
}

.modal-title {
  font-size: 22px;
  margin-bottom: 20px;
  color: #111827;
}

form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 6px;
  color: #374151;
}

input[type="text"], input[type="number"] {
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  transition: border 0.3s ease;
}
input:focus {
  border-color: #2563eb;
  outline: none;
}

.form-actions {
  grid-column: span 2;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
}

.btn-submit {
  background-color: #2563eb;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.btn-submit:hover {
  background-color: #1d4ed8;
}

.btn-cancel {
  background-color: #6b7280;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.btn-cancel:hover {
  background-color: #4b5563;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.header h1 {
  display: flex;
  align-items: center;
  gap: 10px; /* espace entre l’icône et le texte */
  font-size: 28px;
  font-weight: bold;
  color: #1f2937;
}

.header h1 i {
  font-size: 28px;
  color: #2563eb;
  transform: translateY(2px); /* léger ajustement vertical */
}

</style>

