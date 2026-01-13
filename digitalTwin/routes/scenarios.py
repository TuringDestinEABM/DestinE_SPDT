from ..digitaltwin import bp
from flask import render_template, redirect, url_for, flash
from ..library import dataManager, scenarios
from ..library.forms import CreateScenarioForm

## original
# @bp.route("/createscenario", methods = ['GET', 'POST'])
# def createScenario():
#     form  = CreateScenarioForm()
#     if form.validate_on_submit():
#         jobID, metadata = runSim.run(form)
#         return render_template("success.html", data=metadata, ID=jobID)
#     return render_template("create_scenario.html", form=form)

@bp.route("/createscenario", methods = ['GET', 'POST'])
def createScenario():
    form  = CreateScenarioForm()
    if form.validate_on_submit():
        scenario_name = scenarios.createNewScenario(form)
        scenario = dataManager.findDBData('Scenario', scenario_name)
        # getData.calculateSubset(scenario.data_source, scenario.subset)
        return render_template("scenario_created.html", scenario_name = scenario_name, scenario = scenario)
    return render_template("create_scenario.html", form=form)

@bp.route("/runscenario/<scenario_name>", methods = ['GET', 'POST'])
def runScenario(scenario_name):
    scenario = dataManager.findDBData('Scenario', scenario_name)
    scenarios.run(scenario_name) 
    return render_template("scenario_status.html", scenario_name = scenario_name)


# @bp.route("/run/<ID>", methods = ['GET', 'POST'])
# def runScenario():
#     data = runSim.run(id)

# @bp.route("/success/<ID>", methods = ['GET', 'POST'])
# def success(ID):
#     return render_template("successTEMP.html", ID=ID)