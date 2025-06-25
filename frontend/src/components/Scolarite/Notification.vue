<template>
    <div v-if="show" :class="['notification', type]">
      <div class="content">
        <span class="message">{{ message }}</span>
        <button @click="close">&times;</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const props = defineProps({
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'success',
      validator: (value) => ['success', 'error', 'warning'].includes(value)
    }
  })
  
  const show = ref(true)
  
  const emit = defineEmits(['close'])
  
  const close = () => {
    show.value = false
    emit('close')
  }
  </script>
  
  <style scoped>
  .notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 25px;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    z-index: 1000;
    animation: slideIn 0.3s ease-out;
  }
  
  .content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }
  
  .message {
    margin: 0;
  }
  
  button {
    background: none;
    border: none;
    color: white;
    font-size: 1.2em;
    cursor: pointer;
    padding: 0 5px;
  }
  
  .success {
    background-color: #4CAF50;
  }
  
  .error {
    background-color: #f44336;
  }
  
  .warning {
    background-color: #ff9800;
  }
  
  @keyframes slideIn {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  </style>