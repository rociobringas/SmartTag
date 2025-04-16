from datetime import datetime
from app.database import db

class VaccineHistory(db.Model):
    __tablename__ = 'VaccineHistory'

    IDVaccine = db.Column(db.Integer, primary_key=True)
    IDAnimal = db.Column(db.Integer, db.ForeignKey('Animal.IDAnimal'), nullable=False)
    vaccineType = db.Column(db.Enum('typea', 'typeb', 'typec'), nullable=False)
    date = db.Column(db.Date, nullable=False)

    # Relación con Animal
    animal = db.relationship('Animal', backref=db.backref('vaccines', lazy=True))

    def __repr__(self):
        return f'<VaccineHistory {self.IDVaccine}>'
