from ..digitaltwin import bp
from flask import render_template

@bp.route("/data_sources")
def data_sources():
    return render_template("temp_page.html")