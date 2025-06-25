from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

class Classe(models.Model):
    nom = models.CharField(max_length=50)
    niveau = models.CharField(max_length=20)
    capacite = models.IntegerField()

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, null=True, blank=True)
    date_naissance = models.DateField()
    adresse = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.classe.nom if self.classe else 'Aucune classe'}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

    def get_short_name(self):
        return self.prenom

class Professeur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()

class Matiere(models.Model):
    nom = models.CharField(max_length=50)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    coefficient = models.FloatField(default=1.0)

class Note(models.Model):
    TYPE_NOTE = (
        ('DEVOIR', 'Devoir'),
        ('CONTROLE', 'Contrôle'),
        ('EXAMEN', 'Examen')
    )
    
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    note = models.FloatField()
    type = models.CharField(max_length=10, choices=TYPE_NOTE, default='DEVOIR')
    semestre = models.IntegerField(choices=[(1, 'Semestre 1'), (2, 'Semestre 2')], null=True, blank=True)
    date = models.DateField(default=timezone.now)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.etudiant.user.get_full_name()} - {self.matiere.nom} - {self.type}"
    
    @property
    def moyenne(self):
        return self.note

class Presence(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)