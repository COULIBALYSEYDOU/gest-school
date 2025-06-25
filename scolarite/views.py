from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Classe, Etudiant, Professeur, Matiere, Note, Presence
from .serializers import (
    ClasseSerializer, EtudiantSerializer, ProfesseurSerializer, 
    MatiereSerializer, NoteSerializer, PresenceSerializer
)

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer

class EtudiantViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer

class ProfesseurViewSet(viewsets.ModelViewSet):
    queryset = Professeur.objects.all()
    serializer_class = ProfesseurSerializer

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class PresenceViewSet(viewsets.ModelViewSet):
    queryset = Presence.objects.all()
    serializer_class = PresenceSerializer

# Vue spécifique pour gérer la création et la mise à jour des étudiants
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def create_etudiant(request):
    serializer = EtudiantSerializer(data=request.data)
    if serializer.is_valid():
        # Créer l'utilisateur
        user_data = serializer.validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['email'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password='default_password'  # Le mot de passe sera changé après la création
        )
        
        # Créer l'étudiant
        etudiant = Etudiant.objects.create(user=user, **serializer.validated_data)
        return Response(EtudiantSerializer(etudiant).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    serializer = EtudiantSerializer(etudiant, data=request.data, partial=True)
    
    if serializer.is_valid():
        # Mettre à jour l'utilisateur
        user_data = serializer.validated_data.pop('user', None)
        if user_data:
            user = etudiant.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()
        
        # Mettre à jour l'étudiant
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)