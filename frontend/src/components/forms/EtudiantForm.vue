<template>
  <BaseForm
    :title="isEditing ? 'Modifier un étudiant' : 'Ajouter un étudiant'"
    :submitText="isEditing ? 'Mettre à jour' : 'Enregistrer'"
    :loading="loading"
    :errorMessage="globalError"
    @submit="handleSubmit"
    @cancel="$emit('cancel')"
  >
    <FormFieldset legend="Informations personnelles" columns="2">
      <BaseInput
        id="last_name"
        label="Nom"
        v-model="form.user.last_name"
        :error="errors.last_name"
        required
        placeholder="Entrez le nom de famille"
      />
      
      <BaseInput
        id="first_name"
        label="Prénom"
        v-model="form.user.first_name"
        :error="errors.first_name"
        required
        placeholder="Entrez le prénom"
      />
      
      <BaseDatepicker
        id="date_naissance"
        label="Date de naissance"
        v-model="form.date_naissance"
        :error="errors.date_naissance"
        required
        :max="maxBirthDate"
        helpText="Date de naissance de l'étudiant"
      />
      
      <BaseSelect
        id="classe"
        label="Classe"
        v-model="form.classe"
        :error="errors.classe"
        required
        placeholder="Sélectionnez une classe"
      >
        <option v-for="classe in classes" :key="classe.id" :value="classe.id">
          {{ classe.nom }}
        </option>
      </BaseSelect>
    </FormFieldset>
    
    <FormFieldset legend="Coordonnées">
      <BaseTextarea
        id="adresse"
        label="Adresse"
        v-model="form.adresse"
        :error="errors.adresse"
        required
        rows="3"
        placeholder="Entrez l'adresse complète"
      />
      
      <BaseInput
        id="telephone"
        label="Téléphone"
        v-model="form.telephone"
        :error="errors.telephone"
        placeholder="Ex: 01 23 45 67 89"
        type="tel"
      />
      
      <BaseInput
        id="email"
        label="Email"
        v-model="form.email"
        :error="errors.email"
        placeholder="Ex: etudiant@exemple.com"
        type="email"
      />
    </FormFieldset>
    
    <FormFieldset legend="Informations supplémentaires">
      <BaseCheckbox
        id="active"
        label="Étudiant actif"
        v-model="form.active"
        helpText="Décochez pour désactiver temporairement l'étudiant"
      />
    </FormFieldset>
  </BaseForm>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import axios from 'axios';
import { ValidationService } from '@/services/ValidationService';

// Import des composants de formulaire
import BaseForm from '@/components/forms/BaseForm.vue';
import FormFieldset from '@/components/forms/FormFieldset.vue';
import BaseInput from '@/components/forms/BaseInput.vue';
import BaseSelect from '@/components/forms/BaseSelect.vue';
import BaseDatepicker from '@/components/forms/BaseDatepicker.vue';
import BaseTextarea from '@/components/forms/BaseTextarea.vue';
import BaseCheckbox from '@/components/forms/BaseCheckbox.vue';

// Props
const props = defineProps({
  etudiant: {
    type: Object,
    default: () => ({
      user: { first_name: '', last_name: '' },
      classe: null,
      date_naissance: '',
      adresse: '',
      telephone: '',
      email: '',
      active: true
    })
  },
  isEditing: {
    type: Boolean,
    default: false
  }
});

// Émissions d'événements
const emit = defineEmits(['submit', 'cancel']);

// État du formulaire
const form = reactive({
  user: {
    first_name: props.etudiant.user?.first_name || '',
    last_name: props.etudiant.user?.last_name || ''
  },
  classe: props.etudiant.classe || null,
  date_naissance: props.etudiant.date_naissance || '',
  adresse: props.etudiant.adresse || '',
  telephone: props.etudiant.telephone || '',
  email: props.etudiant.email || '',
  active: props.etudiant.active !== undefined ? props.etudiant.active : true
});

// État des erreurs
const errors = reactive({
  first_name: '',
  last_name: '',
  classe: '',
  date_naissance: '',
  adresse: '',
  telephone: '',
  email: ''
});

// État global
const loading = ref(false);
const globalError = ref('');
const classes = ref([]);

// Date maximale pour la date de naissance (aujourd'hui)
const maxBirthDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

// Chargement des classes
const fetchClasses = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/classes/');
    classes.value = response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des classes:', error);
    globalError.value = 'Impossible de charger la liste des classes.';
  }
};

// Validation du formulaire
const validateForm = () => {
  let isValid = true;
  
  // Validation du nom
  const lastNameResult = ValidationService.validate(
    form.user.last_name,
    [
      { rule: ValidationService.required, message: 'Le nom est requis.' },
      { rule: ValidationService.maxLength, options: { max: 100 }, message: 'Le nom ne doit pas dépasser 100 caractères.' }
    ],
    'Le nom'
  );
  errors.last_name = lastNameResult.valid ? '' : lastNameResult.message || '';
  isValid = isValid && lastNameResult.valid;
  
  // Validation du prénom
  const firstNameResult = ValidationService.validate(
    form.user.first_name,
    [
      { rule: ValidationService.required, message: 'Le prénom est requis.' },
      { rule: ValidationService.maxLength, options: { max: 100 }, message: 'Le prénom ne doit pas dépasser 100 caractères.' }
    ],
    'Le prénom'
  );
  errors.first_name = firstNameResult.valid ? '' : firstNameResult.message || '';
  isValid = isValid && firstNameResult.valid;
  
  // Validation de la classe
  const classeResult = ValidationService.validate(
    form.classe,
    [{ rule: ValidationService.required, message: 'La classe est requise.' }],
    'La classe'
  );
  errors.classe = classeResult.valid ? '' : classeResult.message || '';
  isValid = isValid && classeResult.valid;
  
  // Validation de la date de naissance
  const dateResult = ValidationService.validate(
    form.date_naissance,
    [
      { rule: ValidationService.required, message: 'La date de naissance est requise.' },
      { rule: ValidationService.isDate, message: 'La date de naissance doit être une date valide.' },
      { rule: ValidationService.isPastDate, message: 'La date de naissance doit être dans le passé.' }
    ],
    'La date de naissance'
  );
  errors.date_naissance = dateResult.valid ? '' : dateResult.message || '';
  isValid = isValid && dateResult.valid;
  
  // Validation de l'adresse
  const adresseResult = ValidationService.validate(
    form.adresse,
    [{ rule: ValidationService.required, message: 'L\'adresse est requise.' }],
    'L\'adresse'
  );
  errors.adresse = adresseResult.valid ? '' : adresseResult.message || '';
  isValid = isValid && adresseResult.valid;
  
  // Validation de l'email (si fourni)
  if (form.email) {
    const emailResult = ValidationService.validate(
      form.email,
      [{ rule: ValidationService.email, message: 'L\'email n\'est pas valide.' }],
      'L\'email'
    );
    errors.email = emailResult.valid ? '' : emailResult.message || '';
    isValid = isValid && emailResult.valid;
  } else {
    errors.email = '';
  }
  
  // Validation du téléphone (si fourni)
  if (form.telephone) {
    const phoneRegex = /^[0-9\s+()-]{8,15}$/;
    const phoneResult = ValidationService.validate(
      form.telephone,
      [{ 
        rule: ValidationService.pattern, 
        options: { regex: phoneRegex }, 
        message: 'Le numéro de téléphone n\'est pas valide.' 
      }],
      'Le téléphone'
    );
    errors.telephone = phoneResult.valid ? '' : phoneResult.message || '';
    isValid = isValid && phoneResult.valid;
  } else {
    errors.telephone = '';
  }
  
  return isValid;
};

// Soumission du formulaire
const handleSubmit = async () => {
  // Réinitialiser les erreurs
  globalError.value = '';
  
  // Valider le formulaire
  if (!validateForm()) {
    return;
  }
  
  // Soumettre le formulaire
  loading.value = true;
  
  try {
    // Préparer les données à envoyer
    const etudiantData = {
      ...props.etudiant,
      user: {
        ...props.etudiant.user,
        first_name: form.user.first_name,
        last_name: form.user.last_name
      },
      classe: form.classe,
      date_naissance: form.date_naissance,
      adresse: form.adresse,
      telephone: form.telephone,
      email: form.email,
      active: form.active
    };
    
    // Émettre l'événement avec les données
    emit('submit', etudiantData);
  } catch (error) {
    console.error('Erreur lors de la soumission du formulaire:', error);
    globalError.value = 'Une erreur est survenue lors de la soumission du formulaire.';
  } finally {
    loading.value = false;
  }
};

// Chargement initial des données
onMounted(() => {
  fetchClasses();
});
</script>
