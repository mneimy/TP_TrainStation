from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Train
from app.forms import TrainForm, TrainSearchForm
from app.database.queries import DatabaseQueries

train_bp = Blueprint('train', __name__)

@train_bp.route('/', methods=['GET', 'POST'])
def list_trains():
    db_queries = DatabaseQueries()
    search_form = TrainSearchForm()
    
    # Remplir les listes déroulantes
    stations = db_queries.get_unique_stations()
    search_form.source_station.choices = [('', 'Toutes les gares')] + [(station['station_name'], station['station_name']) for station in stations]
    search_form.destination_station.choices = [('', 'Toutes les gares')] + [(station['station_name'], station['station_name']) for station in stations]
    
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
            search_form.source_station.data or '',
            search_form.destination_station.data or '',
            departure_time
        )
    else:
        # Afficher tous les trains par défaut
        trains = db_queries.get_all_trains()
    
    return render_template('train/list.html', trains=trains, search_form=search_form)

@train_bp.route('/add', methods=['GET', 'POST'])
def add_train():
    form = TrainForm()
    if form.validate_on_submit():
        train = Train(
            train_number=form.train_number.data,
            source_station_code=form.source_station_code.data,
            source_station_name=form.source_station_name.data,
            destination_station_code=form.destination_station_code.data,
            destination_station_name=form.destination_station_name.data,
            departure_time=form.departure_time.data,
            arrival_time=form.arrival_time.data,
            distance=form.distance.data
        )
        db.session.add(train)
        db.session.commit()
        flash('Train ajouté avec succès!', 'success')
        return redirect(url_for('train.list_trains'))
    return render_template('train/add.html', form=form)

@train_bp.route('/<int:train_id>')
def view_train(train_id):
    db_queries = DatabaseQueries()
    train = db_queries.get_train_by_id(train_id)
    if not train:
        flash('Train non trouvé.', 'error')
        return redirect(url_for('train.list_trains'))
    return render_template('train/view.html', train=train)

@train_bp.route('/<int:train_id>/edit', methods=['GET', 'POST'])
def edit_train(train_id):
    train = Train.query.get_or_404(train_id)
    form = TrainForm(obj=train)
    if form.validate_on_submit():
        train.train_number = form.train_number.data
        train.source_station_code = form.source_station_code.data
        train.source_station_name = form.source_station_name.data
        train.destination_station_code = form.destination_station_code.data
        train.destination_station_name = form.destination_station_name.data
        train.departure_time = form.departure_time.data
        train.arrival_time = form.arrival_time.data
        train.distance = form.distance.data
        db.session.commit()
        flash('Train modifié avec succès!', 'success')
        return redirect(url_for('train.view_train', train_id=train_id))
    return render_template('train/edit.html', form=form, train=train)

@train_bp.route('/<int:train_id>/delete', methods=['POST'])
def delete_train(train_id):
    train = Train.query.get_or_404(train_id)
    db.session.delete(train)
    db.session.commit()
    flash('Train supprimé avec succès!', 'success')
    return redirect(url_for('train.list_trains'))
