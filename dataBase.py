from logging import PlaceHolder
from flask.json import jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from os import path
import datetime
from datetime import timedelta


from sqlalchemy.sql.sqltypes import DateTime

#SLQ access layer initialization
DATABASE_FILE = "database.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True

engine = create_engine('sqlite:///%s?check_same_thread=False'%(DATABASE_FILE), echo = False) 

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

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    code = Column(String)
    time_stamp = Column(DateTime)
    def __repr__(self):
        return "<User(id=%d code='%s', time_stamp='%s')>" % (
                                self.id, self.code, str(self.time_stamp))
    def as_json(self):
        return {
            'id':self.id,
            'code':self.code,
            'time_stamp':self.time_stamp,
        }
    
Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()

###########################
# GATE DATABASE FUNCTIONS #
###########################

def newGate(ID,secret,location):
    gate = Gate(id = ID,secret = secret,location = location,count = 0)
    session.add(gate)
    session.commit()

def listGate():
    list = session.query(Gate).all()
    return [Gate.as_json(item) for item in list]

def getGateById(ID):
    resp = session.query(Gate).filter(Gate.id == ID).first()
    return resp


###########################
# USER DATABASE FUNCTIONS #
###########################

# def newUser(Id,Code):
#     placeholderTime = datetime.datetime.now() - timedelta(hours = 1)
#     user = User(id = Id,code = Code,time_stamp = placeholderTime)
#     session.add(user)
#     session.commit()

def newUser(ID,code,time):
    user = User(id = ID,code = code,time_stamp = time)
    session.add(user)
    session.commit()

def getUserById(ID):
    resp = session.query(User).filter(User.id == ID).first()
    return resp

def setNewUserCode(ID, newCode, newDate ):
    user=getUserById(ID)  
    if bool(user):  
        user.code = newCode
        user.time_stamp = newDate
        session.commit()
    else:
        newUser(ID,newCode,newDate)

def validateCode(ID,code,gate_id):
    resp = getUserById(ID)
    true1 = str(resp.code) == code
    true2 = resp.time_stamp + timedelta(minutes = 2)  > datetime.datetime.now()
    if str(resp.code) == code and resp.time_stamp + timedelta(minutes = 2)  > datetime.datetime.now():
        resp.time_stamp =  datetime.datetime.now() - timedelta(weeks = 100)
        gate = getGateById(gate_id)
        gate.count = gate.count + 1
        session.commit()
        return 0
    elif str(resp.code) == code and (resp.time_stamp < datetime.datetime.now() - timedelta(weeks = 50)):
        return 2 #code has already been used
    else:
        return 1
        