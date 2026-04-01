from ..digitaltwin import bp
from ..library import dataManager, plotting
from flask import render_template, request, jsonify


@bp.route('/reports', methods = ['GET', 'POST'])
def reports():
    page = request.args.get('page', 1, type=int)

    data, next_url, prev_url = dataManager.listAvailableScenarios(page, 'desc')
    return render_template("reports.html", data = data, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/reports/<scenario_name>', methods = ['GET'])
def specific_report(scenario_name):
    scenario = dataManager.findDBData('Scenario', scenario_name)
    hi, model_ts, prop_cols, wealth_cols, hourly = plotting.prepare_data(scenario)
    
    fig2 = plotting.dailyByPropTypePX(model_ts, prop_cols)
    fig3 = plotting.dailyByWealth(model_ts, wealth_cols)
    fig4 = plotting.temporalHeatMap(hourly)
                        
    return render_template("reportTemplate.html",
                            scenario = scenario,
                            fig2 = fig2,
                            fig3 = fig3,
                            fig4 = fig4,
                            ID=scenario.id)

@bp.route('/reports/<scenario_name>/timeline', methods = ['GET'])
def specific_report_timeline(scenario_name):
    scenario = dataManager.findDBData('Scenario', scenario_name)
    hourArray, gdf_static_js, energy_range = plotting.timeline(scenario)
    init_coords = [scenario.init_lat, scenario.init_lon]

    return render_template("reportTemplateTimeline.html",
                            gdf_static_js = gdf_static_js,
                            energy_range = energy_range,
                            hourArray = hourArray,
                            init_coords = init_coords)

@bp.route('/api/reports/<scenario_name>/energy/<day>')
def timeline_daily_energy(scenario_name, day):
    scenario = dataManager.findDBData('Scenario', scenario_name)
    energy_data = plotting.timeline_daily(scenario, int(day))
    return jsonify(energy_data)