
# Système de Gestion de Scolarité

Un système complet de gestion de scolarité développé avec Django (backend) et Vue.js (frontend).

## Fonctionnalités

- Gestion des étudiants
- Gestion des professeurs
- Gestion des classes
- Gestion des matières
- Gestion des notes
- Gestion des présences
- Rapports et statistiques

## Installation

1. Créer un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer la base de données dans `gestschool/settings.py`

4. Appliquer les migrations :
```bash
python manage.py migrate
```

5. Lancer le serveur de développement :
```bash
python manage.py runserver
```

## Structure du projet

- `backend/` : Contient l'application Django
- `frontend/` : Contient l'application Vue.js
- `gestschool/` : Configuration du projet Django
