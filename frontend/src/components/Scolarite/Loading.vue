<template>
    <div class="loading">
      <div class="spinner"></div>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script setup>
  defineProps({
    message: {
      type: String,
      default: 'Chargement...'
    }
  })
  </script>
  
  <style scoped>
  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #42b983;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 10px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  p {
    color: #666;
    margin: 0;
  }
  </style>