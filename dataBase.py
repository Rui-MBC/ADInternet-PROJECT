from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from os import path

#SLQ access layer initialization
DATABASE_FILE = "database.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

##CLASSES##

class Gate(Base):
    __tablename__ = 'gate'
    id = Column(Integer, primary_key=True)
    secret = Column(String)
    location = Column(String)
    count =  Column(Integer)
    def __repr__(self):
        return "<Gate(id=%d secret='%s', location='%s',count='%d')>" % (
                                self.id, self.secret, self.location,self.count)
    def as_json(self):
        return {
            'id':self.id,
            'secret':self.secret,
            'location':self.location,
            'count':self.count,
        }

Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()

def newGate(ID,secret,location):
    gate = Gate(id=ID,secret=secret,location=location,count=0)
    session.add(gate)
    session.commit()

def listGate():
    return session.query(Gate).all()
