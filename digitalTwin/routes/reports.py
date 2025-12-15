from ..digitaltwin import bp
from ..library import getData, plotting
from flask import render_template, request


@bp.route('/reports', methods = ['GET', 'POST'])
def reports():
    page = request.args.get('page', 1, type=int)

    data, next_url, prev_url = getData.listAvailableScenarios(page)
    return render_template("reports.html", data = data, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/reports/<scenario_name>/timeline', methods = ['GET'])
def specific_report_timeline(scenario_name):
    scenario = getData.findDBData('Scenario', scenario_name)
    steps, timeseries, energy_range = plotting.timeline(scenario)

    print(steps)
    print('---')
    print(energy_range)
    return render_template("reportTemplateTimeline.html", timeseries = timeseries, energy_range = energy_range, steps = steps)

@bp.route('/reports/<scenario_name>', methods = ['GET'])
def specific_report(scenario_name):
    scenario = getData.findDBData('Scenario', scenario_name)
    hi, model_ts, prop_cols, wealth_cols, hourly = plotting.prepare_data(scenario)
    fig2 = plotting.dailyByPropTypePX(model_ts, prop_cols)
    fig3 = plotting.dailyByWealth(model_ts, wealth_cols)
    fig4 = plotting.temporalHeatMap(hourly)
  
    return render_template("reportTemplate.html", scenario = scenario, fig2 = fig2, fig3 = fig3, fig4 = fig4, ID=scenario.id)

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