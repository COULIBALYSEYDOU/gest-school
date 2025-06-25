from django import forms
from django.contrib.auth.models import User
from .models import Etudiant

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['user', 'classe', 'date_naissance', 'adresse']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pour un nouvel étudiant, on ne montre pas les informations du User
        if self.instance.pk:  # Si l'instance existe déjà
            user = self.instance.user
            if user:
                self.fields['user'].label = 'Utilisateur'
                self.fields['user'].help_text = f"Nom: {user.last_name}, Prénom: {user.first_name}, Email: {user.email}"
        else:
            self.fields['user'].label = 'Utilisateur'

    def clean_user(self):
        user = self.cleaned_data.get('user')
        if user:
            return user
        raise forms.ValidationError("Vous devez sélectionner un utilisateur")
