from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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
    
    departure_times = db_queries.get_departure_times()
    search_form.departure_time.choices = [('', 'Tous les horaires')] + [(time['departure_time'].strftime('%H:%M'), time['departure_time'].strftime('%H:%M')) for time in departure_times]
    
    trains = []
    if search_form.validate_on_submit():
        trains = db_queries.search_trains_by_criteria(
            search_form.source_station.data,
            search_form.destination_station.data,
            search_form.departure_time.data
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
