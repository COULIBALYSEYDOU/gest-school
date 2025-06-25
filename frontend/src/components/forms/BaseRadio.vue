<template>
  <div class="form-control">
    <label class="block text-sm font-medium text-gray-700 mb-2">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <div class="space-y-2">
      <div v-for="(option, index) in options" :key="index" class="flex items-center">
        <input
          :id="`${id}-${index}`"
          :name="name"
          type="radio"
          :value="option.value"
          :checked="modelValue === option.value"
          @change="$emit('update:modelValue', option.value)"
          :required="required"
          :disabled="disabled || option.disabled"
          :class="[
            'h-4 w-4 transition duration-150 ease-in-out',
            error ? 'text-red-600 border-red-300 focus:ring-red-500' : 'text-primary border-gray-300 focus:ring-primary',
            disabled ? 'bg-gray-100 cursor-not-allowed' : ''
          ]"
        />
        <label :for="`${id}-${index}`" class="ml-3 block text-sm font-medium text-gray-700">
          {{ option.label }}
        </label>
      </div>
    </div>
    
    <!-- Message d'erreur -->
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
    
    <!-- Message d'aide -->
    <p v-if="helpText && !error" class="mt-1 text-sm text-gray-500">{{ helpText }}</p>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

interface RadioOption {
  label: string;
  value: string | number;
  disabled?: boolean;
}

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
  options: {
    type: Array as () => RadioOption[],
    required: true
  },
  modelValue: {
    type: [String, Number],
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
