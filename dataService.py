
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

@app.route("/users/<path:id>/code", methods = ['GET','PUT'])
def getCode(id):
    if request.method == 'PUT':
        try:
            content = request.json
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        if not content:
            resp = {
            'errorCode' : 5,
            'errorDescription':'database had an error with JSON input.'
        }
            return jsonify(resp)

        newCode = content['code']
        if not newCode:
            resp = {
                'errorCode' : 6,
                'errorDescription':'Failed to receive code.'
            }
            return jsonify(resp)
        dB.setNewUserCode(id, newCode, datetime.datetime.now())
        resp = {
                'errorCode' : 0,
                'errorDescription':''
            }
        return jsonify(resp)

        
    elif request.method == 'GET':

        try:
            content = request.json
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        if not content:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        id = content['id']
        code = content['code']
        gate_id = content['gate_id']
        validation = dB.validateCode(id,code,gate_id)
        if validation == 1:
            success={
                'errorCode':1,
                'errorDescription':'!!! Code not valid !!!'
            }
            return jsonify(success)
        elif validation == 2:
            success={
                'errorCode':2,
                'errorDescription':'This Code Has Been Used Already.'
            }
            return jsonify(success)
        elif validation == 0:
            success={
                'errorCode':0,
                'errorDescription':'Correct Code, Please Proceed.'
            }
            return jsonify(success)




###########################
# GATE DATABASE ENDPOINTS #
###########################


@app.route("/gates/id", methods = ['GET'])
def logInGate():
    if request.method == 'GET':
        try:
            gateInfo = request.json 
        except:
            response = {
                    'errorCode':5,
                    'errorDescription':'DataBase had an error with JSON input.'
                }
            return jsonify(response)
        if not gateInfo:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        try:
            gateInfo["id"]
            gateInfo["secret"]
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        # if not isinstance(gateInfo["id"],int) :
        #     response = {
        #             'errorCode':4,
        #             'errorDescription':'Invalid ID.'
        #         }
        #     return jsonify(response)

        gate = dB.getGateById(gateInfo["id"])
        if gate != None :
            if gate.secret == gateInfo["secret"]:
                response = {
                    'errorCode':0,
                    'errorDescription':''
                }
            else:
                response = {
                    'errorCode':1,
                    'errorDescription':'The secret is not valid for this gate.'
                }
            
        else:
            response = {
                    'errorCode':3,
                    'errorDescription':'No gate found for this ID.'
                }

        return jsonify(response)

@app.route("/gates", methods = ['GET','PUT'])
def createGate( ):
    if request.method == 'PUT':
        try:
            gateInfo = request.json 
        except:
            response = {
                    'errorCode':5,
                    'errorDescription':'DataBase had an error with JSON input.'
                }
            return jsonify(response)
        if not gateInfo:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        try:
            gateInfo["id"]
            gateInfo["location"]
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        sec = random.randint(1000,9999)  
        
        if not dB.getGateById(int(gateInfo["id"])):
            dB.newGate(int(gateInfo["id"]), str(sec) ,gateInfo["location"])
            return jsonify(str(sec))
        else:
            response = {
                    'errorCode':4,
                    'errorDescription':'Gate id not available.'
                }
            return jsonify(response)
        #return str(sec)
    if request.method == 'GET':
        return jsonify(dB.listGate())
    
if __name__ == "__main__":
    session.query(dB.User).delete()
    dB.newUser(1111,str(27),datetime.datetime.now() - timedelta(hours = 1))
    app.run(host = 'localhost', port = 8000, debug = True)    