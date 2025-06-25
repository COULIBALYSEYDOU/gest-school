<template>
    <div class="rapports-container">
      <h1>Rapports et Statistiques</h1>
      
      <!-- Filtres -->
      <div class="filters">
        <select v-model="selectedClasse" @change="fetchRapports">
          <option value="">Toutes les classes</option>
          <option v-for="classe in classes" :key="classe.id" :value="classe.id">
            {{ classe.nom }}
          </option>
        </select>
        <select v-model="selectedDate" @change="fetchRapports">
          <option value="">Toutes les dates</option>
          <option v-for="date in dates" :key="date" :value="date">
            {{ new Date(date).toLocaleDateString() }}
          </option>
        </select>
      </div>
  
      <!-- Rapports -->
      <div class="rapports">
        <div class="rapport">
          <h2>Statistiques des Notes</h2>
          <div v-if="statsNotes">
            <p>Moyenne générale: {{ statsNotes.moyenne_generale.toFixed(2) }}</p>
            <p>Meilleure note: {{ statsNotes.meilleure_note }}</p>
            <p>Pire note: {{ statsNotes.pire_note }}</p>
          </div>
        </div>
  
        <div class="rapport">
          <h2>Taux de Présence</h2>
          <div v-if="statsPresences">
            <p>Taux moyen: {{ statsPresences.taux_moyen }}%</p>
            <p>Meilleur taux: {{ statsPresences.meilleur_taux }}%</p>
            <p>Pire taux: {{ statsPresences.pire_taux }}%</p>
          </div>
        </div>
  
        <div class="rapport">
          <h2>Classement des Étudiants</h2>
          <table v-if="classement">
            <thead>
              <tr>
                <th>Position</th>
                <th>Étudiant</th>
                <th>Moyenne</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(etudiant, index) in classement" :key="etudiant.id">
                <td>{{ index + 1 }}</td>
                <td>{{ etudiant.user.last_name }} {{ etudiant.user.first_name }}</td>
                <td>{{ etudiant.moyenne.toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const selectedClasse = ref('')
  const selectedDate = ref('')
  const classes = ref([])
  const dates = ref([])
  const statsNotes = ref(null)
  const statsPresences = ref(null)
  const classement = ref([])
  
  const fetchClasses = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/classes/')
      classes.value = response.data
    } catch (error) {
      console.error('Erreur lors de la récupération des classes:', error)
    }
  }
  
  const fetchDates = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/dates/')
      dates.value = response.data
    } catch (error) {
      console.error('Erreur lors de la récupération des dates:', error)
    }
  }
  
  const fetchRapports = async () => {
    try {
      // Récupérer les statistiques des notes
      let urlNotes = 'http://localhost:8000/api/stats/notes/'
      if (selectedClasse.value) {
        urlNotes += `?classe=${selectedClasse.value}`
      }
      if (selectedDate.value) {
        urlNotes += selectedClasse.value ? '&' : '?'
        urlNotes += `date=${selectedDate.value}`
      }
      const responseNotes = await axios.get(urlNotes)
      statsNotes.value = responseNotes.data
  
      // Récupérer les statistiques des présences
      let urlPresences = 'http://localhost:8000/api/stats/presences/'
      if (selectedClasse.value) {
        urlPresences += `?classe=${selectedClasse.value}`
      }
      if (selectedDate.value) {
        urlPresences += selectedClasse.value ? '&' : '?'
        urlPresences += `date=${selectedDate.value}`
      }
      const responsePresences = await axios.get(urlPresences)
      statsPresences.value = responsePresences.data
  
      // Récupérer le classement
      let urlClassement = 'http://localhost:8000/api/classement/'
      if (selectedClasse.value) {
        urlClassement += `?classe=${selectedClasse.value}`
      }
      const responseClassement = await axios.get(urlClassement)
      classement.value = responseClassement.data
    } catch (error) {
      console.error('Erreur lors de la récupération des rapports:', error)
    }
  }
  
  onMounted(async () => {
    await Promise.all([
      fetchClasses(),
      fetchDates()
    ])
  })
  </script>
  
  <style scoped>
  .rapports-container {
    padding: 20px;
  }
  
  .filters {
    margin-bottom: 20px;
  }
  
  select {
    padding: 8px;
    margin-right: 10px;
  }
  
  .rapports {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .rapport {
    border: 1px solid #ccc;
    padding: 15px;
    border-radius: 4px;
  }
  
  .rapport h2 {
    margin-bottom: 15px;
    color: #333;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  th {
    background-color: #f5f5f5;
  }
  </style>