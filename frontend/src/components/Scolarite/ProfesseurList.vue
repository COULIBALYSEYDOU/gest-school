<template>
  <div class="scolarite-container">
    <!-- En-tête -->
    <header class="header">
    <h1>
      <i class="fas fa-chalkboard-teacher" style="margin-right: 8px;"></i> Gestion des Professeurs
    </h1>
      <button class="btn-add" @click="openModal">
        <i class="fas fa-user-plus"></i> Ajouter un professeur
      </button>
    </header>

    <!-- Zone de recherche -->
    <div class="search-container">
      <input v-model="searchQuery" type="text" placeholder="Rechercher un professeur..." />
    </div>

    <!-- Tableau -->
    <table>
      <thead>
        <tr>
          <th>Nom</th>
          <th>Prénom</th>
          <th>Matière</th>
          <th>Téléphone</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="professeur in paginatedProfesseurs" :key="professeur.id">
          <td>{{ professeur.user.last_name }}</td>
          <td>{{ professeur.user.first_name }}</td>
          <td>{{ professeur.matiere?.nom }}</td>
          <td>{{ professeur.telephone }}</td>
          <td>
            <button class="btn-edit" @click="editProfesseur(professeur)">Modifier</button>
            <button class="btn-delete" @click="deleteProfesseur(professeur.id)">Supprimer</button>
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

    <!-- Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>{{ isEditing ? 'Modifier' : 'Ajouter' }} un professeur</h2>
        <form @submit.prevent="saveProfesseur">
          <div class="form-group">
            <label>Nom</label>
            <input v-model="currentProfesseur.user.last_name" type="text" required />
          </div>
          <div class="form-group">
            <label>Prénom</label>
            <input v-model="currentProfesseur.user.first_name" type="text" required />
          </div>
          <div class="form-group">
            <label>Matière</label>
            <select v-model="currentProfesseur.matiere" required>
              <option value="" disabled selected>Choisir une matière</option>
              <option v-for="matiere in matieres" :key="matiere.id" :value="matiere.id">
                {{ matiere.nom }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Téléphone</label>
            <input v-model="currentProfesseur.telephone" type="text" required />
          </div>
          <div class="form-group">
            <label>Adresse</label>
            <textarea v-model="currentProfesseur.adresse" required></textarea>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-submit">{{ isEditing ? 'Enregistrer' : 'Créer' }}</button>
            <button type="button" class="btn-cancel" @click="closeModal">Annuler</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const professeurs = ref([])
const matieres = ref([])
const showModal = ref(false)
const isEditing = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 5

const currentProfesseur = ref({
  user: { last_name: '', first_name: '' },
  matiere: null,
  telephone: '',
  adresse: ''
})

const fetchProfesseurs = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/professeurs/')
    professeurs.value = res.data
  } catch (err) {
    console.error('Erreur récupération professeurs :', err)
  }
}

const fetchMatieres = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/matieres/')
    matieres.value = res.data
  } catch (err) {
    console.error('Erreur récupération matières :', err)
  }
}

const openModal = () => {
  isEditing.value = false
  currentProfesseur.value = {
    user: { last_name: '', first_name: '' },
    matiere: null,
    telephone: '',
    adresse: ''
  }
  showModal.value = true
}

const closeModal = () => (showModal.value = false)

const saveProfesseur = async () => {
  try {
    if (isEditing.value) {
      await axios.put(`http://localhost:8000/api/professeurs/${currentProfesseur.value.id}/`, currentProfesseur.value)
    } else {
      await axios.post(`http://localhost:8000/api/professeurs/`, currentProfesseur.value)
    }
    await fetchProfesseurs()
    closeModal()
  } catch (err) {
    console.error('Erreur sauvegarde professeur :', err)
  }
}

const editProfesseur = (prof) => {
  currentProfesseur.value = JSON.parse(JSON.stringify(prof)) // éviter mutation directe
  isEditing.value = true
  showModal.value = true
}

const deleteProfesseur = async (id) => {
  if (confirm('Confirmer la suppression ?')) {
    try {
      await axios.delete(`http://localhost:8000/api/professeurs/${id}/`)
      await fetchProfesseurs()
    } catch (err) {
      console.error('Erreur suppression professeur :', err)
    }
  }
}

const filteredProfesseurs = computed(() =>
  professeurs.value.filter(p =>
    `${p.user.last_name} ${p.user.first_name} ${p.telephone}`.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

const totalPages = computed(() => Math.ceil(filteredProfesseurs.value.length / pageSize))

const paginatedProfesseurs = computed(() =>
  filteredProfesseurs.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
)

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}
const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

onMounted(() => {
  fetchProfesseurs()
  fetchMatieres()
})
</script>

<style scoped>
/* @import './GestionSharedStyle.css'; */ /* Ce fichier contiendra les styles réutilisables pour toutes les pages */
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
  background: #024fe7;
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
h1 {
  display: flex;
  align-items: center;
  font-size: 28px;
  font-weight: bold;
  color: #1f2937;
}

h1 i {
  margin-right: 8px;
  font-size: 28px;
  color: #2563eb; /* couleur bleue sympa */
  /* léger ajustement vertical si besoin */
  transform: translateY(2px);
}

</style>



