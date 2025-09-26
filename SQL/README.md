# 📊 Base de Données - Gare de Train

Ce répertoire contient tous les scripts SQL nécessaires pour configurer et utiliser la base de données de l'application Gare de Train.

## 📁 Contenu du Répertoire

- `Creation_script.sql` - Script de création des tables
- `queries.sql` - Requêtes SQL sécurisées utilisées par l'application
- `README.md` - Ce fichier de documentation

## 🚀 Configuration de la Base de Données

### Prérequis

- PostgreSQL installé et en cours d'exécution
- Accès en tant qu'utilisateur avec privilèges de création de base de données
- Client PostgreSQL (psql) ou interface graphique (pgAdmin, DBeaver, etc.)

### 1. Création de la Base de Données

#### Option A : Via psql (ligne de commande)

```bash
# Se connecter à PostgreSQL en tant que superutilisateur
psql -U postgres

# Créer la base de données
CREATE DATABASE "TrainStation";

# Créer un utilisateur pour l'application (optionnel)
CREATE USER trainuser WITH PASSWORD 'votre_mot_de_passe';

# Donner les privilèges à l'utilisateur
GRANT ALL PRIVILEGES ON DATABASE "TrainStation" TO trainuser;

# Se déconnecter
\q
```

#### Option B : Via pgAdmin (interface graphique)

1. Ouvrir pgAdmin
2. Se connecter au serveur PostgreSQL
3. Clic droit sur "Databases" → "Create" → "Database"
4. Nom : `TrainStation`
5. Cliquer sur "Save"

### 2. Exécution du Script de Création

#### Option A : Via psql

```bash
# Se connecter à la base de données créée
psql -U trainuser -d TrainStation

# Exécuter le script de création
\i SQL/Creation_script.sql

# Vérifier que les tables ont été créées
\dt

# Se déconnecter
\q
```

#### Option B : Via pgAdmin

1. Ouvrir pgAdmin
2. Se connecter à la base de données `TrainStation`
3. Clic droit sur la base de données → "Query Tool"
4. Ouvrir le fichier `SQL/Creation_script.sql`
5. Exécuter le script (F5 ou bouton "Execute")

#### Option C : Via DBeaver

1. Ouvrir DBeaver
2. Se connecter à la base de données `TrainStation`
3. Ouvrir le fichier `SQL/Creation_script.sql`
4. Exécuter le script (Ctrl+Enter)

### 3. Vérification de l'Installation

Après l'exécution du script, vous devriez avoir les tables suivantes :

```sql
-- Vérifier les tables créées
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Résultat attendu :
-- table_name
-- -----------
-- utilisateur
-- train
-- reservation
```

## 📋 Structure des Tables

### Table `utilisateur`
```sql
CREATE TABLE utilisateur (
    id_user INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    age INTEGER
);
```

### Table `train`
```sql
CREATE TABLE train (
    id_train INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    train_number VARCHAR NOT NULL,
    arrival_time TIME,
    departure_time TIME,
    distance INT CHECK (distance >= 0),
    source_station_code VARCHAR(50),
    source_station_name VARCHAR(200),
    destination_station_code VARCHAR(50),
    destination_station_name VARCHAR(200)
);
```

### Table `reservation`
```sql
CREATE TABLE reservation (
    id_reservation INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_user INTEGER NOT NULL,
    id_train INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user),
    FOREIGN KEY (id_train) REFERENCES train(id_train)
);
```

## 🔧 Configuration de l'Application

### Variables d'Environnement

Créer un fichier `.env` à la racine du projet :

```bash
# Configuration PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=TrainStation
DB_USERNAME=trainuser
DB_PASSWORD=votre_mot_de_passe

# Autres configurations
SECRET_KEY=votre-cle-secrete
FLASK_ENV=development
FLASK_DEBUG=True
```

### Test de Connexion

```bash
# Lancer l'application
python3 app.py

# L'application devrait se connecter automatiquement à PostgreSQL
# Vérifier dans les logs qu'il n'y a pas d'erreur de connexion
```

## 📊 Requêtes SQL Sécurisées

Le fichier `queries.sql` contient toutes les requêtes SQL utilisées par l'application. Ces requêtes sont :

- **Sécurisées** : Utilisent des paramètres pour éviter les injections SQL
- **Documentées** : Chaque requête est commentée
- **Organisées** : Groupées par fonctionnalité (utilisateurs, trains, réservations)

### Exemples d'Utilisation

```sql
-- Récupérer tous les trains
SELECT id_train, train_number, source_station_name, destination_station_name
FROM train 
ORDER BY id_train 
LIMIT 50 OFFSET 0;

-- Récupérer les réservations d'un utilisateur
SELECT r.id_reservation, u.nom, u.prenom, t.train_number
FROM reservation r
JOIN utilisateur u ON r.id_user = u.id_user
JOIN train t ON r.id_train = t.id_train
WHERE r.id_user = 1;
```

## 🛠️ Maintenance

### Sauvegarde

```bash
# Sauvegarder la base de données
pg_dump -U trainuser -h localhost TrainStation > backup_trainstation.sql

# Restaurer la base de données
psql -U trainuser -h localhost TrainStation < backup_trainstation.sql
```

### Nettoyage

```sql
-- Supprimer toutes les données (ATTENTION : irréversible)
TRUNCATE TABLE reservation, train, utilisateur CASCADE;

-- Supprimer les tables (ATTENTION : irréversible)
DROP TABLE IF EXISTS reservation, train, utilisateur CASCADE;
```

## ❓ Dépannage

### Erreur de Connexion

```
psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: FATAL: role "trainuser" does not exist
```

**Solution :** Créer l'utilisateur PostgreSQL :
```sql
CREATE USER trainuser WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE "TrainStation" TO trainuser;
```

### Erreur de Base de Données

```
psycopg2.OperationalError: FATAL: database "TrainStation" does not exist
```

**Solution :** Créer la base de données :
```sql
CREATE DATABASE "TrainStation";
```

### Erreur de Privilèges

```
psycopg2.OperationalError: permission denied for table utilisateur
```

**Solution :** Donner les privilèges à l'utilisateur :
```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO trainuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO trainuser;
```

## 📚 Ressources

- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [psql Documentation](https://www.postgresql.org/docs/current/app-psql.html)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [DBeaver Documentation](https://dbeaver.com/docs/)

## 🔗 Liens Utiles

- [Retour au README principal](../README.md)
- [Configuration de l'application](../README.md#configuration)
- [Déploiement](../DEPLOYMENT.md)
