-- Optionnel : tout remettre à zéro proprement
DROP TABLE IF EXISTS reservation CASCADE;
DROP TABLE IF EXISTS train CASCADE;
DROP TABLE IF EXISTS utilisateur CASCADE;

-- ===== Table Utilisateur =====
CREATE TABLE utilisateur (
    id_user      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom          VARCHAR(100) NOT NULL,
    prenom       VARCHAR(100) NOT NULL,
    age          INT CHECK (age >= 0)
);

-- ===== Table Train (trajet + horaires) =====
CREATE TABLE train (
    id_train                      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    train_number                  VARCHAR NOT NULL,
    arrival_time                  TIME,
    departure_time                TIME,
    distance                      INT CHECK (distance >= 0),
    source_station_code           VARCHAR(50),
    source_station_name           VARCHAR(200),
    destination_station_code      VARCHAR(50),
    destination_station_name      VARCHAR(200)
);

-- ===== Table de Réservation (association N:N) =====
CREATE TABLE reservation (
    id_reservation  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_user         INT NOT NULL,
    id_train        INT NOT NULL,
    CONSTRAINT fk_res_user
        FOREIGN KEY (id_user)  REFERENCES utilisateur(id_user) ON DELETE CASCADE,
    CONSTRAINT fk_res_train
        FOREIGN KEY (id_train) REFERENCES train(id_train)      ON DELETE CASCADE
    -- Empêche les doublons de réservation pour le même couple (user, train)
    -- CONSTRAINT uq_res_user_train UNIQUE (id_user, id_train)
);

-- Index utiles (en plus des PK/UK) pour accélérer les recherches par FK
-- CREATE INDEX idx_reservation_id_user  ON reservation(id_user);
-- CREATE INDEX idx_reservation_id_train ON reservation(id_train);

-- (Optionnel) Quelques commentaires pour la doc interne
COMMENT ON TABLE utilisateur  IS 'Utilisateurs finaux';
COMMENT ON TABLE train        IS 'Trajets (point A->B) et horaires';
COMMENT ON TABLE reservation  IS 'Réservations liant utilisateurs et trains';

-- Creation d'une table de stagging pour transformer les données
CREATE TABLE train_stage (
    train_number                  VARCHAR,
    station_code                  VARCHAR,
    station_name                  VARCHAR,
    arrival_time                  VARCHAR,
    departure_time                VARCHAR,
    distance                      VARCHAR,
    source_station_code           VARCHAR,
    source_station_name           VARCHAR,
    destination_station_code      VARCHAR,
    destination_station_name      VARCHAR
);

-- Copy des données dans la table de staging (utilisation de l'assistant)

-- Transformation de type de colonnes en TIME 
ALTER TABLE train
    ALTER COLUMN arrival_time TYPE TIME USING arrival_time::timestamp::time,
    ALTER COLUMN departure_time TYPE TIME USING departure_time::timestamp::time;

-- Suppression des valeurs aberrante 
DELETE FROM train_stage where train_number = 'K'

-- Premierement on veut la première ligne pour chaque trajet --> couple(train_number,source_station, 
--										destionation_station, departure_time)
-- On vérifie les doublons
SELECT count(distinct train_number)
FROM train_stage
--  ==> Résultat : 11 112  Train number unique

SELECT count(distinct (train_number, source_station_code ,destination_station_code))
FROM train_stage
-- ==> Résultat : 11 117 Train number unique

-- Pour vérifier quels sont les train_number en double
SELECT count(distinct (t1.train_number, t1.source_station_code ,t1.destination_station_code)),
t1.train_number
FROM train_stage t1
join train_stage t2 on (t1.train_number = t2.train_number)
group by t1.train_number
order by count(distinct (t1.train_number, t1.source_station_code ,t1.destination_station_code)) desc

-- Vérifier que c'est les bonnes lignes
select *
from train_stage
where source_station_code is null
or destination_station_code is null;

-- Supprimer les doublons 
DELETE FROM train_stage 
where source_station_code is null
or destination_station_code is null;

-- Requete pour récupérer la première ligne
SELECT DISTINCT train_number,source_station_code,destination_station_code,
       FIRST_VALUE(departure_time) OVER (PARTITION BY train_number ORDER BY train_number,source_station_code,destination_station_code ASC)  AS departure_time                     
FROM train_stage

-- Ensuite on veut la dernière ligne pour chaque trajet -->  couple(train_number,source_station,
--									destination_station,distance,arrival_time)
SELECT DISTINCT train_number,source_station_code,destination_station_code,
       LAST_VALUE(arrival_time) OVER (PARTITION BY train_number ORDER BY train_number,source_station_code,destination_station_code ASC)  AS arrival_time,
	   LAST_VALUE(distance) OVER (PARTITION BY train_number ORDER BY train_number,source_station_code,destination_station_code ASC)  AS distance
FROM train_stage;


-- Créer une table avec ces deux tables contenant toutes les colonnes dont on a besoin.
-- 
with info_depart as (
SELECT DISTINCT train_number,source_station_code,destination_station_code,
       FIRST_VALUE(departure_time) OVER (PARTITION BY train_number ORDER BY train_number,source_station_code,destination_station_code ASC)  AS departure_time                     
FROM train_stage
),

info_arrivee as(
SELECT DISTINCT train_number,source_station_code,destination_station_code,
       LAST_VALUE(arrival_time) OVER (PARTITION BY train_number ORDER BY train_number,source_station_code,destination_station_code ASC)  AS arrival_time,
	   LAST_VALUE(distance) OVER (PARTITION BY train_number ORDER BY train_number,source_station_code,destination_station_code ASC)  AS distance
FROM train_stage

)
select distinct
	de.train_number,
	de.source_station_code,
	stg.source_station_name,
	de.destination_station_code,
	stg.destination_station_name,
	de.departure_time,
	ar.arrival_time,
	ar.distance
from info_depart de 
left join info_arrivee ar on (de.train_number = ar.train_number)
left join train_stage stg on (stg.train_number = de.train_number) 

ALTER TABLE train
    ALTER COLUMN arrival_time TYPE TIME USING arrival_time::timestamp::time,
    ALTER COLUMN departure_time TYPE TIME USING departure_time::timestamp::time;


-- Insertion des données
insert into train (
	train_number,                 
    arrival_time,               
    departure_time,               
    distance,                     
    source_station_code  ,         
    source_station_name,           
    destination_station_code   ,   
    destination_station_name      
)
(
with info_depart as (
SELECT DISTINCT train_number,source_station_code,destination_station_code,
       FIRST_VALUE(departure_time) OVER (PARTITION BY train_number ORDER BY train_number,source_station_code,destination_station_code ASC)  AS departure_time                     
FROM train_stage
),

info_arrivee as(
SELECT DISTINCT train_number,source_station_code,destination_station_code,
       LAST_VALUE(arrival_time) OVER (PARTITION BY train_number ORDER BY train_number,source_station_code,destination_station_code ASC)  AS arrival_time,
	   LAST_VALUE(distance) OVER (PARTITION BY train_number ORDER BY train_number,source_station_code,destination_station_code ASC)  AS distance
FROM train_stage

)
select distinct
	de.train_number,
	NULLIF(ar.arrival_time, '00:00:00')::time as arrival_time,
	NULLIF(de.departure_time, '00:00:00')::time as departure_time,
	ar.distance::integer,
	de.source_station_code,
	stg.source_station_name,
	de.destination_station_code,
	stg.destination_station_name
from info_depart de 
left join info_arrivee ar on (de.train_number = ar.train_number)
left join train_stage stg on (stg.train_number = de.train_number)

)



