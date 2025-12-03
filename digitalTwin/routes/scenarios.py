from ..digitaltwin import bp
from flask import render_template, redirect, url_for, flash
from ..library import scenarios
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
        scenarios.run(scenario_name)
        # return redirect(url_for('success', ID=id))
        return render_template("success.html", scenario_name = scenario_name)
    return render_template("create_scenario.html", form=form)

# @bp.route("/run/<ID>", methods = ['GET', 'POST'])
# def runScenario():
#     data = runSim.run(id)

# @bp.route("/success/<ID>", methods = ['GET', 'POST'])
# def success(ID):
#     return render_template("successTEMP.html", ID=ID)