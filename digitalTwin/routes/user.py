from ..digitaltwin import bp
from flask import render_template

@bp.route("/user")
def user():
    return render_template("temp_page.html")