from ..digitaltwin import bp
# from ..library import getData
from flask import render_template, jsonify
import json
from pathlib import Path

@bp.route('/map', methods = ['POST', 'GET'])
def map():
    filepath = Path(__file__).parents[1] /"data/geo_data/example.json"
    d = loadJSONdata(filepath)
    data = d
    return render_template("map.html", data = data)

def loadJSONdata(filepath):
    with open(filepath) as file:
        d = json.load(file)
    return d