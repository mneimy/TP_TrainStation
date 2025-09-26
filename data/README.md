# 📊 Données - Gare de Train

Ce répertoire contient les données utilisées par l'application Gare de Train.

## 📁 Contenu

- `Train_details.csv` - Base de données des trains avec leurs détails complets
- `README.md` - Ce fichier de documentation

## 📋 Description des Données

### Train_details.csv

Ce fichier contient les informations détaillées de tous les trains avec les colonnes suivantes :

| Colonne | Description | Type |
|---------|-------------|------|
| `train_number` | Numéro du train | String |
| `station_code` | Code de la gare | String |
| `station_name` | Nom de la gare | String |
| `arrival_time` | Heure d'arrivée | Time (HH:MM:SS) |
| `departure_time` | Heure de départ | Time (HH:MM:SS) |
| `distance` | Distance depuis la gare source | Integer (km) |
| `source_station_code` | Code de la gare de départ | String |
| `source_station_name` | Nom de la gare de départ | String |
| `destination_station_code` | Code de la gare d'arrivée | String |
| `destination_station_name` | Nom de la gare d'arrivée | String |

## 🔄 Import des Données

### Méthode 1 : Via l'application Flask

L'application peut importer automatiquement ces données lors de l'initialisation :

```python
# Dans app/__init__.py ou un script d'import
import pandas as pd
from app import db
from app.models import Train

def import_train_data():
    df = pd.read_csv('data/Train_details.csv')
    for _, row in df.iterrows():
        train = Train(
            train_number=row['train_number'],
            source_station_code=row['source_station_code'],
            source_station_name=row['source_station_name'],
            destination_station_code=row['destination_station_code'],
            destination_station_name=row['destination_station_name'],
            departure_time=row['departure_time'],
            arrival_time=row['arrival_time'],
            distance=row['distance']
        )
        db.session.add(train)
    db.session.commit()
```

### Méthode 2 : Via PostgreSQL directement

```sql
-- Créer une table temporaire pour l'import
CREATE TEMP TABLE temp_trains (
    train_number VARCHAR,
    station_code VARCHAR,
    station_name VARCHAR,
    arrival_time TIME,
    departure_time TIME,
    distance INTEGER,
    source_station_code VARCHAR,
    source_station_name VARCHAR,
    destination_station_code VARCHAR,
    destination_station_name VARCHAR
);

-- Importer le CSV (nécessite une extension comme file_fdw)
COPY temp_trains FROM '/chemin/vers/data/Train_details.csv' 
WITH (FORMAT csv, HEADER true);

-- Insérer dans la table train (en supprimant les doublons)
INSERT INTO train (train_number, source_station_code, source_station_name, 
                  destination_station_code, destination_station_name, 
                  departure_time, arrival_time, distance)
SELECT DISTINCT 
    train_number,
    source_station_code,
    source_station_name,
    destination_station_code,
    destination_station_name,
    departure_time,
    arrival_time,
    distance
FROM temp_trains
WHERE departure_time != '00:00:00'  -- Éviter les gares intermédiaires
ON CONFLICT DO NOTHING;
```

## 📊 Statistiques des Données

- **Nombre total de lignes** : ~11,000+ enregistrements
- **Nombre de trains uniques** : Variable selon les données
- **Gares couvertes** : Toutes les gares du réseau ferroviaire
- **Période** : Données actuelles du réseau

## 🔧 Utilisation

Ces données sont utilisées par l'application pour :

1. **Affichage des trains** disponibles
2. **Recherche de trains** par gare de départ/arrivée
3. **Calcul des distances** et temps de trajet
4. **Gestion des réservations** avec les trains réels

## ⚠️ Notes Importantes

- Les données sont **publiques** et peuvent être partagées
- Le fichier est **volumineux** (~14MB) - considérer la compression pour Git
- Les données peuvent être **mises à jour** périodiquement
- Vérifier la **cohérence** des données avant import

## 🔗 Liens Utiles

- [Retour au README principal](../README.md)
- [Configuration de la base de données](../SQL/README.md)
- [Documentation de l'application](../README.md#utilisation)
