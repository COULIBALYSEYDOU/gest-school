<template>
  <div class="bg-white shadow rounded-lg overflow-hidden">
    <!-- Tableau -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th 
              v-for="column in columns" 
              :key="column.key" 
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              {{ column.label }}
            </th>
            <th v-if="hasActions" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <!-- Message si aucun résultat -->
          <tr v-if="items.length === 0">
            <td :colspan="columns.length + (hasActions ? 1 : 0)" class="px-6 py-10 text-center text-gray-500">
              <p>Aucun élément trouvé</p>
            </td>
          </tr>
          
          <!-- Affichage des données -->
          <tr 
            v-for="(item, index) in items" 
            :key="index"
            class="hover:bg-gray-50"
          >
            <td 
              v-for="column in columns" 
              :key="column.key" 
              class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
            >
              <slot :name="column.key" :item="item">
                {{ getNestedValue(item, column.key) }}
              </slot>
            </td>
            <td v-if="hasActions" class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <slot name="actions" :item="item">
                <button @click="editItem(item)" class="text-indigo-600 hover:text-indigo-900 mr-4">
                  Modifier
                </button>
                <button @click="deleteItem(item)" class="text-red-600 hover:text-red-900">
                  Supprimer
                </button>
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  },
  hasActions: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['edit', 'delete'])

// Fonctions
const getNestedValue = (obj, path) => {
  if (!path) return obj
  const keys = path.split('.')
  return keys.reduce((o, key) => (o && o[key] !== undefined) ? o[key] : null, obj)
}

const editItem = (item) => {
  emit('edit', item)
}

const deleteItem = (item) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
    emit('delete', item)
  }
}
</script>

<style scoped>
/* Style de base pour le tableau */
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 0.75rem 1rem;
  text-align: left;
}

th {
  font-weight: 500;
  text-transform: uppercase;
  font-size: 0.75rem;
  color: #6b7280;
}

tr:hover {
  background-color: #f9fafb;
}
</style>
