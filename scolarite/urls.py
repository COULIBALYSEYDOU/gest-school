from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClasseViewSet, EtudiantViewSet, ProfesseurViewSet, 
    MatiereViewSet, NoteViewSet, PresenceViewSet,
    create_etudiant, update_etudiant
)
from .views_bulletins import BulletinView, ClasseNotesView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'classes', ClasseViewSet)
router.register(r'etudiants', EtudiantViewSet)
router.register(r'professeurs', ProfesseurViewSet)
router.register(r'matieres', MatiereViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'presences', PresenceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('bulletin/<int:etudiant_id>/<int:semestre>/', BulletinView.as_view(), name='bulletin'),
    path('classe/<int:classe_id>/notes/<int:semestre>/', ClasseNotesView.as_view(), name='classe_notes'),
    path('etudiant/', create_etudiant, name='create_etudiant'),
    path('etudiant/<int:pk>/', update_etudiant, name='update_etudiant')
]