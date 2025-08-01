from ..digitaltwin import bp
from flask import render_template, redirect
from ..library import runSim
from ..library.forms import CreateScenarioForm

@bp.route("/createscenario", methods = ['GET', 'POST'])
def createScenario():
    form  = CreateScenarioForm()
    if form.validate_on_submit():
        jobID, metadata = runSim.run(form)
        return render_template("success.html", data=metadata, ID=jobID)
    return render_template("create_scenario.html", form=form)

