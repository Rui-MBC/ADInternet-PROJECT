
import datetime
from datetime import timedelta
from flask import Flask, render_template, request, send_from_directory, jsonify, json
import os
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.operators import is_precedent
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.sqltypes import ARRAY, DateTime
from werkzeug.utils import secure_filename
import dataBase as dB
from dataBase import session
import random
app = Flask(__name__)

@app.route("users/<path=id>/code", methods=['GET'])
def getCode(id):
    user = dB.getUserById(id)
    validade = datetime.datetime.now() - timedelta(minutes = 5)
    if user.time_stamp > validade:
        return user.code
    else:
        newCode = random.randint(1000,9999)
        dB.setNewUserCode(id, newCode, datetime.datetime.now() )
        return newCode

@app.route("/gates", methods=['GET','PUT'])
def createGate( ):
    if request.method=='PUT':
        gateInfo = request.json
        sec = random.randint(1000,9999)
        dB.newGate(int(gateInfo["id"]), str(sec) ,gateInfo["location"])
        return jsonify(str(sec))
        #return str(sec)
    if request.method=='GET':
        return jsonify(dB.listGate())
    
if __name__ == "__main__":
    session.query(dB.User).delete()
    dB.newUser(85229,0)
    app.run(host='localhost', port=8000, debug=True)    