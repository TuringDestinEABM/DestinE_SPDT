from ..digitaltwin import bp
from ..library import energyABM, getData
from flask import render_template

@bp.route("/submit", methods = ['GET', 'POST'])
def submit():
    energyABM.runmodel("ncc_neighborhood.geojson", 7, "01")
    return render_template("success.html")