from django.contrib import admin
from django.contrib.auth.models import User
from .models import Classe, Etudiant, Professeur, Matiere, Note, Presence
from .forms import EtudiantForm

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau', 'capacite')
    search_fields = ('nom', 'niveau')

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    form = EtudiantForm
    list_display = (
        'user',
        'classe',
        'date_naissance',
        'adresse',
        'created_at',
        'updated_at'
    )
    list_display_links = ('user',)
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'adresse'
    )
    list_filter = (
        'classe',
        'date_naissance',
        'created_at',
        'updated_at'
    )
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': (
                'user',
                'classe',
                'date_naissance',
                'adresse'
            )
        }),
        ('Dates', {
            'fields': (
                'created_at',
                'updated_at'
            )
        }),
    )
    
    readonly_fields = (
        'created_at',
        'updated_at'
    )

@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('user', 'matiere', 'telephone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'classe', 'coefficient')
    search_fields = ('nom',)
    list_filter = ('classe',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'matiere', 'note', 'date')
    search_fields = ('etudiant__user__username', 'matiere__nom')
    list_filter = ('date', 'matiere__classe')

@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'classe', 'date', 'present')
    search_fields = ('etudiant__user__username',)
    list_filter = ('date', 'classe')