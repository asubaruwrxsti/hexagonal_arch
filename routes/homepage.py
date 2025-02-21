from flask import Blueprint
import os

file_path = os.path.abspath(__file__)
homepage_bp = Blueprint(file_path.split("/")[-1].split(".")[0], __name__)

@homepage_bp.route("/")
def homepage_route():
    return "<p>Hello, World!</p>"