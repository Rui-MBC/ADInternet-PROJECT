from flask import Flask, render_template, request, send_from_directory, jsonify, json
import os
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.operators import is_precedent
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.sqltypes import ARRAY, DateTime
from werkzeug.utils import secure_filename
import dataBase as dB
from dataBase import Gate
app = Flask(__name__)

@app.route("/create_gate", methods=['GET','POST'])
def createGate():


if __name__ == "__main__":
    app.run(host='localhost', port=8000, debug=True)