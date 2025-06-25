<template>
  <form @submit.prevent="handleSubmit" :class="formClass">
    <div v-if="title" class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800">{{ title }}</h2>
      <p v-if="subtitle" class="mt-1 text-sm text-gray-500">{{ subtitle }}</p>
    </div>
    
    <!-- Message de succès -->
    <div v-if="successMessage" class="mb-4 p-4 rounded-md bg-green-50 border border-green-200">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium text-green-800">{{ successMessage }}</p>
        </div>
      </div>
    </div>
    
    <!-- Message d'erreur -->
    <div v-if="errorMessage" class="mb-4 p-4 rounded-md bg-red-50 border border-red-200">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium text-red-800">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
    
    <!-- Contenu du formulaire -->
    <slot></slot>
    
    <!-- Boutons d'action -->
    <div :class="['flex', buttonsAlign === 'right' ? 'justify-end' : (buttonsAlign === 'center' ? 'justify-center' : 'justify-start'), 'space-x-3 mt-6']">
      <slot name="buttons">
        <button 
          v-if="showCancelButton" 
          type="button" 
          @click="$emit('cancel')"
          :disabled="loading"
          class="px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          {{ cancelText }}
        </button>
        <button 
          type="submit" 
          :disabled="loading || disabled"
          :class="[
            'px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white',
            loading ? 'bg-primary-300 cursor-not-allowed' : 'bg-primary hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary',
            disabled && !loading ? 'bg-gray-300 cursor-not-allowed' : ''
          ]"
        >
          <span v-if="loading" class="flex items-center">
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loadingText }}
          </span>
          <span v-else>{{ submitText }}</span>
        </button>
      </slot>
    </div>
  </form>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  formClass: {
    type: String,
    default: ''
  },
  submitText: {
    type: String,
    default: 'Enregistrer'
  },
  cancelText: {
    type: String,
    default: 'Annuler'
  },
  loadingText: {
    type: String,
    default: 'Chargement...'
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  showCancelButton: {
    type: Boolean,
    default: true
  },
  successMessage: {
    type: String,
    default: ''
  },
  errorMessage: {
    type: String,
    default: ''
  },
  buttonsAlign: {
    type: String,
    default: 'right',
    validator: (value: string) => ['left', 'center', 'right'].includes(value)
  }
});

const emit = defineEmits(['submit', 'cancel']);

const handleSubmit = (event: Event) => {
  emit('submit', event);
};
</script>

<style scoped>
/* Animation de chargement */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
