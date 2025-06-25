<template>
  <div class="bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">{{ title }}</h2>
    <form @submit.prevent="handleSubmit">
      <slot></slot>
      <div class="mt-6">
        <button type="submit" 
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
          {{ submitText }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  submitText: {
    type: String,
    default: 'Submit'
  }
})

const emit = defineEmits(['submit'])

const handleSubmit = (event) => {
  emit('submit', event)
}
</script>

<style scoped>
/* Styles spécifiques au formulaire */
input[type="text"],
input[type="email"],
input[type="password"],
select,
textarea {
  @apply w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
}

.form-group {
  @apply mb-4;
}

.error {
  @apply text-red-500 text-sm mt-1;
}
</style>
