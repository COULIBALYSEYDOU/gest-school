<template>
  <div class="form-control">
    <label :for="id" class="block text-sm font-medium text-gray-700 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <div class="relative">
      <textarea
        :id="id"
        :name="name"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        :readonly="readonly"
        :rows="rows"
        :class="[
          'block w-full rounded-md shadow-sm transition duration-150 ease-in-out',
          error ? 'border-red-300 text-red-900 placeholder-red-300 focus:outline-none focus:ring-red-500 focus:border-red-500' 
                : 'border-gray-300 focus:outline-none focus:ring-primary focus:border-primary',
          disabled ? 'bg-gray-100 cursor-not-allowed' : '',
          'py-2 px-3'
        ]"
      ></textarea>
      
      <!-- Indicateur de caractères restants si maxLength est défini -->
      <div v-if="maxLength > 0 && modelValue" class="absolute bottom-2 right-2 text-xs text-gray-500">
        {{ modelValue.length }}/{{ maxLength }}
      </div>
    </div>
    
    <!-- Message d'erreur -->
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
    
    <!-- Message d'aide -->
    <p v-if="helpText && !error" class="mt-1 text-sm text-gray-500">{{ helpText }}</p>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  name: {
    type: String,
    default() { return this.id; }
  },
  label: {
    type: String,
    required: true
  },
  modelValue: {
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
  rows: {
    type: Number,
    default: 4
  },
  maxLength: {
    type: Number,
    default: 0
  },
  error: {
    type: String,
    default: ''
  },
  helpText: {
    type: String,
    default: ''
  }
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.form-control {
  @apply mb-4;
}
</style>
