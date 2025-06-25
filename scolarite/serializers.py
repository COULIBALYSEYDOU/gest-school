from rest_framework import serializers
from .models import Classe, Etudiant, Professeur, Matiere, Note, Presence

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = '__all__'

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class EtudiantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    classe_nom = serializers.SerializerMethodField()
    nom = serializers.CharField(source='user.last_name', read_only=True)
    prenom = serializers.CharField(source='user.first_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Etudiant
        fields = [
            'id',
            'user',
            'nom',
            'prenom',
            'email',
            'classe',
            'classe_nom',
            'date_naissance',
            'adresse',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['nom', 'prenom', 'email', 'created_at', 'updated_at']

    def get_classe_nom(self, obj):
        return obj.classe.nom if obj.classe else None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', 'default_password')
        user = User.objects.create_user(
            username=user_data['email'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=password
        )
        etudiant = Etudiant.objects.create(user=user, **validated_data)
        return etudiant

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            if 'password' in user_data:
                user.set_password(user_data['password'])
            user.save()
        return super().update(instance, validated_data)

class ProfesseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professeur
        fields = '__all__'

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    matiere_nom = serializers.SerializerMethodField()
    classe_nom = serializers.SerializerMethodField()
    type = serializers.CharField(source='get_type_display')
    semestre = serializers.IntegerField()
    moyenne = serializers.FloatField()

    class Meta:
        model = Note
        fields = ['id', 'etudiant', 'etudiant_nom', 'matiere', 'matiere_nom', 
                 'note', 'type', 'semestre', 'date', 'moyenne', 'classe_nom']

    def get_etudiant_nom(self, obj):
        return obj.etudiant.user.get_full_name()

    def get_matiere_nom(self, obj):
        return obj.matiere.nom

    def get_classe_nom(self, obj):
        return obj.etudiant.classe.nom if obj.etudiant.classe else None

    def get_moyenne(self, obj):
        return obj.moyenne
        return obj.moyenne_generale

class PresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = '__all__'