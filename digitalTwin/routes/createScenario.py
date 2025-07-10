from ..digitaltwin import bp
from flask import render_template

@bp.route("/createscenario")
def createScenario():
    return render_template("temp_page.html")