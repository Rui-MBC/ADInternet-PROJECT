from flask import Flask, render_template, request, send_from_directory, jsonify, json
from werkzeug.utils import secure_filename
import requests
app = Flask(__name__)

@app.route("/user/<path:id>/code", methods=['GET'])
def getCode(id):
    resp = requests.get("http://localhost:8000/users/"+id+"/code")
    return jsonify(resp.json())

    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newGate", )
def newGate():
    return render_template("newGate.html")

@app.route("/createGate",methods=['GET','POST'])
def createGate():
    if request.method=='POST':
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
    app.run(host='localhost', port=8008, debug=True)