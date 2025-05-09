from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime
from flask_login import current_user

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    #esta línea es para el testeo de generar un informe
    last_report = db.Column(db.DateTime, default=None)


class MemoryResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent = db.Column(db.Float)  # En segundos
    attempts = db.Column(db.Integer)

    user = db.relationship('User', backref='memory_results')

class AttentionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    average_time = db.Column(db.Float)  # tiempo medio de respuesta
    errors = db.Column(db.Integer)
    rounds_completed = db.Column(db.Integer)

    user = db.relationship('User', backref='attention_results')

class ReasoningResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    correct = db.Column(db.Integer)
    incorrect = db.Column(db.Integer)
    time_spent = db.Column(db.Float)

    user = db.relationship('User', backref='reasoning_results')

class Informe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('informes', lazy=True))
