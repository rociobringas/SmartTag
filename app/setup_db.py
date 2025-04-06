from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Text, Enum, ForeignKey, Double
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import enum
from flask_login import UserMixin

Base = declarative_base()

# ENUMS
class EventTypeEnum(enum.Enum):
    Weight = 'Weight'
    Vaccine = 'Vaccine'
    Insemination = 'Insemination'
    Recognition = 'Recognition'

# TABLAS

class User(Base, UserMixin):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)  # CAMBIO: usar 'id'
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    fullname = Column(String(100))

    males = relationship("Male", back_populates="user")
    females = relationship("Female", back_populates="user")
    registrations = relationship("Registration", back_populates="user")

class Male(Base):
    __tablename__ = 'Male'
    IDMale = Column(Integer, primary_key=True)
    IDUser = Column(Integer, ForeignKey('User.id'))
    breed = Column(String(50))
    father = Column(String(50))
    birth = Column(Date)
    fertile = Column(Boolean)

    user = relationship("User", back_populates="males")
    reproduction_history = relationship("ReproductionHistory", back_populates="male")

class Female(Base):
    __tablename__ = 'Female'
    IDFemale = Column(Integer, primary_key=True)
    IDUser = Column(Integer, ForeignKey('User.id'))
    breed = Column(String(50))
    father = Column(String(50))
    birth = Column(Date)
    fertile = Column(Boolean)

    user = relationship("User", back_populates="females")
    reproduction = relationship("ReproductionHistory", back_populates="female", uselist=False)

class EventType(Base):
    __tablename__ = 'EventType'
    IDEventType = Column(Integer, primary_key=True)
    name = Column(Enum(EventTypeEnum))
    description = Column(Text)

    registrations = relationship("Registration", back_populates="event_type")

class Registration(Base):
    __tablename__ = 'Registration'
    IDRegistration = Column(Integer, primary_key=True)
    IDUser = Column(Integer, ForeignKey('User.id'))
    IDAnimal = Column(Integer)  # Este campo puede representar tanto macho como hembra
    IDEventType = Column(Integer, ForeignKey('EventType.IDEventType'))
    date = Column(Date)
    value = Column(String(100))

    user = relationship("User", back_populates="registrations")
    event_type = relationship("EventType", back_populates="registrations")

class ReproductionHistory(Base):
    __tablename__ = 'ReproductionHistory'
    IDReproduction = Column(Integer, primary_key=True)
    IDMale = Column(Integer, ForeignKey('Male.IDMale'))
    IDFemale = Column(Integer, ForeignKey('Female.IDFemale'))
    IDEventType = Column(Integer, ForeignKey('EventType.IDEventType'))
    date = Column(Date)
    result = Column(Boolean)

    male = relationship("Male", back_populates="reproduction_history")
    female = relationship("Female", back_populates="reproduction")
    event_type = relationship("EventType")

class VaccineHistory(Base):
    __tablename__ = 'VaccineHistory'
    IDVaccine = Column(Integer, primary_key=True)
    IDAnimal = Column(Integer)
    IDEventType = Column(Integer, ForeignKey('EventType.IDEventType'))
    vaccineType = Column(String(100))
    date = Column(Date)

    event_type = relationship("EventType")

class WeightHistory(Base):
    __tablename__ = 'WeightHistory'
    IDWeight = Column(Integer, primary_key=True)
    IDAnimal = Column(Integer)
    IDEventType = Column(Integer, ForeignKey('EventType.IDEventType'))
    value = Column(Double)
    date = Column(Date)

    event_type = relationship("EventType")


DATABASE_URL = "mysql+pymysql://root:Facu2004@localhost/smarttag"
# 🚀 CONEXIÓN Y CREACIÓN
def setup_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    setup_database()
