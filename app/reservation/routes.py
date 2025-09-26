from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db
from app.models import Reservation, Train, User
from app.forms import ReservationForm, ReservationSearchForm
from app.database.queries import DatabaseQueries

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('/')
def list_reservations():
    user_id = session.get('user_id')
    if not user_id:
        flash('Vous devez être connecté pour voir vos réservations.', 'error')
        return redirect(url_for('auth.login'))
    
    db_queries = DatabaseQueries()
    reservations = db_queries.get_user_reservations(user_id)
    return render_template('reservation/list.html', reservations=reservations)

@reservation_bp.route('/add', methods=['GET', 'POST'])
def add_reservation():
    user_id = session.get('user_id')
    if not user_id:
        flash('Vous devez être connecté pour faire une réservation.', 'error')
        return redirect(url_for('auth.login'))
    
    db_queries = DatabaseQueries()
    search_form = ReservationSearchForm()
    
    # Remplir les listes déroulantes
    stations = db_queries.get_unique_stations()
    search_form.source_station.choices = [('', 'Sélectionner une gare')] + [(station['station_name'], station['station_name']) for station in stations]
    search_form.destination_station.choices = [('', 'Sélectionner une gare')] + [(station['station_name'], station['station_name']) for station in stations]
    
    # Remplir les listes d'heures et de minutes
    search_form.departure_hour.choices = [('', 'Heure')] + [(str(i).zfill(2), str(i).zfill(2)) for i in range(24)]
    search_form.departure_minute.choices = [('', 'Minute')] + [(str(i).zfill(2), str(i).zfill(2)) for i in range(0, 60, 5)]  # Par pas de 5 minutes
    
    trains = []
    if search_form.validate_on_submit():
        # Construire l'heure de départ si les deux champs sont remplis
        departure_time = None
        if search_form.departure_hour.data and search_form.departure_minute.data:
            departure_time = f"{search_form.departure_hour.data}:{search_form.departure_minute.data}"
        
        trains = db_queries.search_trains_by_criteria(
            search_form.source_station.data,
            search_form.destination_station.data,
            departure_time
        )
    
    return render_template('reservation/add.html', search_form=search_form, trains=trains)

@reservation_bp.route('/book/<int:train_id>', methods=['POST'])
def book_train(train_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Vous devez être connecté pour faire une réservation.', 'error')
        return redirect(url_for('auth.login'))
    
    db_queries = DatabaseQueries()
    success = db_queries.create_reservation(user_id, train_id)
    
    if success:
        flash('Réservation effectuée avec succès!', 'success')
    else:
        flash('Vous avez déjà réservé ce train ou une erreur s\'est produite!', 'error')
    
    return redirect(url_for('reservation.list_reservations'))

@reservation_bp.route('/<int:reservation_id>/cancel', methods=['POST'])
def cancel_reservation(reservation_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Vous devez être connecté.', 'error')
        return redirect(url_for('auth.login'))
    
    db_queries = DatabaseQueries()
    success = db_queries.cancel_reservation(reservation_id, user_id)
    
    if success:
        flash('Réservation annulée avec succès!', 'success')
    else:
        flash('Réservation non trouvée ou erreur lors de l\'annulation.', 'error')
    
    return redirect(url_for('reservation.list_reservations'))

@reservation_bp.route('/api/available-destinations')
def get_available_destinations():
    """API endpoint pour récupérer les gares d'arrivée disponibles pour une gare de départ donnée"""
    source_station = request.args.get('source_station')
    db_queries = DatabaseQueries()
    
    if not source_station:
        # Si aucune gare de départ n'est spécifiée, retourner toutes les gares d'arrivée
        destinations = db_queries.get_unique_stations()
        # Filtrer pour ne garder que les gares d'arrivée
        arrival_stations = []
        for station in destinations:
            arrival_stations.append({
                'destination_station_name': station['station_name'],
                'destination_station_code': station['station_code']
            })
        return jsonify(arrival_stations)
    
    destinations = db_queries.get_available_destinations(source_station)
    return jsonify(destinations)

@reservation_bp.route('/api/available-sources')
def get_available_sources():
    """API endpoint pour récupérer les gares de départ disponibles pour une gare d'arrivée donnée"""
    destination_station = request.args.get('destination_station')
    db_queries = DatabaseQueries()
    
    if not destination_station:
        # Si aucune gare d'arrivée n'est spécifiée, retourner toutes les gares de départ
        sources = db_queries.get_unique_stations()
        # Filtrer pour ne garder que les gares de départ
        departure_stations = []
        for station in sources:
            departure_stations.append({
                'source_station_name': station['station_name'],
                'source_station_code': station['station_code']
            })
        return jsonify(departure_stations)
    
    sources = db_queries.get_available_sources(destination_station)
    return jsonify(sources)
