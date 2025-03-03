from ..digitaltwin import bp
from flask import render_template, request

@bp.route("/contact")
def contact():
    return render_template("contact.html")