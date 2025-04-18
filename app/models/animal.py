from app.database import db

class Animal(db.Model):
    __tablename__ = 'Animal'

    IDAnimal = db.Column(db.Integer, primary_key=True)
    IDUser = db.Column(db.Integer, db.ForeignKey('User.IDUser'), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female'), nullable=False)
    birth = db.Column(db.Date, nullable=False)
    fertile = db.Column(db.Boolean, default=False)

    def __init__(self, IDUser, breed, gender, birth, fertile):
        self.IDUser = IDUser
        self.breed = breed
        self.gender = gender
        self.birth = birth
        self.fertile = fertile
