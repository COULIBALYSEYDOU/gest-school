<template>
  <div class="form-control">
    <div class="flex items-start">
      <div class="flex items-center h-5">
        <input
          :id="id"
          :name="name"
          type="checkbox"
          :checked="modelValue"
          @change="$emit('update:modelValue', $event.target.checked)"
          :required="required"
          :disabled="disabled"
          :class="[
            'h-4 w-4 rounded transition duration-150 ease-in-out',
            error ? 'text-red-600 border-red-300 focus:ring-red-500' : 'text-primary border-gray-300 focus:ring-primary',
            disabled ? 'bg-gray-100 cursor-not-allowed' : ''
          ]"
        />
      </div>
      <div class="ml-3 text-sm">
        <label :for="id" :class="['font-medium', disabled ? 'text-gray-400' : 'text-gray-700']">
          {{ label }}
          <span v-if="required" class="text-red-500">*</span>
        </label>
        <p v-if="helpText && !error" class="text-gray-500">{{ helpText }}</p>
        <p v-if="error" class="text-red-600">{{ error }}</p>
      </div>
    </div>
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
  modelValue: {
    type: Boolean,
    default: false
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
