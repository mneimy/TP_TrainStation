from flask_sqlalchemy import SQLAlchemy
from datetime import time
from app import db

class User(db.Model):
    __tablename__ = 'utilisateur'
    
    id_user = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)  # Peut être NULL selon votre structure
    
    # Relation avec les réservations
    reservations = db.relationship('Reservation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.prenom} {self.nom}>'
    
    def to_dict(self):
        return {
            'id': self.id_user,
            'nom': self.nom,
            'prenom': self.prenom,
            'age': self.age
        }

class Train(db.Model):
    __tablename__ = 'train'
    
    id_train = db.Column(db.Integer, primary_key=True)
    train_number = db.Column(db.String, nullable=False)
    arrival_time = db.Column(db.Time, nullable=True)
    departure_time = db.Column(db.Time, nullable=True)
    distance = db.Column(db.Integer, nullable=True)
    source_station_code = db.Column(db.String(50), nullable=True)
    source_station_name = db.Column(db.String(200), nullable=True)
    destination_station_code = db.Column(db.String(50), nullable=True)
    destination_station_name = db.Column(db.String(200), nullable=True)
    
    # Relation avec les réservations
    reservations = db.relationship('Reservation', backref='train', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Train {self.train_number}: {self.source_station_name} -> {self.destination_station_name}>'
    
    def to_dict(self):
        return {
            'id': self.id_train,
            'train_number': self.train_number,
            'arrival_time': self.arrival_time.strftime('%H:%M') if self.arrival_time else None,
            'departure_time': self.departure_time.strftime('%H:%M') if self.departure_time else None,
            'distance': self.distance,
            'source_station_code': self.source_station_code,
            'source_station_name': self.source_station_name,
            'destination_station_code': self.destination_station_code,
            'destination_station_name': self.destination_station_name
        }
    
    @property
    def display_name(self):
        """Nom d'affichage du train pour les formulaires"""
        if self.source_station_name and self.destination_station_name:
            return f"{self.train_number} - {self.source_station_name} → {self.destination_station_name}"
        return f"Train {self.train_number}"

class Reservation(db.Model):
    __tablename__ = 'reservation'
    
    id_reservation = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('utilisateur.id_user'), nullable=False)
    id_train = db.Column(db.Integer, db.ForeignKey('train.id_train'), nullable=False)
    
    def __repr__(self):
        return f'<Reservation User:{self.id_user} Train:{self.id_train}>'
    
    def to_dict(self):
        return {
            'id': self.id_reservation,
            'user_id': self.id_user,
            'train_id': self.id_train,
            'user': self.user.to_dict() if self.user else None,
            'train': self.train.to_dict() if self.train else None
        }
