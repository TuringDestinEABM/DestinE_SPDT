from ..digitaltwin import bp
from flask import render_template

@bp.route("/help")
def help():
    return render_template("temp_page.html")