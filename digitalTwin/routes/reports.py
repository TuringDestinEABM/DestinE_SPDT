from ..digitaltwin import bp
from ..library import getData
from flask import render_template, jsonify
from pathlib import Path

@bp.route('/reports', methods = ['GET'])
def reports():
    filepath = Path(__file__).parents[1] /"data/geo_data/metadata.json"
    data = getData.loadJSONdata(filepath)
    return render_template("reports.html", data = data)

@bp.route('/reports/<ID>', methods = ['GET'])
def specific_report(ID):
    return render_template("reportTemplate.html", summaryGIS = findData(ID, "summaryGIS.json"))

def findData(ID, filename):
    filepath = Path(__file__).parents[1] /"data/geo_data/metadata.json"
    metadata = getData.loadJSONdata(filepath)
    for item in metadata["files"]:
        if item["id"] == ID:
           data_loc = item["data_loc"]
           filepath = Path(__file__).parents[1] /"data/geo_data" / data_loc / filename
           data = getData.loadJSONdata(filepath)
           break
    return data
    # TODO: make this do a 404