<template>
  <div class="form-control">
    <label :for="id" class="block text-sm font-medium text-gray-700 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <div class="relative">
      <!-- Icône à gauche si fournie -->
      <div v-if="icon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <component :is="icon" class="h-5 w-5 text-gray-400" />
      </div>
      
      <!-- Icône de calendrier par défaut -->
      <div v-else class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
      
      <input
        :id="id"
        :name="name"
        :type="type"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :min="min"
        :max="max"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        :readonly="readonly"
        :class="[
          'block w-full rounded-md shadow-sm transition duration-150 ease-in-out pl-10',
          error ? 'border-red-300 text-red-900 placeholder-red-300 focus:outline-none focus:ring-red-500 focus:border-red-500' 
                : 'border-gray-300 focus:outline-none focus:ring-primary focus:border-primary',
          disabled ? 'bg-gray-100 cursor-not-allowed' : '',
          'py-2 pr-3'
        ]"
      />
    </div>
    
    <!-- Message d'erreur -->
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
    
    <!-- Message d'aide -->
    <p v-if="helpText && !error" class="mt-1 text-sm text-gray-500">{{ helpText }}</p>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  name: {
    type: String,
    default(): string {
      return this.id as string;
    }
  },
  label: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'date' // Peut être 'date', 'datetime-local', 'month', etc.
  },
  modelValue: {
    type: String,
    default: ''
  },
  min: {
    type: String,
    default: ''
  },
  max: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  helpText: {
    type: String,
    default: ''
  },
  icon: {
    type: [String, Object, Function],
    default: null
  }
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.form-control {
  @apply mb-4;
}

/* Personnalisation de l'apparence du sélecteur de date natif */
input[type="date"],
input[type="datetime-local"],
input[type="month"],
input[type="time"] {
  @apply appearance-none;
}

/* Masquer l'icône de calendrier native sur certains navigateurs */
input::-webkit-calendar-picker-indicator {
  @apply opacity-0 absolute right-0 top-0 bottom-0 w-10 h-auto cursor-pointer;
}
</style>
