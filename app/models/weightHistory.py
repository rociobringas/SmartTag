from database import db

class WeightHistory(db.Model):
    __tablename__ = 'WeightHistory'

    IDWeight = db.Column(db.Integer, primary_key=True)
    IDAnimal = db.Column(db.Integer, db.ForeignKey('Animal.IDAnimal'), nullable=False)
    IDRegistration = db.Column(db.Integer, nullable=False)  # Podemos setearlo si usamos registro general
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, IDAnimal, IDRegistration, value, date):
        self.IDAnimal = IDAnimal
        self.IDRegistration = IDRegistration
        self.value = value
        self.date = date
