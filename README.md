# 🚂 Gare de Train - Application Web Flask

Une application web complète pour la gestion des trains et des réservations, développée avec Flask et SQLAlchemy.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [API Routes](#-api-routes)
- [Base de données](#-base-de-données)
- [Développement](#-développement)

## 🎯 Fonctionnalités

### Authentification
- ✅ **Inscription** : Enregistrement d'utilisateurs avec nom, prénom et âge
- ✅ **Connexion** : Identification basée sur nom/prénom/âge
- ✅ **Gestion des sessions** : Maintien de la connexion utilisateur
- ✅ **Déconnexion** : Fermeture de session sécurisée

### Gestion des Trains
- ✅ **Ajout de trains** : Formulaire complet avec tous les champs
- ✅ **Liste des trains** : Affichage de tous les trains disponibles
- ✅ **Modification** : Édition des informations des trains
- ✅ **Suppression** : Suppression des trains avec confirmation
- ✅ **Détails** : Vue détaillée de chaque train

### Système de Réservation
- ✅ **Réservation** : Sélection d'un train et création d'une réservation
- ✅ **Liste des réservations** : Affichage des réservations de l'utilisateur
- ✅ **Annulation** : Suppression des réservations avec confirmation
- ✅ **Protection** : Empêche les doublons de réservation

### Interface Utilisateur
- ✅ **Design moderne** : Interface Bootstrap 5 responsive
- ✅ **Navigation intuitive** : Menu de navigation complet
- ✅ **Messages flash** : Notifications de succès/erreur
- ✅ **Templates structurés** : Organisation claire des vues

## 🏗️ Architecture

### Architecture MVC (Model-View-Controller)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CONTROLLERS   │    │     MODELS      │    │      VIEWS      │
│                 │    │                 │    │                 │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │   Auth    │  │    │  │   User    │  │    │  │ Templates │  │
│  │  Routes   │  │◄──►│  │  Model   │  │◄──►│  │    HTML   │  │
│  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │
│                 │    │                 │    │                 │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │   Train   │  │    │  │   Train   │  │    │  │  Static   │  │
│  │  Routes   │  │◄──►│  │  Model   │  │◄──►│  │   Files   │  │
│  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │
│                 │    │                 │    │                 │
│  ┌───────────┐  │    │  ┌───────────┐  │    │                 │
│  │Reservation│  │    │  │Reservation│  │    │                 │
│  │  Routes   │  │◄──►│  │  Model   │  │    │                 │
│  └───────────┘  │    │  └───────────┘  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   DATABASE      │
                    │                 │
                    │  ┌───────────┐  │
                    │  │  SQLite   │  │
                    │  │PostgreSQL │  │
                    │  └───────────┘  │
                    └─────────────────┘
```

### Technologies Utilisées

- **Backend** : Flask 3.1.2
- **ORM** : SQLAlchemy 2.0.43
- **Base de données** : PostgreSQL (par défaut) / SQLite (optionnel)
- **Formulaires** : WTForms 3.2.1
- **Frontend** : Bootstrap 5.1.3
- **Templates** : Jinja2 3.1.6
- **Sécurité** : Flask-WTF 1.2.2
- **Configuration** : python-dotenv 1.0.0
- **Authentification** : Flask-Login 0.6.3

## 🚀 Installation

### Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- PostgreSQL (recommandé) ou SQLite (optionnel)
- Git (pour le versioning)

### Installation des dépendances

```bash
# Cloner le projet
git clone <repository-url>
cd TP-TrainStation

# Configuration automatique pour Git
chmod +x setup_git.sh
./setup_git.sh

# Créer un environnement virtuel
python3 -m venv prod
source prod/bin/activate  # Sur Windows: prod\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configuration de l'environnement
cp config.env.example .env
# Modifier .env avec vos configurations personnelles (DB_USERNAME, DB_PASSWORD, etc.)

# Configuration de la base de données PostgreSQL
# Voir le guide détaillé : SQL/README.md
# 1. Créer la base de données TrainStation
# 2. Exécuter le script SQL/Creation_script.sql
# 3. Configurer les variables d'environnement dans .env

# Lancer l'application
python3 app.py
```

### Fichier requirements.txt

```txt
# Framework web principal
Flask==3.1.2

# Extensions Flask
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.2
Flask-Login==0.6.3

# Gestion des formulaires
WTForms==3.2.1

# Base de données
SQLAlchemy==2.0.43
psycopg2-binary==2.9.10

# Gestion des variables d'environnement
python-dotenv==1.0.0

# Dépendances système
Werkzeug==3.1.3
Jinja2==3.1.6
MarkupSafe==3.0.2
itsdangerous==2.2.0
click==8.3.0
blinker==1.9.0
```

## ⚙️ Configuration

### Variables d'environnement

L'application utilise des fichiers d'environnement pour la configuration :

#### 1. Fichier `.env` (Vos informations personnelles)
Créez un fichier `.env` à la racine du projet avec vos informations :

```bash
# Configuration personnelle - NE SERA PAS COMMITTÉ
SECRET_KEY=votre-cle-secrete-personnelle
FLASK_ENV=development
FLASK_DEBUG=True

# Configuration PostgreSQL personnelle
DB_HOST=localhost
DB_PORT=5432
DB_NAME=TrainStation
DB_USERNAME=votre_utilisateur_postgresql
DB_PASSWORD=votre_mot_de_passe

# Configuration du serveur
HOST=0.0.0.0
PORT=5001
```

#### 2. Fichier `config.env.example` (Pour Git)
Ce fichier contient des valeurs génériques et sera committé :

```bash
# Configuration générique - SERA COMMITTÉ
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Configuration PostgreSQL générique
DB_HOST=localhost
DB_PORT=5432
DB_NAME=TrainStation
DB_USERNAME=postgres
DB_PASSWORD=

# Configuration du serveur
HOST=0.0.0.0
PORT=5001
```

#### 3. Configuration automatique
L'application charge automatiquement le fichier `.env` grâce à `python-dotenv`.

### Configuration de la Base de Données

Pour une configuration complète de PostgreSQL, consultez le **[Guide de Configuration de la Base de Données](SQL/README.md)**.

#### Configuration Rapide

```sql
-- Se connecter à PostgreSQL
psql -U postgres

-- Créer la base de données
CREATE DATABASE "TrainStation";

-- Créer un utilisateur (optionnel)
CREATE USER trainuser WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE "TrainStation" TO trainuser;

-- Exécuter le script de création des tables
\i SQL/Creation_script.sql
```

## 🎮 Utilisation

### Lancement de l'application

```bash
# Activer l'environnement virtuel
source prod/bin/activate

# Lancer l'application
python3 app.py
```

L'application sera accessible sur : `http://localhost:5001`

### Utilisation de l'interface

1. **Accueil** : Page d'accueil avec vue d'ensemble
2. **Inscription** : Créer un compte utilisateur
3. **Connexion** : Se connecter avec nom/prénom/âge
4. **Gestion des trains** : Ajouter, modifier, supprimer des trains
5. **Réservations** : Réserver et gérer ses réservations

## 📁 Structure du projet

```
TP-TrainStation/
├── app/                          # Application principale
│   ├── __init__.py              # Configuration Flask
│   ├── config.py                # Configuration de l'app
│   ├── models.py                # Modèles SQLAlchemy
│   ├── forms.py                 # Formulaires WTForms
│   ├── database/                # Module de base de données
│   │   ├── __init__.py
│   │   └── queries.py           # Requêtes SQL sécurisées
│   ├── auth/                    # Module d'authentification
│   │   ├── __init__.py
│   │   └── routes.py            # Routes d'authentification
│   ├── main/                    # Pages principales
│   │   ├── __init__.py
│   │   └── routes.py            # Routes principales
│   ├── train/                   # Module de gestion des trains
│   │   ├── __init__.py
│   │   └── routes.py            # Routes des trains
│   ├── reservation/             # Module de réservation
│   │   ├── __init__.py
│   │   └── routes.py            # Routes des réservations
│   ├── templates/               # Templates HTML
│   │   ├── base.html           # Template de base
│   │   ├── index.html          # Page d'accueil
│   │   ├── dashboard.html      # Tableau de bord
│   │   ├── auth/               # Templates d'authentification
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── train/              # Templates des trains
│   │   │   ├── list.html
│   │   │   ├── add.html
│   │   │   ├── edit.html
│   │   │   └── view.html
│   │   └── reservation/        # Templates des réservations
│   │       ├── list.html
│   │       └── add.html
│   └── static/                 # Fichiers statiques
│       └── style.css           # Styles CSS
├── prod/                       # Environnement virtuel
├── SQL/                        # Scripts SQL
│   ├── Creation_script.sql     # Script de création des tables
│   ├── queries.sql             # Requêtes SQL sécurisées
│   └── README.md               # Guide de configuration de la base de données
├── app.py                      # Point d'entrée
├── .env                        # Variables d'environnement personnelles (ignoré par Git)
├── .gitignore                  # Fichiers à ignorer par Git
├── requirements.txt            # Dépendances Python
├── config.env.example          # Exemple de configuration générique
├── setup_git.sh               # Script de configuration Git
└── README.md                   # Documentation
```

## 🛣️ API Routes

### Routes principales
- `GET /` - Page d'accueil
- `GET /dashboard` - Tableau de bord (authentifié)

### Authentification
- `GET /auth/login` - Page de connexion
- `POST /auth/login` - Traitement de la connexion
- `GET /auth/register` - Page d'inscription
- `POST /auth/register` - Traitement de l'inscription
- `GET /auth/logout` - Déconnexion

### Gestion des trains
- `GET /train/` - Liste des trains
- `GET /train/add` - Formulaire d'ajout
- `POST /train/add` - Traitement de l'ajout
- `GET /train/<id>` - Détails d'un train
- `GET /train/<id>/edit` - Formulaire de modification
- `POST /train/<id>/edit` - Traitement de la modification
- `POST /train/<id>/delete` - Suppression d'un train

### Réservations
- `GET /reservation/` - Liste des réservations (authentifié)
- `GET /reservation/add` - Formulaire de réservation
- `POST /reservation/add` - Traitement de la réservation
- `POST /reservation/<id>/cancel` - Annulation d'une réservation

## 🗄️ Base de données

### Modèles

#### User (utilisateur)
```python
- id_user: INTEGER (PK)
- nom: VARCHAR(100)
- prenom: VARCHAR(100)
- age: INTEGER
```

#### Train
```python
- id_train: INTEGER (PK)
- train_number: VARCHAR
- arrival_time: TIME
- departure_time: TIME
- distance: INTEGER
- source_station_code: VARCHAR(50)
- source_station_name: VARCHAR(200)
- destination_station_code: VARCHAR(50)
- destination_station_name: VARCHAR(200)
```

#### Reservation
```python
- id_reservation: INTEGER (PK)
- id_user: INTEGER (FK -> User)
- id_train: INTEGER (FK -> Train)
```

### Relations
- User 1:N Reservation
- Train 1:N Reservation
- Reservation N:1 User
- Reservation N:1 Train

## 🔒 Sécurité

### Protection contre les injections SQL

L'application utilise des requêtes SQL paramétrées pour éviter les injections SQL :

- **Requêtes centralisées** : Toutes les requêtes sont dans `SQL/queries.sql`
- **Module de requêtes** : `app/database/queries.py` gère les requêtes sécurisées
- **Paramètres obligatoires** : Toutes les requêtes utilisent des paramètres `%s`
- **Validation des entrées** : WTForms valide toutes les données utilisateur

### Gestion des fichiers sensibles

#### Fichiers protégés par `.gitignore` :
- `.env` - Configuration personnelle (NE SERA PAS COMMITTÉ)
- `*.env` - Tous les fichiers d'environnement
- `config.env` - Configuration locale
- `instance/` - Base de données locale
- `__pycache__/` - Fichiers Python compilés
- Logs et fichiers temporaires
- Scripts de test et démonstration

#### Fichiers committés :
- `config.env.example` - Modèle de configuration générique
- `requirements.txt` - Dépendances Python
- `README.md` - Documentation
- Code source de l'application

### Configuration sécurisée

- **Variables d'environnement** : Toutes les informations sensibles sont dans `.env`
- **Chargement automatique** : `python-dotenv` charge le fichier `.env`
- **Valeurs par défaut** : Configuration générique dans `config.env.example`
- **Séparation claire** : Informations personnelles vs génériques

## 🔧 Développement

### Ajout de nouvelles fonctionnalités

1. **Créer un nouveau module** :
   ```bash
   mkdir app/nouveau_module
   touch app/nouveau_module/__init__.py
   touch app/nouveau_module/routes.py
   ```

2. **Ajouter les routes dans `__init__.py`** :
   ```python
   from .nouveau_module.routes import nouveau_bp
   app.register_blueprint(nouveau_bp, url_prefix='/nouveau')
   ```

3. **Créer les templates** :
   ```bash
   mkdir app/templates/nouveau_module
   ```

4. **Ajouter des requêtes SQL** :
   - Ajouter dans `SQL/queries.sql`
   - Implémenter dans `app/database/queries.py`

5. **Ajouter des variables d'environnement** :
   - Ajouter dans `config.env.example` (valeur générique)
   - Documenter dans le README
   - Utiliser dans `app/config.py`

### Tests

```bash
# Lancer l'application en mode debug
python3 app.py

# Accéder à l'application
# http://localhost:5001

# Tester les fonctionnalités
# 1. Inscription d'un utilisateur
# 2. Connexion
# 3. Consultation des trains
# 4. Création de réservations
# 5. Gestion des réservations
```

### Configuration Git

```bash
# Configuration automatique pour Git
chmod +x setup_git.sh
./setup_git.sh

# Commiter les changements
git add .
git commit -m "Initial commit - Application Gare de Train"

# Ajouter un remote et pousser
git remote add origin <votre-repo-url>
git push -u origin main
```

### Déploiement

1. **Configuration de production** :
   ```bash
   # Créer un fichier .env pour la production
   cp config.env.example .env
   # Modifier .env avec les configurations de production
   
   # Ou utiliser des variables d'environnement
   export FLASK_ENV=production
   export DB_USERNAME=production_user
   export DB_PASSWORD=production_password
   export DB_HOST=production_host
   ```

2. **Utiliser un serveur WSGI** :
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

## 📝 Notes

- L'application utilise SQLite par défaut pour le développement
- PostgreSQL est recommandé pour la production
- Tous les formulaires sont protégés par CSRF
- L'authentification est basée sur les sessions Flask
- L'interface est responsive et compatible mobile

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
