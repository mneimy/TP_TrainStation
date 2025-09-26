-- ===========================================
-- REQUÊTES SQL SÉCURISÉES - GARE DE TRAIN
-- ===========================================
-- Ce fichier contient toutes les requêtes SQL utilisées par l'application
-- Toutes les requêtes utilisent des paramètres pour éviter les injections SQL

-- ===========================================
-- REQUÊTES UTILISATEURS
-- ===========================================

-- Récupérer un utilisateur par ses informations de connexion
-- Paramètres: nom, prenom, age
SELECT id_user, nom, prenom, age 
FROM utilisateur 
WHERE nom = %s AND prenom = %s AND age = %s;

-- Récupérer un utilisateur par ID
-- Paramètres: id_user
SELECT id_user, nom, prenom, age 
FROM utilisateur 
WHERE id_user = %s;

-- Créer un nouvel utilisateur
-- Paramètres: nom, prenom, age
INSERT INTO utilisateur (nom, prenom, age) 
VALUES (%s, %s, %s);

-- Vérifier si un utilisateur existe déjà
-- Paramètres: nom, prenom, age
SELECT COUNT(*) 
FROM utilisateur 
WHERE nom = %s AND prenom = %s AND age = %s;

-- Récupérer tous les utilisateurs (avec pagination)
-- Paramètres: limit, offset
SELECT id_user, nom, prenom, age 
FROM utilisateur 
ORDER BY id_user 
LIMIT %s OFFSET %s;

-- Compter le nombre total d'utilisateurs
SELECT COUNT(*) FROM utilisateur;

-- ===========================================
-- REQUÊTES TRAINS
-- ===========================================

-- Récupérer tous les trains (avec pagination)
-- Paramètres: limit, offset
SELECT id_train, train_number, source_station_name, destination_station_name, 
       departure_time, arrival_time, distance, source_station_code, destination_station_code
FROM train 
ORDER BY id_train 
LIMIT %s OFFSET %s;

-- Récupérer un train par ID
-- Paramètres: id_train
SELECT id_train, train_number, source_station_name, destination_station_name, 
       departure_time, arrival_time, distance, source_station_code, destination_station_code
FROM train 
WHERE id_train = %s;

-- Rechercher des trains par gare de départ
-- Paramètres: source_station_name
SELECT id_train, train_number, source_station_name, destination_station_name, 
       departure_time, arrival_time, distance
FROM train 
WHERE source_station_name ILIKE %s 
ORDER BY departure_time;

-- Rechercher des trains par gare d'arrivée
-- Paramètres: destination_station_name
SELECT id_train, train_number, source_station_name, destination_station_name, 
       departure_time, arrival_time, distance
FROM train 
WHERE destination_station_name ILIKE %s 
ORDER BY departure_time;

-- Rechercher des trains par trajet (départ -> arrivée)
-- Paramètres: source_station_name, destination_station_name
SELECT id_train, train_number, source_station_name, destination_station_name, 
       departure_time, arrival_time, distance
FROM train 
WHERE source_station_name ILIKE %s AND destination_station_name ILIKE %s
ORDER BY departure_time;

-- Rechercher des trains par numéro
-- Paramètres: train_number
SELECT id_train, train_number, source_station_name, destination_station_name, 
       departure_time, arrival_time, distance
FROM train 
WHERE train_number ILIKE %s 
ORDER BY id_train;

-- Créer un nouveau train
-- Paramètres: train_number, source_station_code, source_station_name, 
--            destination_station_code, destination_station_name, 
--            departure_time, arrival_time, distance
INSERT INTO train (train_number, source_station_code, source_station_name, 
                  destination_station_code, destination_station_name, 
                  departure_time, arrival_time, distance) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);

-- Mettre à jour un train
-- Paramètres: train_number, source_station_code, source_station_name, 
--            destination_station_code, destination_station_name, 
--            departure_time, arrival_time, distance, id_train
UPDATE train 
SET train_number = %s, 
    source_station_code = %s, 
    source_station_name = %s, 
    destination_station_code = %s, 
    destination_station_name = %s, 
    departure_time = %s, 
    arrival_time = %s, 
    distance = %s 
WHERE id_train = %s;

-- Supprimer un train
-- Paramètres: id_train
DELETE FROM train WHERE id_train = %s;

-- Compter le nombre total de trains
SELECT COUNT(*) FROM train;

-- ===========================================
-- REQUÊTES RÉSERVATIONS
-- ===========================================

-- Récupérer les réservations d'un utilisateur
-- Paramètres: id_user
SELECT r.id_reservation, r.id_user, r.id_train,
       u.nom, u.prenom, u.age,
       t.train_number, t.source_station_name, t.destination_station_name,
       t.departure_time, t.arrival_time, t.distance
FROM reservation r
JOIN utilisateur u ON r.id_user = u.id_user
JOIN train t ON r.id_train = t.id_train
WHERE r.id_user = %s
ORDER BY r.id_reservation;

-- Récupérer une réservation par ID
-- Paramètres: id_reservation
SELECT r.id_reservation, r.id_user, r.id_train,
       u.nom, u.prenom, u.age,
       t.train_number, t.source_station_name, t.destination_station_name,
       t.departure_time, t.arrival_time, t.distance
FROM reservation r
JOIN utilisateur u ON r.id_user = u.id_user
JOIN train t ON r.id_train = t.id_train
WHERE r.id_reservation = %s;

-- Vérifier si une réservation existe déjà (utilisateur + train)
-- Paramètres: id_user, id_train
SELECT COUNT(*) 
FROM reservation 
WHERE id_user = %s AND id_train = %s;

-- Créer une nouvelle réservation
-- Paramètres: id_user, id_train
INSERT INTO reservation (id_user, id_train) 
VALUES (%s, %s);

-- Supprimer une réservation
-- Paramètres: id_reservation
DELETE FROM reservation WHERE id_reservation = %s;

-- Supprimer une réservation d'un utilisateur spécifique
-- Paramètres: id_reservation, id_user
DELETE FROM reservation 
WHERE id_reservation = %s AND id_user = %s;

-- name: get_reservations_by_user
-- Récupérer les réservations d'un utilisateur spécifique
-- Paramètres: id_user
SELECT r.id_reservation, r.id_user, r.id_train,
       u.nom, u.prenom, u.age,
       t.train_number, t.source_station_name, t.destination_station_name,
       t.departure_time, t.arrival_time, t.distance
FROM reservation r
JOIN utilisateur u ON r.id_user = u.id_user
JOIN train t ON r.id_train = t.id_train
WHERE r.id_user = %s
ORDER BY r.id_reservation DESC;

-- Récupérer toutes les réservations (avec pagination)
-- Paramètres: limit, offset
SELECT r.id_reservation, r.id_user, r.id_train,
       u.nom, u.prenom, u.age,
       t.train_number, t.source_station_name, t.destination_station_name,
       t.departure_time, t.arrival_time, t.distance
FROM reservation r
JOIN utilisateur u ON r.id_user = u.id_user
JOIN train t ON r.id_train = t.id_train
ORDER BY r.id_reservation
LIMIT %s OFFSET %s;

-- Compter le nombre total de réservations
SELECT COUNT(*) FROM reservation;

-- Compter les réservations d'un utilisateur
-- Paramètres: id_user
SELECT COUNT(*) FROM reservation WHERE id_user = %s;

-- ===========================================
-- REQUÊTES DE STATISTIQUES
-- ===========================================

-- Statistiques générales
SELECT 
    (SELECT COUNT(*) FROM utilisateur) as total_users,
    (SELECT COUNT(*) FROM train) as total_trains,
    (SELECT COUNT(*) FROM reservation) as total_reservations;

-- Top 5 des trains les plus réservés
SELECT t.train_number, t.source_station_name, t.destination_station_name,
       COUNT(r.id_reservation) as reservation_count
FROM train t
LEFT JOIN reservation r ON t.id_train = r.id_train
GROUP BY t.id_train, t.train_number, t.source_station_name, t.destination_station_name
ORDER BY reservation_count DESC
LIMIT 5;

-- Top 5 des utilisateurs les plus actifs
SELECT u.nom, u.prenom, COUNT(r.id_reservation) as reservation_count
FROM utilisateur u
LEFT JOIN reservation r ON u.id_user = r.id_user
GROUP BY u.id_user, u.nom, u.prenom
ORDER BY reservation_count DESC
LIMIT 5;

-- Répartition des réservations par âge
SELECT 
    CASE 
        WHEN age < 25 THEN '18-24'
        WHEN age < 35 THEN '25-34'
        WHEN age < 45 THEN '35-44'
        WHEN age < 55 THEN '45-54'
        ELSE '55+'
    END as age_group,
    COUNT(r.id_reservation) as reservation_count
FROM utilisateur u
LEFT JOIN reservation r ON u.id_user = r.id_user
GROUP BY age_group
ORDER BY age_group;

-- ===========================================
-- REQUÊTES DE RECHERCHE AVANCÉE
-- ===========================================

-- Recherche de trains par critères multiples
-- Paramètres: source_station_name, destination_station_name, min_distance, max_distance
SELECT id_train, train_number, source_station_name, destination_station_name, 
       departure_time, arrival_time, distance
FROM train 
WHERE (source_station_name ILIKE %s OR %s IS NULL)
  AND (destination_station_name ILIKE %s OR %s IS NULL)
  AND (distance >= %s OR %s IS NULL)
  AND (distance <= %s OR %s IS NULL)
ORDER BY departure_time;

-- Recherche de trains disponibles (non réservés par un utilisateur)
-- Paramètres: id_user, source_station_name, destination_station_name
SELECT t.id_train, t.train_number, t.source_station_name, t.destination_station_name, 
       t.departure_time, t.arrival_time, t.distance
FROM train t
WHERE t.id_train NOT IN (
    SELECT r.id_train 
    FROM reservation r 
    WHERE r.id_user = %s
)
AND (t.source_station_name ILIKE %s OR %s IS NULL)
AND (t.destination_station_name ILIKE %s OR %s IS NULL)
ORDER BY t.departure_time;

-- name: search_trains_by_criteria
-- Recherche de trains par critères de recherche
-- Paramètres: source_station_name, destination_station_name, departure_time
SELECT DISTINCT t.id_train, t.train_number, t.source_station_name, t.destination_station_name, 
       t.departure_time, t.arrival_time, t.distance
FROM train t
WHERE t.source_station_name ILIKE %s
  AND t.destination_station_name ILIKE %s
  AND (t.departure_time::text LIKE %s OR %s IS NULL)
ORDER BY t.departure_time;

-- name: get_unique_stations
-- Récupère toutes les gares uniques (départ et arrivée)
SELECT DISTINCT station_name, station_code
FROM (
    SELECT source_station_name as station_name, source_station_code as station_code
    FROM train
    WHERE source_station_name IS NOT NULL
    UNION
    SELECT destination_station_name as station_name, destination_station_code as station_code
    FROM train
    WHERE destination_station_name IS NOT NULL
) stations
ORDER BY station_name;

-- name: get_departure_times
-- Récupère tous les horaires de départ uniques
SELECT DISTINCT departure_time
FROM train
WHERE departure_time IS NOT NULL
ORDER BY departure_time;

-- ===========================================
-- REQUÊTES DE MAINTENANCE
-- ===========================================

-- Nettoyer les réservations orphelines (utilisateur ou train supprimé)
DELETE FROM reservation 
WHERE id_user NOT IN (SELECT id_user FROM utilisateur)
   OR id_train NOT IN (SELECT id_train FROM train);

-- Vérifier l'intégrité des données
SELECT 
    'Orphelins utilisateur' as type,
    COUNT(*) as count
FROM reservation r
WHERE r.id_user NOT IN (SELECT id_user FROM utilisateur)
UNION ALL
SELECT 
    'Orphelins train' as type,
    COUNT(*) as count
FROM reservation r
WHERE r.id_train NOT IN (SELECT id_train FROM train);

-- ===========================================
-- REQUÊTES D'EXPORT
-- ===========================================

-- Export des réservations avec détails complets
-- Paramètres: date_debut, date_fin (optionnel)
SELECT 
    r.id_reservation,
    u.nom as user_nom,
    u.prenom as user_prenom,
    u.age as user_age,
    t.train_number,
    t.source_station_name,
    t.destination_station_name,
    t.departure_time,
    t.arrival_time,
    t.distance
FROM reservation r
JOIN utilisateur u ON r.id_user = u.id_user
JOIN train t ON r.id_train = t.id_train
-- WHERE r.created_at >= %s AND r.created_at <= %s  -- Si vous ajoutez des timestamps
ORDER BY r.id_reservation;
