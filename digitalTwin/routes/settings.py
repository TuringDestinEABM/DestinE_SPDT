from ..digitaltwin import bp
from flask import render_template

@bp.route("/settings")
def settings():
    return render_template("temp_page.html")