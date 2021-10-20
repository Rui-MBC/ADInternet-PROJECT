from flask import Flask, render_template, request, send_from_directory, jsonify, json
import os
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.operators import is_precedent
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.sqltypes import ARRAY, DateTime
from werkzeug.utils import secure_filename
import dataBase as dB
from dataBase import Gate
import random
app = Flask(__name__)

@app.route("/gate", methods=['GET','PUT'])
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
    app.run(host='localhost', port=8000, debug=True)