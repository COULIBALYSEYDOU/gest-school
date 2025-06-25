<template>
  <fieldset :class="['border-t border-gray-200 pt-4', spacing]">
    <legend v-if="legend" class="px-2 text-lg font-medium text-gray-900">
      {{ legend }}
    </legend>
    <div v-if="description" class="mt-1 text-sm text-gray-500">
      {{ description }}
    </div>
    <div :class="['mt-4', columns === 1 ? '' : `grid grid-cols-${columns} gap-x-4 gap-y-2`]">
      <slot></slot>
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps({
  legend: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  columns: {
    type: Number,
    default: 1,
    validator: (value: number) => [1, 2, 3, 4, 6].includes(value)
  },
  spacing: {
    type: String,
    default: 'mb-6'
  }
});
</script>

<style scoped>
/* Classes de grille pour différentes colonnes */
.grid-cols-2 {
  @apply grid-cols-1 md:grid-cols-2;
}

.grid-cols-3 {
  @apply grid-cols-1 md:grid-cols-2 lg:grid-cols-3;
}

.grid-cols-4 {
  @apply grid-cols-1 md:grid-cols-2 lg:grid-cols-4;
}

.grid-cols-6 {
  @apply grid-cols-1 md:grid-cols-3 lg:grid-cols-6;
}
</style>
