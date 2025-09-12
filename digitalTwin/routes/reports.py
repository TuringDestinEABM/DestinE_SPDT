from ..digitaltwin import bp
from ..library import getData, plotting
from flask import render_template, url_for, send_file
from pathlib import Path
import base64
from io import BytesIO
# from . import mpl_plots

@bp.route('/reports', methods = ['GET'])
def reports():
    data = listAvailableReports()
    return render_template("reports.html", data = data)

@bp.route('/reports/<ID>', methods = ['GET'])
def specific_report(ID):
    metadata = findMetadata(ID)
    hi, model_ts, prop_cols, wealth_cols = plotting.prepare_data(metadata["DataSource"], metadata["OutputLocation"], 25)
    hexbinPlot(hi)
    fig2 = plotting.dailyByPropTypePX(model_ts, prop_cols)
    fig3 = plotting.dailyByWealth(model_ts, wealth_cols)
    return render_template("reportTemplateSimple.html", summaryGIS = findGEOData('placeholder1', "summaryGIS.json"), metadata = metadata, fig1="/reports/20250814_test1/hexbin" , fig2 = fig2, fig3 = fig3, ID=ID)

@bp.route('/reports/<ID>/hexbin')
def hexbinPlot(ID):
    metadata = findMetadata("20250814_test1")
    hi, model_ts, prop_cols, wealth_cols = plotting.prepare_data(metadata["DataSource"], metadata["OutputLocation"], 25)
    fig = plotting.spatialHexBin(hi)
    # img = BytesIO()
    # fig.savefig(img)
    # img.seek(0)
    # return send_file(img, mimetype='image/png')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"




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
    # figures = listSummaryFigures(path)
    
    return metadata

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
    # print(data)
    return data

# def create_figure():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     xs = range(100)
#     ys = [random.randint(1, 50) for x in xs]
#     axis.plot(xs, ys)
#     return fig