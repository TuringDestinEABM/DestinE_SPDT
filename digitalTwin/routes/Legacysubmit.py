from ..digitaltwin import bp
from ..modelling import energyABM
from flask import render_template

@bp.route("/submit", methods = ['GET', 'POST'])
def submit():
    energyABM.runmodel("ncc_neighborhood.geojson", 7, "01")
    return render_template("success.html")

def createJob():
    pass