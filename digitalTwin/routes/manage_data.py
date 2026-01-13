from ..digitaltwin import bp
from ..library import dataManager
from flask import render_template, request, redirect, url_for


@bp.route("/manage_data", methods = ['GET', 'POST'])
def manageData():
    active_tab = request.args.get('tab', 'scenarios')
    page1 = request.args.get('page1', 1, type=int)
    page2 = request.args.get('page2', 1, type=int)
    data, next, prev, reports = dataManager.manageScenarios(page1, 'asc')
    # reports = dataManager.findCorrespondingResults(data)
    data2, next2, prev2 = dataManager.viewSourceData(page2)

    return render_template("manage_data.html",
                           active_tab=active_tab,
                            data = data,
                            reports = reports,
                            next_url=next,
                            prev_url=prev,
                            data2 =data2,
                            next_url2=next2,
                            prev_url2=prev2)

@bp.route("/data/<id>/clear", methods = ['GET', 'POST'])
def clearData(id):
    print('clearing ' + str(id))
    dataManager.clearResults(id)
    return redirect("/manage_data")

@bp.route("/data/<id>/delete", methods = ['GET', 'POST'])
def deleteData(id):
    dataManager.deleteScenario(id)
    return redirect("/manage_data")