from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Reservation, Train, User
from app.forms import ReservationForm
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
    
    form = ReservationForm()
    # Remplir les choix de trains avec les données de votre base PostgreSQL
    form.train_id.choices = [(train.id_train, train.display_name) 
                             for train in Train.query.all()]
    
    if form.validate_on_submit():
        db_queries = DatabaseQueries()
        reservation_id = db_queries.create_reservation(user_id, form.train_id.data)
        
        if reservation_id:
            flash('Réservation effectuée avec succès!', 'success')
            return redirect(url_for('reservation.list_reservations'))
        else:
            flash('Vous avez déjà réservé ce train ou une erreur s\'est produite!', 'error')
            return redirect(url_for('reservation.add_reservation'))
    
    return render_template('reservation/add.html', form=form)

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
