
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

###########################
# USER DATABASE ENDPOINTS #
###########################

@app.route("/users/<path:id>/code", methods = ['GET','POST'])
def getCode(id):
    if request.method == ['POST']:
        content = request.json
        newCode = content['code']
        dB.setNewUserCode(id, newCode, datetime.datetime.now())
        # user = dB.getUserById(id)
        # validade = datetime.datetime.now() - timedelta(minutes = 5)
        # if user.time_stamp > validade:
        #     return jsonify(user.code)
        # else:
        #     newCode = random.randint(1000,9999)
        #     dB.setNewUserCode(id, newCode, datetime.datetime.now() )
        #     return jsonify(newCode)
    elif request.method == ['GET']:
        content = request.json
        id = content['id']
        code = content['code']
        validation = dB.validateCode(id,code)
        if validation == 1:
            success={
                'Validation':'1'
            }
            return jsonify(success)
        else :
            success={
                'Validation':'1'
            }
            return jsonify(success)




###########################
# GATE DATABASE ENDPOINTS #
###########################


@app.route("/gates/id", methods = ['GET'])
def logInGate():
    if request.method == ['GET']:
        gateInfo = request.json
        gate = dB.getGateById(gateInfo["id"])
        if gate.secret == gateInfo["secret"]:
            create_cont = {
                'SUCCESS':1,
            }
        else:
            create_cont = {
                'SUCCESS':0,
            }
        return jsonify(create_cont)

@app.route("/gates", methods = ['GET','PUT'])
def createGate( ):
    if request.method == 'PUT':
        gateInfo = request.json
        sec = random.randint(1000,9999)
        dB.newGate(int(gateInfo["id"]), str(sec) ,gateInfo["location"])
        return jsonify(str(sec))
        #return str(sec)
    if request.method == 'GET':
        return jsonify(dB.listGate())
    
if __name__ == "__main__":
    session.query(dB.User).delete()
    dB.newUser(85229,27)
    app.run(host = 'localhost', port = 8000, debug = True)    