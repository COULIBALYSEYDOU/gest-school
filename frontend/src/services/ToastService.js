import { ref, markRaw, h, render } from 'vue';
import Toast from '@/components/ui/Toast.vue';

// État global pour stocker les toasts actifs
const toasts = ref([]);
let toastId = 0;

/**
 * Crée un conteneur pour les toasts s'il n'existe pas déjà
 */
function ensureContainer() {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'fixed inset-0 z-50 pointer-events-none';
    document.body.appendChild(container);
  }
  return container;
}

/**
 * Ajoute un toast à la liste
 */
function addToast({ type, title, message, duration = 3000, position = 'top-right', autoClose = true }) {
  const id = `toast-${toastId++}`;
  const container = ensureContainer();
  
  // Créer un élément pour ce toast spécifique
  const toastContainer = document.createElement('div');
  toastContainer.id = id;
  toastContainer.className = 'pointer-events-auto';
  container.appendChild(toastContainer);
  
  // Créer le composant Toast
  const toastInstance = h(Toast, {
    type,
    title,
    message,
    duration,
    position,
    autoClose,
    onClose: () => removeToast(id)
  });
  
  // Rendre le composant dans le conteneur
  render(toastInstance, toastContainer);
  
  // Ajouter à la liste des toasts actifs
  toasts.value.push({
    id,
    type,
    title,
    message,
    container: toastContainer
  });
  
  return id;
}

/**
 * Supprime un toast de la liste
 */
function removeToast(id) {
  const index = toasts.value.findIndex(toast => toast.id === id);
  if (index !== -1) {
    const toast = toasts.value[index];
    
    // Supprimer le conteneur du DOM
    if (toast.container && toast.container.parentNode) {
      render(null, toast.container); // Nettoyer le rendu Vue
      toast.container.parentNode.removeChild(toast.container);
    }
    
    // Supprimer de la liste
    toasts.value.splice(index, 1);
  }
}

/**
 * Supprime tous les toasts
 */
function clearAllToasts() {
  toasts.value.forEach(toast => {
    if (toast.container && toast.container.parentNode) {
      render(null, toast.container);
      toast.container.parentNode.removeChild(toast.container);
    }
  });
  toasts.value = [];
}

/**
 * Service de notification exposant les méthodes pour afficher différents types de toasts
 */
export const ToastService = {
  // Affiche un toast de succès
  success(message, title = 'Succès', options = {}) {
    return addToast({ type: 'success', title, message, ...options });
  },
  
  // Affiche un toast d'erreur
  error(message, title = 'Erreur', options = {}) {
    return addToast({ type: 'error', title, message, ...options });
  },
  
  // Affiche un toast d'information
  info(message, title = 'Information', options = {}) {
    return addToast({ type: 'info', title, message, ...options });
  },
  
  // Affiche un toast d'avertissement
  warning(message, title = 'Attention', options = {}) {
    return addToast({ type: 'warning', title, message, ...options });
  },
  
  // Supprime un toast spécifique
  remove(id) {
    removeToast(id);
  },
  
  // Supprime tous les toasts
  clearAll() {
    clearAllToasts();
  },
  
  // Retourne la liste des toasts actifs (pour des besoins de débogage)
  getToasts() {
    return toasts.value;
  }
};

export default ToastService;
