from ..digitaltwin import bp
from ..library import getData
from flask import render_template, url_for
from pathlib import Path

@bp.route('/reports', methods = ['GET'])
def reports():
    data = listAvailableReports()
    return render_template("reports.html", data = data)

@bp.route('/reports/<ID>', methods = ['GET'])
def specific_report(ID):
    return render_template("reportTemplate.html", summaryGIS = findGEOData('placeholder1', "summaryGIS.json"), metadata = findMetadata(ID), figures = listSummaryFigures(ID))

def findGEOData(ID, filename):
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

def findMetadata(ID):
    path = Path(__file__).parents[1] /"data/geo_data/results" / ID / "metadata.json"
    metadata = getData.loadJSONdata(path)
    figures = listSummaryFigures(path)
    
    return metadata, figures

    # TODO: make this do a 404

def listSummaryFigures(ID):
    path = Path(__file__).parents[1] /"data/geo_data/results" / ID
    figures = dict(plot_day_hour = str(path /"plot_day_hour.png"),
                   plot_hexbin = str(path /"plot_day_hour.png"),
                   plot_prop_type = str(path /"plot_prop_type.png"),
                   plot_wealth = str(path /"plot_wealth.png")
                   )
    return figures


def listAvailableReports():
    path = Path(__file__).parents[1] /"data/geo_data/results"
    folders = list(path.iterdir())
    data = list()

    for folder in folders:
       mdPath = path / folder / "metadata.json"
       metadata =  getData.loadJSONdata(mdPath)
       data.append(metadata) 

    data = dict(files = data)
    print(data)
    return data
