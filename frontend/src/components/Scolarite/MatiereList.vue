<template>
  <div class="scolarite-container">
    <!-- Header avec Titre et Bouton Ajouter -->
    <header class="header">
      <h1>
       <i class="fas fa-book" aria-hidden="true"></i> Gestion des Matières
     </h1>
      <button class="btn-add" @click="openCreateModal">
        <i class="fas fa-plus-circle"></i> Ajouter une matière
      </button>
    </header>

    <!-- Section Table -->
    <section class="classes-table">
      <!-- Barre de recherche -->
      <div class="search-container">
        <input type="text" v-model="searchQuery" placeholder="Rechercher une matière..." />
      </div>

      <!-- Tableau des matières -->
      <table>
        <thead>
          <tr>
            <th>Nom</th>
            <th>Code</th>
            <th>Volume horaire</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="matiere in filteredMatieres" :key="matiere.id">
            <td>{{ matiere.nom }}</td>
            <td>{{ matiere.code }}</td>
            <td>{{ matiere.volume_horaire }} h</td>
            <td>
              <button @click="editMatiere(matiere)" class="btn-edit">Modifier</button>
              <button @click="deleteMatiere(matiere.id)" class="btn-delete">Supprimer</button>
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
        <h2 class="modal-title">{{ isEditing ? 'Modifier' : 'Ajouter' }} une matière</h2>
        <form @submit.prevent="saveMatiere">
          <div class="form-group">
            <label for="nom">Nom</label>
            <input v-model="currentMatiere.nom" id="nom" type="text" required />
          </div>
          <div class="form-group">
            <label for="code">Code</label>
            <input v-model="currentMatiere.code" id="code" type="text" required />
          </div>
          <div class="form-group">
            <label for="volume">Volume horaire</label>
            <input v-model="currentMatiere.volume_horaire" id="volume" type="number" required />
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-submit">{{ isEditing ? 'Enregistrer' : 'Créer' }}</button>
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

const matieres = ref([])
const currentMatiere = ref({ nom: '', code: '', volume_horaire: 0 })
const showModal = ref(false)
const isEditing = ref(false)
const searchQuery = ref('')

const currentPage = ref(1)
const pageSize = 5

const totalPages = computed(() => Math.ceil(filteredMatieres.value.length / pageSize))

const fetchMatieres = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/matieres/')
    matieres.value = response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des matières:', error)
  }
}

const openCreateModal = () => {
  currentMatiere.value = { nom: '', code: '', volume_horaire: 0 }
  isEditing.value = false
  showModal.value = true
}

const editMatiere = (matiere) => {
  currentMatiere.value = { ...matiere }
  isEditing.value = true
  showModal.value = true
}

const saveMatiere = async () => {
  try {
    if (isEditing.value) {
      await axios.put(`http://localhost:8000/api/matieres/${currentMatiere.value.id}/`, currentMatiere.value)
    } else {
      await axios.post('http://localhost:8000/api/matieres/', currentMatiere.value)
    }
    await fetchMatieres()
    closeModal()
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
  }
}

const deleteMatiere = async (id) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cette matière ?')) {
    try {
      await axios.delete(`http://localhost:8000/api/matieres/${id}/`)
      await fetchMatieres()
    } catch (error) {
      console.error('Erreur lors de la suppression:', error)
    }
  }
}

const closeModal = () => {
  showModal.value = false
}

const filteredMatieres = computed(() => {
  return matieres.value
    .filter(matiere => matiere.nom.toLowerCase().includes(searchQuery.value.toLowerCase()))
    .slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
})

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

onMounted(fetchMatieres)
</script>

<style scoped>
scolarite-container {
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
  background: #024feb;
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
  color: #2563eb; /* couleur bleue */
  transform: translateY(2px); /* léger ajustement vertical */
}

</style>


