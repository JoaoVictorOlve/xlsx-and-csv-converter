import os
from app import app
from flask import render_template, request, make_response, jsonify

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
            print("File must have name")
            res = make_response(jsonify({"message":"File must have name"}), 400)
            return res
            
        if not allowed_file(file.filename):
            print("File extension is not allowed")
            res = make_response(jsonify({"message":"File extension is not allowed"}), 400)
            return res
        else:
            print("Ok")
            res = make_response(jsonify({"message":"File is ok"}), 200)
            return res
