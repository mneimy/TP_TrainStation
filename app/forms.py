from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TimeField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class UserForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(min=1, max=100)])
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=1, max=100)])
    age = IntegerField('Âge', validators=[DataRequired(), NumberRange(min=0, max=120)])
    submit = SubmitField('Enregistrer')

class TrainForm(FlaskForm):
    train_number = StringField('Numéro de train', validators=[DataRequired()])
    source_station_code = StringField('Code gare départ', validators=[Optional(), Length(max=50)])
    source_station_name = StringField('Nom gare départ', validators=[Optional(), Length(max=200)])
    destination_station_code = StringField('Code gare arrivée', validators=[Optional(), Length(max=50)])
    destination_station_name = StringField('Nom gare arrivée', validators=[Optional(), Length(max=200)])
    departure_time = TimeField('Heure de départ', validators=[Optional()])
    arrival_time = TimeField('Heure d\'arrivée', validators=[Optional()])
    distance = IntegerField('Distance (km)', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Ajouter le train')

class ReservationForm(FlaskForm):
    train_id = SelectField('Sélectionner un train', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Réserver')

class TrainSearchForm(FlaskForm):
    source_station = SelectField('Gare de départ', coerce=str, validators=[DataRequired()])
    destination_station = SelectField('Gare d\'arrivée', coerce=str, validators=[DataRequired()])
    departure_time = SelectField('Heure de départ', coerce=str, validators=[Optional()])
    submit = SubmitField('Chercher des trains')

class ReservationSearchForm(FlaskForm):
    source_station = SelectField('Gare de départ', coerce=str, validators=[DataRequired()])
    destination_station = SelectField('Gare d\'arrivée', coerce=str, validators=[DataRequired()])
    departure_time = SelectField('Heure de départ', coerce=str, validators=[Optional()])
    submit = SubmitField('Chercher des trajets')

class LoginForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    age = IntegerField('Âge', validators=[DataRequired()])
    submit = SubmitField('Se connecter')
