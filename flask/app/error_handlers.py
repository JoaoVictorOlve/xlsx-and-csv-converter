from app import app

from flask import render_template, request

@app.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html")

@app.errorhandler(404)
def internal_error(error):
    return render_template("errors/404.html")