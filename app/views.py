import os
from app import app
import pandas as pd
from flask import render_template, request, make_response, jsonify, flash, redirect, url_for, Response
import time
from werkzeug.utils import secure_filename

@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")

app.config["ALLOWED_FILE_EXTENSION"] = ["CSV", "XLSX"]
app.config["FILE_UPLOADS"] = r"/mnt/c/Users/Computador/Documents/xlsx-and-csv-converter/app/static/files/uploads"

def allowed_file(filename):

    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSION"]:
        return True
    else:
        return False

@app.route("/verify_file", methods=["POST"])
def verify_file():

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == "":
            flash(message="File must have name")
            res = make_response(jsonify({"message":"File must have name"}), 400)
            return res
            
        if not allowed_file(file.filename):
            flash(message="File extension is not allowed")
            res = make_response(jsonify({"message":"File extension is not allowed"}), 400)
            return res
        else:
            res = make_response(jsonify({"message":"File is ok"}), 200)
            return res

@app.route('/convert-file', methods=["GET", "POST"])
def convert_file():

    if request.method == "POST":
        if 'file' in request.files:
            print("tem arquivo")
            file = request.files['file']
            if file.filename == "":
                flash("File must have name", category="error")
                res = make_response(jsonify({"message":"File must have name"}), 400)
                return render_template("index.html"), 400
            
            if not allowed_file(file.filename):
                flash("File extension is not allowed", category="error")
                res = make_response(jsonify({"message":"File extension is not allowed"}), 400)
                return render_template("index.html"), 400
            
            else:
                print("Carregado")
                read_file = pd.read_excel(file, header=0)
                # read_file.to_csv("C:\app\master_file.xlsx", index=False, quotechar="'")
                read_file.to_csv(os.path.join("./app/static/files/uploads/",file.filename), index=False, quotechar="'")
                print("Convertido")
                # file.save(os.path.join(app.config["FILE_UPLOADS"], "teste"))
                return "Ok"