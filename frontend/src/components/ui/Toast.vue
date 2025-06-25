<template>
  <div 
    v-if="visible"
    :class="[
      'fixed z-50 p-4 rounded-md shadow-lg transform transition-all duration-300 ease-in-out',
      positionClasses,
      typeClasses,
      visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
    ]"
  >
    <div class="flex items-center">
      <!-- Icône en fonction du type -->
      <div class="flex-shrink-0">
        <!-- Succès -->
        <svg v-if="type === 'success'" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        <!-- Erreur -->
        <svg v-else-if="type === 'error'" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        <!-- Info -->
        <svg v-else-if="type === 'info'" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        <!-- Warning -->
        <svg v-else-if="type === 'warning'" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
      </div>
      
      <!-- Contenu -->
      <div class="ml-3">
        <h3 v-if="title" class="text-sm font-medium">{{ title }}</h3>
        <div class="text-sm">{{ message }}</div>
      </div>
      
      <!-- Bouton de fermeture -->
      <div class="ml-auto pl-3">
        <button 
          @click="close"
          class="inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2"
          :class="closeButtonClasses"
        >
          <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';

const props = defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  title: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    required: true
  },
  duration: {
    type: Number,
    default: 3000 // 3 secondes par défaut
  },
  position: {
    type: String,
    default: 'top-right',
    validator: (value) => [
      'top-right', 'top-left', 'bottom-right', 'bottom-left', 'top-center', 'bottom-center'
    ].includes(value)
  },
  autoClose: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['close']);

// État de visibilité
const visible = ref(false);
let timer = null;

// Classes en fonction du type
const typeClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-green-50 text-green-800';
    case 'error':
      return 'bg-red-50 text-red-800';
    case 'warning':
      return 'bg-yellow-50 text-yellow-800';
    case 'info':
      return 'bg-blue-50 text-blue-800';
    default:
      return 'bg-gray-50 text-gray-800';
  }
});

// Classes pour le bouton de fermeture
const closeButtonClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'text-green-500 hover:bg-green-100 focus:ring-green-400 focus:ring-offset-green-50';
    case 'error':
      return 'text-red-500 hover:bg-red-100 focus:ring-red-400 focus:ring-offset-red-50';
    case 'warning':
      return 'text-yellow-500 hover:bg-yellow-100 focus:ring-yellow-400 focus:ring-offset-yellow-50';
    case 'info':
      return 'text-blue-500 hover:bg-blue-100 focus:ring-blue-400 focus:ring-offset-blue-50';
    default:
      return 'text-gray-500 hover:bg-gray-100 focus:ring-gray-400 focus:ring-offset-gray-50';
  }
});

// Classes de position
const positionClasses = computed(() => {
  switch (props.position) {
    case 'top-right':
      return 'top-4 right-4';
    case 'top-left':
      return 'top-4 left-4';
    case 'bottom-right':
      return 'bottom-4 right-4';
    case 'bottom-left':
      return 'bottom-4 left-4';
    case 'top-center':
      return 'top-4 left-1/2 -translate-x-1/2';
    case 'bottom-center':
      return 'bottom-4 left-1/2 -translate-x-1/2';
    default:
      return 'top-4 right-4';
  }
});

// Fermeture du toast
const close = () => {
  visible.value = false;
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
  // Émettre un événement pour informer le parent
  setTimeout(() => {
    emit('close');
  }, 300); // Attendre la fin de l'animation
};

// Démarrer le timer pour la fermeture automatique
const startTimer = () => {
  if (props.autoClose && props.duration > 0) {
    timer = setTimeout(() => {
      close();
    }, props.duration);
  }
};

// Afficher le toast à l'initialisation
onMounted(() => {
  // Petit délai pour permettre l'animation d'entrée
  setTimeout(() => {
    visible.value = true;
    startTimer();
  }, 100);
});

// Réinitialiser le timer si la durée change
watch(() => props.duration, () => {
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
  if (visible.value) {
    startTimer();
  }
});
</script>

<style scoped>
/* Animation de transition */
.transform {
  transition-property: opacity, transform;
}
</style>
