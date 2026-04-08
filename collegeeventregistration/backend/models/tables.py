from database.db import Base 
from sqlalchemy   import Column ,  Integer , String ,Boolean

class Event(Base):
    __tablename__="events"
    id=Column(Integer , primary_key = True)
    title=Column(String)
    venue=Column(String)
    date=Column(String)
    time=Column(String)

class Registration(Base):
    __tablename__="registrations"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    gender = Column(String)
    year = Column(String)
    department = Column(String)
    college = Column(String)
    city = Column(String)
    event = Column(String)
    team_event = Column(String)
    team_name = Column(String)
    team_size = Column(Integer)
    teammates = Column(String)
    attendance = Column(Boolean, default=False)

class User(Base):
    __tablename__="users"
    id=Column(Integer , primary_key=True)
    email=Column(String , unique = True , index = True)
    password = Column(String)
    role = Column(String)
