from datetime import datetime
from app.database import db

class WeightHistory(db.Model):
    __tablename__ = 'WeightHistory'

    IDWeight = db.Column(db.Integer, primary_key=True)
    IDAnimal = db.Column(db.Integer, db.ForeignKey('Animal.IDAnimal'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    # Relación con Animal
    animal = db.relationship('Animal', backref=db.backref('weights', lazy=True))

    def __repr__(self):
        return f'<WeightHistory {self.IDWeight}>'
