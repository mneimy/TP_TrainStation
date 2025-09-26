# 🏗️ Architecture de l'Application Gare de Train

## Vue d'ensemble

L'application Gare de Train suit une architecture MVC (Model-View-Controller) avec Flask, organisée en modules Blueprint pour une meilleure séparation des responsabilités.

## Diagramme d'Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        COUCHE PRÉSENTATION                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Browser   │  │   Mobile    │  │   Tablet    │  │  API    │ │
│  │   (Web)     │  │   (Web)     │  │   (Web)     │  │ (JSON)  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        COUCHE RÉSEAU                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │    HTTP     │  │    HTTPS    │  │   WebSocket │             │
│  │   (Port     │  │   (Port     │  │  (Future)   │             │
│  │    5001)    │  │    443)     │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      COUCHE APPLICATION                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    FLASK APPLICATION                        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │ │
│  │  │   Routes    │  │  Templates  │  │   Static    │         │ │
│  │  │ (Blueprints)│  │  (Jinja2)   │  │   Files     │         │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘         │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      COUCHE LOGIQUE MÉTIER                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │    Auth     │  │    Train    │  │Reservation  │  │  Main   │ │
│  │  Module     │  │   Module    │  │   Module    │  │ Module  │ │
│  │             │  │             │  │             │  │         │ │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────┐ │ │
│  │ │ Routes  │ │  │ │ Routes  │ │  │ │ Routes  │ │  │ │Routes│ │ │
│  │ │ Forms   │ │  │ │ Forms   │ │  │ │ Forms   │ │  │ │     │ │ │
│  │ │ Logic   │ │  │ │ Logic   │ │  │ │ Logic   │ │  │ │     │ │ │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │  │ └─────┘ │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      COUCHE DONNÉES                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Models    │  │   ORM       │  │  Database   │             │
│  │ (SQLAlchemy)│  │(SQLAlchemy) │  │  (SQLite/   │             │
│  │             │  │             │  │ PostgreSQL) │             │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │             │
│  │ │  User   │ │  │ │  Query  │ │  │ │ Tables  │ │             │
│  │ │  Train  │ │  │ │ Builder │ │  │ │ Indexes │ │             │
│  │ │Reserv.  │ │  │ │ Migrate │ │  │ │ Views   │ │             │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

## Structure des Modules

### 1. Module d'Authentification (`auth/`)

**Responsabilités :**
- Gestion des utilisateurs (inscription, connexion, déconnexion)
- Validation des formulaires d'authentification
- Gestion des sessions utilisateur

**Fichiers :**
```
auth/
├── __init__.py          # Initialisation du module
└── routes.py            # Routes d'authentification
```

**Routes :**
- `GET/POST /auth/login` - Connexion
- `GET/POST /auth/register` - Inscription
- `GET /auth/logout` - Déconnexion

### 2. Module de Gestion des Trains (`train/`)

**Responsabilités :**
- CRUD des trains (Create, Read, Update, Delete)
- Validation des données de train
- Gestion des formulaires de train

**Fichiers :**
```
train/
├── __init__.py          # Initialisation du module
└── routes.py            # Routes des trains
```

**Routes :**
- `GET /train/` - Liste des trains
- `GET/POST /train/add` - Ajout d'un train
- `GET /train/<id>` - Détails d'un train
- `GET/POST /train/<id>/edit` - Modification d'un train
- `POST /train/<id>/delete` - Suppression d'un train

### 3. Module de Réservation (`reservation/`)

**Responsabilités :**
- Gestion des réservations utilisateur
- Validation des réservations
- Prévention des doublons

**Fichiers :**
```
reservation/
├── __init__.py          # Initialisation du module
└── routes.py            # Routes des réservations
```

**Routes :**
- `GET /reservation/` - Liste des réservations
- `GET/POST /reservation/add` - Nouvelle réservation
- `POST /reservation/<id>/cancel` - Annulation

### 4. Module Principal (`main/`)

**Responsabilités :**
- Pages d'accueil et tableau de bord
- Navigation générale
- Gestion des erreurs

**Fichiers :**
```
main/
├── __init__.py          # Initialisation du module
└── routes.py            # Routes principales
```

**Routes :**
- `GET /` - Page d'accueil
- `GET /dashboard` - Tableau de bord

## Modèles de Données

### User (Utilisateur)
```python
class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    reservations = db.relationship('Reservation', backref='user')
```

### Train
```python
class Train(db.Model):
    id_train = db.Column(db.Integer, primary_key=True)
    train_number = db.Column(db.String, nullable=False)
    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    distance = db.Column(db.Integer)
    source_station_code = db.Column(db.String(50))
    source_station_name = db.Column(db.String(200))
    destination_station_code = db.Column(db.String(50))
    destination_station_name = db.Column(db.String(200))
    reservations = db.relationship('Reservation', backref='train')
```

### Reservation
```python
class Reservation(db.Model):
    id_reservation = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('utilisateur.id_user'))
    id_train = db.Column(db.Integer, db.ForeignKey('train.id_train'))
```

## Flux de Données

### 1. Authentification
```
Utilisateur → Formulaire → Validation → Session → Redirection
```

### 2. Réservation
```
Utilisateur → Sélection Train → Validation → Création → Confirmation
```

### 3. Gestion des Trains
```
Admin → Formulaire → Validation → Base de Données → Mise à jour UI
```

## Sécurité

### 1. Protection CSRF
- Tous les formulaires sont protégés par CSRF
- Tokens générés automatiquement par Flask-WTF

### 2. Validation des Données
- Validation côté client (HTML5)
- Validation côté serveur (WTForms)
- Sanitisation des entrées

### 3. Gestion des Sessions
- Sessions sécurisées avec clé secrète
- Timeout automatique des sessions
- Protection contre les attaques de fixation

## Performance

### 1. Base de Données
- Index sur les clés étrangères
- Requêtes optimisées avec SQLAlchemy
- Pagination pour les grandes listes

### 2. Frontend
- CSS et JS minifiés
- Images optimisées
- Cache des ressources statiques

### 3. Caching
- Cache des templates Jinja2
- Cache des requêtes SQLAlchemy
- Headers de cache HTTP

## Déploiement

### 1. Développement
```bash
python3 app.py
```

### 2. Production
```bash
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### 3. Docker (Future)
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app"]
```

## Monitoring

### 1. Logs
- Logs d'application Flask
- Logs d'erreur SQLAlchemy
- Logs d'accès HTTP

### 2. Métriques
- Temps de réponse des requêtes
- Utilisation de la base de données
- Erreurs applicatives

## Évolutions Futures

### 1. Fonctionnalités
- API REST complète
- Notifications en temps réel
- Système de paiement
- Gestion des sièges

### 2. Technique
- Migration vers PostgreSQL
- Cache Redis
- Load balancing
- Microservices

### 3. UI/UX
- Application mobile native
- PWA (Progressive Web App)
- Interface d'administration
- Dashboard analytics
