from ..digitaltwin import bp
from ..library import getData, plotting
from flask import render_template, url_for, send_file, current_app
import base64
from io import BytesIO
from pathlib import Path

@bp.route('/reports', methods = ['GET'])
def reports():
    results_dir = Path(current_app.config['RESULTS_DIR'])
    data = getData.listAvailableReports(results_dir)
    return render_template("reports.html", data = data)

@bp.route('/reports/<ID>', methods = ['GET'])
def specific_report(ID):
    metadata = getData.findMetadata(ID)
    hi, model_ts, prop_cols, wealth_cols, hourly = plotting.prepare_data(metadata["DataSource"], metadata["OutputLocation"], 25)
    
    fig2 = plotting.dailyByPropTypePX(model_ts, prop_cols)
    fig3 = plotting.dailyByWealth(model_ts, wealth_cols)
    fig4 = plotting.temporalHeatMap(hourly)

    return render_template("reportTemplate.html", metadata = metadata, fig2 = fig2, fig3 = fig3, fig4 = fig4, ID=ID)


@bp.route('/reports/<ID>/timeline', methods = ['GET'])
def specific_report_timeline(ID):
    metadata = getData.findMetadata(ID)
    steps, timeseries, energy_range = plotting.timeline(metadata["DataSource"], metadata["OutputLocation"])
    return render_template("reportTemplateTimeline.html", timeseries = timeseries, energy_range = energy_range, steps = steps)

# @bp.route('/reports/<ID>/hexbin')
# def hexbinPlot(ID):
#     metadata = getData.findMetadata("20250814_test1")
#     hi, model_ts, prop_cols, wealth_cols, hourly = plotting.prepare_data(metadata["DataSource"], metadata["OutputLocation"], 25)
#     fig = plotting.spatialHexBin(hi)
#     buf = BytesIO()
#     fig.savefig(buf, format="png")
#     # Embed the result in the html output.
#     data = base64.b64encode(buf.getbuffer()).decode("ascii")
#     return f"<img src='data:image/png;base64,{data}'/>"

#     # TODO: make this do a 404

# # def create_figure():
# #     fig = Figure()
# #     axis = fig.add_subplot(1, 1, 1)
# #     xs = range(100)
# #     ys = [random.randint(1, 50) for x in xs]
# #     axis.plot(xs, ys)
# #     return fig