from flask import Flask
from os import environ as env

app = Flask(__name__)

if env["FLASK_ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
    app.debug = False
else:
    app.config.from_object("config.DevelopmentConfig")
    app.debug = True

from app import views
