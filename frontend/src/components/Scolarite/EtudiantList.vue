<template>
  <div class="scolarite-container">
    <!-- Header avec Titre et Bouton Ajouter -->
    <header class="header">
      <h1>
    <i class="fas fa-user-graduate" style="margin-right: 8px;"></i> Gestion des Étudiants
    </h1>

      <button class="btn-add" @click="openCreateModal">
        <i class="fas fa-user-plus"></i> Ajouter un étudiant
      </button>
    </header>

    <!-- Section Table -->
    <section class="classes-table">
      <!-- Barre de recherche -->
      <div class="search-container">
        <input type="text" v-model="searchQuery" placeholder="Rechercher un étudiant..." />
      </div>

      <!-- Tableau des étudiants -->
      <table>
        <thead>
          <tr>
            <th>Nom</th>
            <th>Prénom</th>
            <th>Email</th>
            <th>Classe</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="etudiant in filteredEtudiants" :key="etudiant.id">
            <td>{{ etudiant.user.last_name }}</td>
            <td>{{ etudiant.user.first_name }}</td>
            <td>{{ etudiant.user.email }}</td>
            <td>{{ etudiant.classe_nom }}</td>
            <td>
              <button @click="editEtudiant(etudiant)" class="btn-edit">Modifier</button>
              <button @click="deleteEtudiant(etudiant.id)" class="btn-delete">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1"> ← Précédent</button>
        <span>Page {{ currentPage }} sur {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages"> Suivant → </button>
      </div>
    </section>

    <!-- Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2 class="modal-title">{{ isEditing ? 'Modifier' : 'Ajouter' }} un étudiant</h2>
        <form @submit.prevent="saveEtudiant">
          <div class="form-group">
            <label for="last_name">Nom</label>
            <input v-model="currentEtudiant.user.last_name" id="last_name" type="text" required />
          </div>
          <div class="form-group">
            <label for="first_name">Prénom</label>
            <input v-model="currentEtudiant.user.first_name" id="first_name" type="text" required />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input v-model="currentEtudiant.user.email" id="email" type="email" required />
          </div>
          <div class="form-group">
            <label for="classe">Classe</label>
            <select v-model="currentEtudiant.classe" id="classe" required>
              <option value="">Sélectionnez une classe</option>
              <option v-for="classe in classes" :key="classe.id" :value="classe.id">
                {{ classe.nom }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="date_naissance">Date de naissance</label>
            <input v-model="currentEtudiant.date_naissance" id="date_naissance" type="date" required />
          </div>
          <div class="form-group">
            <label for="adresse">Adresse</label>
            <textarea v-model="currentEtudiant.adresse" id="adresse" rows="3"></textarea>
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
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const etudiants = ref([])
const classes = ref([])
const currentEtudiant = ref({
  user: {
    first_name: '',
    last_name: '',
    email: ''
  },
  classe: '',
  date_naissance: '',
  adresse: ''
})
const showModal = ref(false)
const isEditing = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 5

const fetchEtudiants = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/etudiants/')
    etudiants.value = response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des étudiants:', error)
  }
}

const fetchClasses = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/classes/')
    classes.value = response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des classes:', error)
  }
}

const openCreateModal = () => {
  currentEtudiant.value = {
    user: {
      first_name: '',
      last_name: '',
      email: ''
    },
    classe: '',
    date_naissance: '',
    adresse: ''
  }
  isEditing.value = false
  showModal.value = true
}

const editEtudiant = (etudiant) => {
  currentEtudiant.value = { ...etudiant }
  isEditing.value = true
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveEtudiant = async () => {
  try {
    if (isEditing.value) {
      await axios.put(`http://localhost:8000/api/etudiants/${currentEtudiant.value.id}/`, currentEtudiant.value)
    } else {
      await axios.post('http://localhost:8000/api/etudiants/', currentEtudiant.value)
    }
    await fetchEtudiants()
    closeModal()
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
  }
}

const deleteEtudiant = async (id) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cet étudiant ?')) {
    try {
      await axios.delete(`http://localhost:8000/api/etudiants/${id}/`)
      await fetchEtudiants()
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
    }
  }
}

const filteredEtudiants = computed(() => {
  return etudiants.value.filter(e =>
    e.user.last_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    e.user.first_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    e.user.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    e.classe_nom.toLowerCase().includes(searchQuery.value.toLowerCase())
  ).slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
})

const totalPages = computed(() => Math.ceil(filteredEtudiants.value.length / pageSize))

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}
const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

onMounted(fetchEtudiants)
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
  background: #0755f1;
  border-radius: 6px;
  cursor: pointer;
}
.pagination button:disabled {
  opacity: 10;
  cursor: not-allowed;
  background-color: #ff071c;
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

.header h1 i {
  margin-right: 10px;
  color: #2563eb;
}

</style>
