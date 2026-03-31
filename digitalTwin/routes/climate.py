from ..digitaltwin import bp
from ..library import dataManager
from flask import render_template, request

@bp.route("/climate", methods = ['GET', 'POST'])
def climate():
    page = request.args.get('page', 1, type=int)

    data, next_url, prev_url = dataManager.getClimateData(page, 'inbuilt')
    return render_template("climate.html", data = data, next_url=next_url,
                           prev_url=prev_url)