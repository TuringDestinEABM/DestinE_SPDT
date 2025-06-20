from ..digitaltwin import bp
from flask import render_template

@bp.route("/queue")
def queue():
    return render_template("temp_page.html")