import os
from app import app
import pandas as pd
from flask import render_template, request, make_response, jsonify, flash, redirect, url_for, Response, session, send_from_directory
import time
from werkzeug.utils import secure_filename
import datetime
import uuid
import app.helper as helper
import threading

app.config["FILE_UPLOADS"] = r"/mnt/c/Users/Computador/Documents/xlsx-and-csv-converter/app/static/files/uploads"

@app.before_request
def schedule_removal():
    directory = app.config["FILE_UPLOADS"]
    background_thread = threading.Thread(target=helper.schedule_file_removal, args=(directory, 10))
    background_thread.daemon = True
    background_thread.start()

@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")

app.config["ALLOWED_FILE_EXTENSION"] = ["CSV", "XLSX"]

def allowed_file(filename):

    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSION"]:
        return True
    else:
        return False

@app.route("/verify-file", methods=["POST"])
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
                filename_and_ext_list = file.filename.rsplit(".", 1)
                if filename_and_ext_list[1] == "xlsx":

                    read_file = pd.read_excel(file, header=0)
                    datetime_name = str(datetime.datetime.now().date()).replace('-', '_') + '_' + str(datetime.datetime.now().time()).replace(':', '_').replace('.', '_')
                    uuid_name = uuid.uuid4().hex
                    unique_filename = f"{datetime_name}_{uuid_name}-{filename_and_ext_list[0]}.csv"
                    read_file.to_csv(os.path.join("./app/static/files/uploads/",unique_filename), index=False, quotechar="'")
                    session["filename"] = unique_filename
                    return redirect(url_for("result_page"))
                
                else:

                    read_file = pd.read_csv(file, header=0)
                    datetime_name = str(datetime.datetime.now().date()).replace('-', '_') + '_' + str(datetime.datetime.now().time()).replace(':', '_').replace('.', '_')
                    uuid_name = uuid.uuid4().hex
                    unique_filename = f"{datetime_name}_{uuid_name}-{filename_and_ext_list[0]}.xlsx"
                    read_file.to_excel(os.path.join("./app/static/files/uploads/",unique_filename), index=False)
                    session["filename"] = unique_filename
                    return redirect(url_for("result_page"))
            
@app.route('/result-page', methods=["GET"])
def result_page():
    if session["filename"]:
        filename = session["filename"]
        original_filename = filename.split("-", 1)[1]
        return render_template("result.html", original_filename=original_filename)
    else:
        redirect(url_for('index'))

@app.route('/download-file', methods=["GET"])
def download_file():
    if "filename" in session:
        filename = session["filename"]
        print(filename)
        original_filename = filename.split("-", 1)[1]
        try:
            return send_from_directory(directory=app.config["FILE_UPLOADS"], path=filename, download_name=original_filename, as_attachment=True)
        except:
            flash("File could not be downloaded", category="error")
            return redirect(url_for('result_page'))
    else:
        flash("File could not be downloaded", category="error")
        return redirect(url_for('index'))
