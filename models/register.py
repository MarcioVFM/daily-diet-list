from database import db
from datetime import datetime

class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(150), nullable=True)
    dieta = db.Column(db.Boolean, default=False)
    horario = db.Column(db.DateTime, default=datetime.now())