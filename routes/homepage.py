from flask import Blueprint
import os

file_path = os.path.abspath(__file__)
homepage = Blueprint(file_path.split("/")[-1].split(".")[0], __name__)

@homepage.route("/")
def homepage():
    return "<p>Hello, World!</p>"