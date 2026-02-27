from ..digitaltwin import bp
from ..library import dataManager
from ..models import models

from flask import render_template, request, redirect, url_for


@bp.route("/manage_data", methods = ['GET', 'POST'])
def manageData():

    tab_config = [
        {'id': 'scenarios', 'model': models.Scenario, 'per_page': 10, 'check_results': True},
        # {'id': 'climate_models', 'model': models.ClimateModel, 'per_page': 10, 'check_results': False},
        {'id': 'policy_choices', 'model': models.PolicyChoices, 'per_page': 10, 'check_results': False},
        {'id': 'population', 'model': models.Population, 'per_page': 10, 'check_results': False},
        {'id': 'source_data', 'model': models.EPCABMdata, 'per_page': 50, 'check_results': False}
    ]

    tabs_data = []
    active_tab = request.args.get('tab', 'scenarios')    

    for t in tab_config:
        page_param = f"page_{t['id']}"
        current_page = request.args.get(page_param, 1, type=int)

        data, next_url, prev_url = dataManager.getTableData(model = t['model'],
                                                            page = current_page,
                                                            url_str = 'digitaltwin.manageData',
                                                            active_tab = active_tab,
                                                            current_tab_id=t['id'],
                                                            per_page = t['per_page'],
                                                            check_results = t['check_results'])
        tab_object = {
            'id':t['id'],
            'tab_data':data,
            'is_active': (active_tab == t['id']),
            'next_url': next_url,
            'prev_url': prev_url
            }
        tabs_data.append(tab_object)

    return render_template("manage_data.html", tabs_data=tabs_data)

@bp.route("/data/<id>/clear", methods = ['GET', 'POST'])
def clearData(id):
    active_tab = request.args.get('tab', 'scenarios')
    page_param_key = f"page_{active_tab}"
    current_page = request.args.get(page_param_key)
    redirect_args = {'tab': active_tab}
    if current_page:
        redirect_args[page_param_key] = current_page

    #clear the scenario
    print('clearing ' + str(id))
    dataManager.clearResults(id)
    return redirect(url_for('digitaltwin.manageData', **redirect_args))

@bp.route("/data/<table_id>/<id>/delete", methods = ['GET', 'POST'])
def deleteData(table_id, id):
    #   capture current page and tab
    active_tab = request.args.get('tab', 'scenarios')
    page_param_key = f"page_{active_tab}"
    current_page = request.args.get(page_param_key)
    redirect_args = {'tab': active_tab}
    if current_page:
        redirect_args[page_param_key] = current_page

    # delete the entry
    dataManager.deleteEntry(table_id, id)

    return redirect(url_for('digitaltwin.manageData', **redirect_args))