from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Etudiant, Note, Matiere
from .serializers import NoteSerializer


class BulletinView(APIView):
    def get(self, request, etudiant_id, semestre):
        """Récupère le bulletin d'un étudiant pour un semestre"""
        try:
            etudiant = Etudiant.objects.get(id=etudiant_id)
            
            # Notes par matière
            notes = Note.objects.filter(
                etudiant=etudiant,
                semestre=semestre
            ).select_related('matiere')
            
            # Calcul des moyennes par matière
            matieres = Matiere.objects.filter(
                classe=etudiant.classe
            ).prefetch_related('note_set')
            
            bulletin = {
                'etudiant': {
                    'nom': etudiant.user.get_full_name(),
                    'classe': etudiant.classe.nom
                },
                'semestre': semestre,
                'moyennes': [],
                'moyenne_generale': 0
            }
            
            total_notes = 0
            total_coefficients = 0
            
            for matiere in matieres:
                notes_matiere = notes.filter(matiere=matiere)
                if notes_matiere.exists():
                    moyenne = notes_matiere.aggregate(models.Avg('note'))['note__avg']
                    total_notes += moyenne * matiere.coefficient
                    total_coefficients += matiere.coefficient
                    
                    bulletin['moyennes'].append({
                        'matiere': matiere.nom,
                        'moyenne': moyenne,
                        'coefficient': matiere.coefficient
                    })
            
            if total_coefficients > 0:
                bulletin['moyenne_generale'] = total_notes / total_coefficients
            
            return Response(bulletin)
            
        except Etudiant.DoesNotExist:
            return Response({"error": "Étudiant non trouvé"}, status=404)


class ClasseNotesView(generics.ListAPIView):
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        classe_id = self.kwargs['classe_id']
        semestre = self.kwargs['semestre']
        return Note.objects.filter(
            etudiant__classe_id=classe_id,
            semestre=semestre
        ).select_related('etudiant', 'matiere')
