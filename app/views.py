import os
from app import app
from flask import render_template, request, make_response, jsonify, flash

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

@app.route('/verify_file', methods=['POST'])
def verify_file():

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == "":
            flash(message="File must have name", category="error")
            res = make_response(jsonify({"message":"File must have name"}), 400)
            return render_template("index.html"), 400
            
        if not allowed_file(file.filename):
            flash(message="File extension is not allowed", category="error")
            res = make_response(jsonify({"message":"File extension is not allowed"}), 400)
            return render_template("index.html"), 400
        else:
            print("Ok")
            res = make_response(jsonify({"message":"File is ok"}), 200)
            return res
