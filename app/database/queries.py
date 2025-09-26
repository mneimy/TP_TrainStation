"""
Module de requêtes SQL sécurisées pour l'application Gare de Train
Toutes les requêtes utilisent des paramètres pour éviter les injections SQL
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import Config

class DatabaseQueries:
    """Classe pour gérer les requêtes SQL sécurisées"""
    
    def __init__(self):
        self.config = Config()
        self.connection_params = {
            'host': self.config.DB_HOST,
            'port': int(self.config.DB_PORT),
            'database': self.config.DB_NAME,
            'user': self.config.DB_USERNAME,
            'password': self.config.DB_PASSWORD
        }
    
    def get_connection(self):
        """Établit une connexion à la base de données"""
        try:
            conn = psycopg2.connect(**self.connection_params)
            return conn
        except psycopg2.Error as e:
            print(f"Erreur de connexion à PostgreSQL: {e}")
            return None
    
    def execute_query(self, query_name, params=None, fetch_one=False, fetch_all=False, commit=False):
        """Exécute une requête SQL sécurisée"""
        conn = self.get_connection()
        if not conn:
            return None

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Charger la requête depuis le fichier SQL
                query = self._load_query(query_name)
                if not query:
                    raise ValueError(f"Query '{query_name}' not found")
                
                cur.execute(query, params or ())
                
                if commit:
                    conn.commit()
                    return cur.rowcount
                elif fetch_one:
                    return cur.fetchone()
                elif fetch_all:
                    return cur.fetchall()
                else:
                    return None
        except psycopg2.Error as e:
            print(f"Erreur lors de l'exécution de la requête '{query_name}': {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def _load_query(self, query_name):
        """Charge une requête depuis le fichier SQL/queries.sql"""
        import os
        queries_path = os.path.join(os.path.dirname(__file__), '..', '..', 'SQL', 'queries.sql')
        
        try:
            with open(queries_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            queries = {}
            current_query_name = None
            current_query_lines = []

            for line in content.splitlines():
                if line.startswith('-- name:'):
                    if current_query_name and current_query_lines:
                        queries[current_query_name.strip()] = "\n".join(current_query_lines).strip()
                    current_query_name = line.split(':', 1)[1].strip()
                    current_query_lines = []
                elif current_query_name and line.strip():
                    current_query_lines.append(line)
            
            if current_query_name and current_query_lines:
                queries[current_query_name.strip()] = "\n".join(current_query_lines).strip()
            
            return queries.get(query_name)
        except Exception as e:
            print(f"Erreur lors du chargement de la requête '{query_name}': {e}")
            return None
    
    # ===========================================
    # REQUÊTES UTILISATEURS
    # ===========================================
    
    def get_user_by_credentials(self, nom, prenom, age):
        """Récupère un utilisateur par ses informations de connexion"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id_user, nom, prenom, age 
                    FROM utilisateur 
                    WHERE nom = %s AND prenom = %s AND age = %s
                """, (nom, prenom, age))
                return cur.fetchone()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération de l'utilisateur: {e}")
            return None
        finally:
            conn.close()
    
    def get_user_by_id(self, user_id):
        """Récupère un utilisateur par son ID"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id_user, nom, prenom, age 
                    FROM utilisateur 
                    WHERE id_user = %s
                """, (user_id,))
                return cur.fetchone()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération de l'utilisateur: {e}")
            return None
        finally:
            conn.close()
    
    def create_user(self, nom, prenom, age):
        """Crée un nouvel utilisateur"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO utilisateur (nom, prenom, age) 
                    VALUES (%s, %s, %s) 
                    RETURNING id_user
                """, (nom, prenom, age))
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id
        except psycopg2.Error as e:
            print(f"Erreur lors de la création de l'utilisateur: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def user_exists(self, nom, prenom, age):
        """Vérifie si un utilisateur existe déjà"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM utilisateur 
                    WHERE nom = %s AND prenom = %s AND age = %s
                """, (nom, prenom, age))
                count = cur.fetchone()[0]
                return count > 0
        except psycopg2.Error as e:
            print(f"Erreur lors de la vérification de l'utilisateur: {e}")
            return False
        finally:
            conn.close()
    
    # ===========================================
    # REQUÊTES TRAINS
    # ===========================================
    
    def get_all_trains(self, limit=50, offset=0):
        """Récupère tous les trains avec pagination"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id_train, train_number, source_station_name, destination_station_name, 
                           departure_time, arrival_time, distance, source_station_code, destination_station_code
                    FROM train 
                    ORDER BY id_train 
                    LIMIT %s OFFSET %s
                """, (limit, offset))
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des trains: {e}")
            return []
        finally:
            conn.close()
    
    def get_train_by_id(self, train_id):
        """Récupère un train par son ID"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id_train, train_number, source_station_name, destination_station_name, 
                           departure_time, arrival_time, distance, source_station_code, destination_station_code
                    FROM train 
                    WHERE id_train = %s
                """, (train_id,))
                return cur.fetchone()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération du train: {e}")
            return None
        finally:
            conn.close()
    
    def search_trains(self, source_station=None, destination_station=None, train_number=None):
        """Recherche des trains par critères"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Construction dynamique de la requête
                query = """
                    SELECT id_train, train_number, source_station_name, destination_station_name, 
                           departure_time, arrival_time, distance
                    FROM train 
                    WHERE 1=1
                """
                params = []
                
                if source_station:
                    query += " AND source_station_name ILIKE %s"
                    params.append(f"%{source_station}%")
                
                if destination_station:
                    query += " AND destination_station_name ILIKE %s"
                    params.append(f"%{destination_station}%")
                
                if train_number:
                    query += " AND train_number ILIKE %s"
                    params.append(f"%{train_number}%")
                
                query += " ORDER BY departure_time"
                
                cur.execute(query, params)
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Erreur lors de la recherche de trains: {e}")
            return []
        finally:
            conn.close()
    
    def get_trains_count(self):
        """Compte le nombre total de trains"""
        conn = self.get_connection()
        if not conn:
            return 0
        
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM train")
                return cur.fetchone()[0]
        except psycopg2.Error as e:
            print(f"Erreur lors du comptage des trains: {e}")
            return 0
        finally:
            conn.close()
    
    # ===========================================
    # REQUÊTES RÉSERVATIONS
    # ===========================================
    
    def get_user_reservations(self, user_id):
        """Récupère les réservations d'un utilisateur"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT r.id_reservation, r.id_user, r.id_train,
                           u.nom, u.prenom, u.age,
                           t.train_number, t.source_station_name, t.destination_station_name,
                           t.departure_time, t.arrival_time, t.distance
                    FROM reservation r
                    JOIN utilisateur u ON r.id_user = u.id_user
                    JOIN train t ON r.id_train = t.id_train
                    WHERE r.id_user = %s
                    ORDER BY r.id_reservation DESC
                """, (user_id,))
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des réservations: {e}")
            return []
        finally:
            conn.close()
    
    def create_reservation(self, user_id, train_id):
        """Crée une nouvelle réservation"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cur:
                # Vérifier si la réservation existe déjà
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM reservation 
                    WHERE id_user = %s AND id_train = %s
                """, (user_id, train_id))
                
                if cur.fetchone()[0] > 0:
                    return False  # Réservation déjà existante
                
                cur.execute("""
                    INSERT INTO reservation (id_user, id_train) 
                    VALUES (%s, %s)
                """, (user_id, train_id))
                conn.commit()
                return True
        except psycopg2.Error as e:
            print(f"Erreur lors de la création de la réservation: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def cancel_reservation(self, reservation_id, user_id):
        """Annule une réservation"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM reservation 
                    WHERE id_reservation = %s AND id_user = %s
                """, (reservation_id, user_id))
                deleted_count = cur.rowcount
                conn.commit()
                return deleted_count > 0
        except psycopg2.Error as e:
            print(f"Erreur lors de l'annulation de la réservation: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def search_trains_by_criteria(self, source_station, destination_station, departure_time=None):
        """Recherche des trains par critères"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                departure_pattern = f"%{departure_time}%" if departure_time else None
                cur.execute("""
                    SELECT DISTINCT t.id_train, t.train_number, t.source_station_name, t.destination_station_name, 
                           t.departure_time, t.arrival_time, t.distance
                    FROM train t
                    WHERE t.source_station_name ILIKE %s
                      AND t.destination_station_name ILIKE %s
                      AND (t.departure_time::text LIKE %s OR %s IS NULL)
                    ORDER BY t.departure_time
                """, (f"%{source_station}%", f"%{destination_station}%", 
                      departure_pattern, departure_pattern))
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Erreur lors de la recherche de trains: {e}")
            return []
        finally:
            conn.close()

    def get_unique_stations(self):
        """Récupère toutes les gares uniques"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
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
                    ORDER BY station_name
                """)
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des gares: {e}")
            return []
        finally:
            conn.close()

    def get_departure_times(self):
        """Récupère tous les horaires de départ uniques"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT DISTINCT departure_time
                    FROM train
                    WHERE departure_time IS NOT NULL
                    ORDER BY departure_time
                """)
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des horaires: {e}")
            return []
        finally:
            conn.close()
    
    def get_available_trains_for_user(self, user_id, source_station=None, destination_station=None):
        """Récupère les trains disponibles pour un utilisateur (non réservés)"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT t.id_train, t.train_number, t.source_station_name, t.destination_station_name, 
                           t.departure_time, t.arrival_time, t.distance
                    FROM train t
                    WHERE t.id_train NOT IN (
                        SELECT r.id_train 
                        FROM reservation r 
                        WHERE r.id_user = %s
                    )
                """
                params = [user_id]
                
                if source_station:
                    query += " AND t.source_station_name ILIKE %s"
                    params.append(f"%{source_station}%")
                
                if destination_station:
                    query += " AND t.destination_station_name ILIKE %s"
                    params.append(f"%{destination_station}%")
                
                query += " ORDER BY t.departure_time"
                
                cur.execute(query, params)
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des trains disponibles: {e}")
            return []
        finally:
            conn.close()
    
    # ===========================================
    # REQUÊTES DE STATISTIQUES
    # ===========================================
    
    def get_database_stats(self):
        """Récupère les statistiques générales de la base de données"""
        conn = self.get_connection()
        if not conn:
            return {}
        
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        (SELECT COUNT(*) FROM utilisateur) as total_users,
                        (SELECT COUNT(*) FROM train) as total_trains,
                        (SELECT COUNT(*) FROM reservation) as total_reservations
                """)
                result = cur.fetchone()
                return {
                    'total_users': result[0],
                    'total_trains': result[1],
                    'total_reservations': result[2]
                }
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des statistiques: {e}")
            return {}
        finally:
            conn.close()
    
    def get_top_trains(self, limit=5):
        """Récupère les trains les plus réservés"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT t.train_number, t.source_station_name, t.destination_station_name,
                           COUNT(r.id_reservation) as reservation_count
                    FROM train t
                    LEFT JOIN reservation r ON t.id_train = r.id_train
                    GROUP BY t.id_train, t.train_number, t.source_station_name, t.destination_station_name
                    ORDER BY reservation_count DESC
                    LIMIT %s
                """, (limit,))
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Erreur lors de la récupération des top trains: {e}")
            return []
        finally:
            conn.close()
