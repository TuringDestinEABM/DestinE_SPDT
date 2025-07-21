from ..digitaltwin import bp
from ..library import getData
from flask import render_template
from pathlib import Path

# A dummy page for testing GIS functionality, delete before roll out

@bp.route('/map', methods = ['POST', 'GET'])
def map():
    filepath = Path(__file__).parents[1] /"data/geo_data/example.json"
    data = getData.loadJSONdata(filepath)
    return render_template("map.html", data = data)
