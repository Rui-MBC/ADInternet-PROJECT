from flask import Flask, render_template, request, send_from_directory, jsonify, json
from werkzeug.utils import secure_filename
import requests
import datetime
from datetime import timedelta
import random
app = Flask(__name__)

###########################
# USER DATABASE ENDPOINTS #
###########################

# o metodo post servir para meter o codigo aquando do pedido
#o metodo get servir para autentificar o codigo
@app.route("/users/<path:id>/code", methods = ['GET'])
def getCode(id):
    if request.method == 'GET':
        newCode = random.randint(1000,9999)
        code_info = {
            'code':str(newCode)
        }
        try:
            resp = requests.put("http://localhost:8000/users/"+id+"/code",json=code_info)
        except:
            resp = {
                'errorCode' : 7,
                'errorDescription' : 'Couldn´t access database'
            }
            return jsonify(resp)
        
        response = resp.json()
        if response['errorCode'] == 0 :
            response ={
                'errorCode' : 0,
                'errorDescription' : '',
                'code': newCode
            }
        return jsonify(response)

###########################
# GATE DATABASE ENDPOINTS #
###########################


@app.route("/gates/id", methods = ['GET'])
def logInGate():
    if request.method == 'GET':
        try:
            content = request.json
        except:
            resp = {
                'errorCode' : 11,
                'errorDescription':'Server had an error with JSON input.'
            }
            return jsonify(resp)

        if bool(content['id']) and bool(content['secret']):
            try:
                resp = requests.get("http://localhost:8000/gates/id", json=content)
            except:
                resp = {
                    'errorCode' : 7,
                    'errorDescription' : 'Couldn´t access database'
                }
                return jsonify(resp)

            return jsonify(resp.json())
        else:
            resp = {
                'errorCode' : 10,
                'errorDescription' : 'No ID or secret.'
            }
            return jsonify(resp)



@app.route("/gates/code", methods = ['GET'])
def codeValidation():
    if request.method == 'GET':
        try:
            content = request.json
        except:
            resp = {
                'errorCode' : 11,
                'errorDescription' : 'Server had an error with JSON input.'
            }
            return jsonify(resp)
        if not content:
            resp = {
                'errorCode' : 11,
                'errorDescription':'Server had an error with JSON input.'
            }
            return jsonify(resp)
        try:
            content["id"]
            content["code"]
            content["gate_id"]
        except:
            resp = {
                'errorCode' :11,
                'errorDescription':'Server had an error with JSON input.'
            }
            return jsonify(resp)
        code = content['code']
        id = content['id']
        if not code or not id:
            resp = {
                'errorCode' : 8,
                'errorDescription' : 'Lacking arguments.'
            }
            return jsonify(resp)

        try:
            resp = requests.get("http://localhost:8000/users/"+id+"/code", json=content)
        except:
            resp = {
                'errorCode' : 7,
                'errorDescription' : 'Couldn´t access database'
            }
            return jsonify(resp)

        validation = resp.json()
        
        return jsonify(validation)
            


##########################
# ADMIN WEBAPP ENDPOINTS #
##########################

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newGate", )
def newGate():
    return render_template("newGate.html")

@app.route("/createGate",methods = ['GET','POST'])
def createGate():
    if request.method == 'POST':
        form_content = request.form.to_dict()
        try:
            id= int(form_content['id'])
        except:
            resp = {
                'errorCode' : 9,
                'errorDescription' : '!!! Bad form !!!'
            }
            return jsonify(resp)

        if not form_content or not form_content['id'] or not form_content["location"]:
            
            resp = {
                'errorCode' : 9,
                'errorDescription' : '!!! Bad form !!!'
            }
            return jsonify(resp)

        create_gate_cont = {
            'id':form_content['id'],
            'location':form_content["location"]
        }
        try:
            resp = requests.put("http://localhost:8000/gates",json = create_gate_cont)
        except:
            resp = {
                'errorCode' : 7,
                'errorDescription' : 'Couldn´t access database.'
            }
            return jsonify(resp)
        return jsonify(resp.json())

@app.route("/listGate")
def listGate():
    try:
        resp = requests.get("http://localhost:8000/gates")
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database'
        }
        return jsonify(resp)
    return jsonify(resp.json())

if __name__ == "__main__":
    app.run(host = 'localhost', port = 8008, debug = True)