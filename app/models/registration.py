from datetime import datetime
from app.database import db

class Registration(db.Model):
    __tablename__ = 'Registration'
    
    IDRegistration = db.Column(db.Integer, primary_key=True)
    IDUser = db.Column(db.Integer, db.ForeignKey('User.IDUser'), nullable=False)
    IDAnimal = db.Column(db.Integer, db.ForeignKey('Animal.IDAnimal'), nullable=False)
    EventType = db.Column(db.Enum('weight', 'vaccine'), nullable=False)
    reference_id = db.Column(db.Integer, nullable=False)  # ID de WeightHistory o VaccineHistory
    date = db.Column(db.Date, nullable=False)

    # Relación con Animal
    animal = db.relationship('Animal', backref=db.backref('registrations', lazy=True))
    
    # Relación con User
    user = db.relationship('User', backref=db.backref('registrations', lazy=True))

    def __repr__(self):
        return f'<Registration {self.IDRegistration}>'
