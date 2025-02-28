from ..digitaltwin import bp
from flask import render_template

@bp.route("/map")
def map():
    return render_template("map.html")
