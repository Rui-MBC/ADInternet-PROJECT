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
        resp = requests.put("http://localhost:8000/users/"+id+"/code",json=code_info)
        if resp.status_code == 200 :
            return jsonify(newCode)

###########################
# GATE DATABASE ENDPOINTS #
###########################


@app.route("/gates/id", methods = ['GET'])
def logInGate():
    if request.method == 'GET':
        content = request.json
        if bool(content['id']) and bool(content['secret']):
            resp = requests.get("http://localhost:8000/gates/id", json=content)
            return jsonify(resp.json())
        else:
            resp = {
                'errorCode' : 1,
                'errorDescription' : 'No ID or secret'
            }
            return jsonify(resp)



@app.route("/gates/code", methods = ['GET'])
def codeValidation():
    if request.method == 'GET':
        content = request.json
        id = content['id']
        resp = requests.get("http://localhost:8000/users/"+id+"/code", json=content)

        validation = resp.json()
        validation = int(validation['Validation'])
        if validation == 1:
            resp={
                'errorCode':'1'
            }
        else:
            resp={
                'SUCCESS':'0'
            }
        
        return jsonify(resp)
            


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
        create_gate_cont = {
            'id':form_content['id'],
            'location':form_content["location"]
        }
        resp = requests.put("http://localhost:8000/gates",json = create_gate_cont)
        return jsonify(resp.json())

@app.route("/listGate")
def listGate():
    resp = requests.get("http://localhost:8000/gates")
    return jsonify(resp.json())

if __name__ == "__main__":
    app.run(host = 'localhost', port = 8008, debug = True)