from ..digitaltwin import bp
from flask import render_template, redirect, url_for, flash, session, request, current_app, jsonify
from ..library import dataManager, scenarios, forms, policies, populations
from ..models import models
import threading
import traceback
import sqlalchemy as sa

ACTIVE_TASKS = {} # log for run_scemario

@bp.route("/createscenario/", methods=['GET', 'POST'])
def create_scenario():
    # main access via link
    scenarios.clearSession(session)
    session['scenario_progress'] = 0
    return redirect(url_for('digitaltwin.create_scenario_init'))

@bp.route("/createscenario/init", methods=['GET', 'POST'])
def create_scenario_init():
        
    mainForm = forms.CreateScenarioForm(prefix="main")

    # Handle Final Submission
    if mainForm.Submit.data and mainForm.validate():
        session['main_scenario_data'] = mainForm.data
        # progress tracker
        session['scenario_progress'] = 1
        return redirect(url_for('digitaltwin.create_scenario_population'))
    
    if mainForm.errors:
        print("Validation Errors:", mainForm.errors)
    
    # Check for return from later
    if request.method == 'GET' and 'main_scenario_data' in session:
        mainForm.process(data=session['main_scenario_data'])
        
    return render_template("create_scenario_init.html", 
                           mainForm = mainForm)

@bp.route("/createscenario/population", methods=['GET', 'POST'])
def create_scenario_population():
     # Ensure user has completed Step 1
    if session.get('scenario_progress', 0) < 1:
        return redirect(url_for('digitaltwin.create_scenario_init'))

    popForm = forms.PopulationModelForm(prefix="population")

    # Check for return from later
    if request.method == 'GET':
        if 'population_data' in session:
            popForm.process(data=session['population_data'])

    # Handle Final Submission
    if popForm.Submit.data and popForm.validate():
        session['population_data'] = popForm.data
        session['scenario_progress'] = 2
        return redirect(url_for('digitaltwin.create_scenario_policy'))
        # return redirect(url_for('digitaltwin.create_scenario_climate'))
    
    if popForm.errors:
        print("Validation Errors:", popForm.errors)

    return render_template("create_scenario_pop.html", 
                           popForm = popForm)
        

### Deprecated, for extension
# @bp.route("/createscenario/climate", methods=['GET', 'POST'])
# def create_scenario_climate():
    
#     if session.get('scenario_progress', 0) < 2:
#         return redirect(url_for('digitaltwin.create_scenario_population'))

#     climateForm = forms.ClimateModelForm(prefix="climate")
#     selectPresets = forms.SelectPresetsClimate(prefix="preset")

#     # Check for return from later
#     if request.method == 'GET':
#         if 'climate_data' in session:
#             climateForm.process(data=session['climate_data'])
    
#     if request.method == 'POST':
#         # Handle Select Preset Submission
#         if selectPresets.Submit.data and selectPresets.validate():
#             selected_obj = selectPresets.selected_climate_id.data
#             if selected_obj:
#                 # Store the choice in session
#                 session['climate_mode'] = 'preset'
#                 session['selected_preset_id'] = selected_obj.id
#                 session['climate_data'] = None # Clear conflicting data

#                 session['scenario_progress'] = 3
#                 return redirect(url_for('digitaltwin.create_scenario_policy'))

#         # Handle "Create New Climate" Submission
#         elif climateForm.Submit.data and climateForm.validate():
#             # Store the form data in session
#             session['climate_mode'] = 'new'
#             session['climate_data'] = climateForm.data # Serializes form data to dict
#             session['selected_preset_id'] = None # Clear conflicting data

#             session['scenario_progress'] = 3
#             return redirect(url_for('digitaltwin.create_scenario_policy'))
        
#         # handle validation errors    
#     if climateForm.errors:
#         print("Validation Errors:", climateForm.errors)
#     if selectPresets.errors:
#         print("Validation Errors:", selectPresets.errors)
    

#     return render_template("create_scenario_climate.html", 
#                            selectPresets=selectPresets, 
#                            climateForm=climateForm)

@bp.route("/createscenario/policy", methods=['GET', 'POST'])
def create_scenario_policy():
    
    policy_data = None
    policyForm = forms.PolicyChoicesForm(prefix="policy")
    selectPresets = forms.SelectPresetsPolicy(prefix="preset")

    # Check for return from later
    if request.method == 'GET':
        if 'policy_data' in session:
            policyForm.process(data=session['policy_data'])

    if request.method == 'POST':

        # check for submission first
        if selectPresets.Submit.data:
            print('selectPresets.Submit.data')
            if selectPresets.validate():
                selected_obj = selectPresets.selected_policy_id.data
                if selected_obj:
                    # Store the choice in session
                    session['policy_mode'] = 'preset'
                    session['selected_policy_id'] = selected_obj.id
                    session['policy_data'] = None # Clear conflicting data
                    session['scenario_progress'] = 3

                    return redirect(url_for('digitaltwin.create_scenario_summary'))
                else:
                    print('Error: No policy selected')
                    flash("Error: No policy selected")

        # Options for viewing policies
        elif selectPresets.View.data and selectPresets.validate():
            policy_data = policies.getPolicy(selectPresets.selected_policy_id.data.id)

    # handle validation errors    
    if policyForm.errors:
        print("Validation Errors:", policyForm.errors)
    if selectPresets.errors:
        print("Validation Errors:", selectPresets.errors)

    return render_template("create_scenario_policy.html", 
                           selectPresets=selectPresets, 
                           policyForm=policyForm,
                           policy_data=policy_data)

@bp.route("/createscenario/summary", methods=['GET', 'POST'])
def create_scenario_summary():

    # redirects for incomplete data
    debug_config = [{'session_data':'main_scenario_data', 'progress_val': 0, 'redirect':'digitaltwin.create_scenario_init'},
                    {'session_data':'population_data', 'progress_val': 1, 'redirect':'digitaltwin.create_scenario_population'},
                    # {'session_data':'climate_data', 'progress_val': 2, 'redirect':'digitaltwin.create_scenario_climate'},
                    {'session_data':'policy_data', 'progress_val': 2, 'redirect':'digitaltwin.create_scenario_climate'}
                    ]

    if session.get('scenario_progress', 0) < 3:
        print('Debug: steps out of order (scenario progress is '
                + str(session.get('scenario_progress', 0))
                + ' and should be 3')
        flash("Please complete the previous steps in order.", "warning")
        return redirect(url_for('digitaltwin.create_scenario_policy'))  
    else:
        for item in debug_config:
            if item['session_data'] not in session:
                print('Debug, missing data in session: ' + str(item['session_data']))
                flash("Missing form options. Redirecting to " +  str(url_for(item['redirect'])))
                session['scenario_progress'] = item['progress_val']
    
    submitForm = forms.SubmitForm()

    if submitForm.Save.data:
        scenario_name = scenarios.saveScenario(session)
        return redirect(url_for('digitaltwin.success', scenario_name = scenario_name))
    
    elif submitForm.Run.data:
        scenario_name = scenarios.saveScenario(session)
        return redirect(url_for('digitaltwin.runScenario', scenario_name = scenario_name))
    
    
    # catch case for presets
    # climate_data = {}
    policy_data = {}
    # if session['climate_mode'] == 'preset':
    #     climate_data = dataManager.findDBData('ClimateModel', session['selected_preset_id'])
    if session['policy_mode'] == 'preset':
        policy_data = policies.getPolicy(session['selected_policy_id'])

    return render_template("create_scenario_summary.html",
                           submitForm = submitForm,
                        #    climate_data = climate_data,
                           policy_data = policy_data
                        )

@bp.route("/success/<scenario_name>", methods = ['GET', 'POST'])
def success(scenario_name):
    scenario = dataManager.findDBData('Scenario', scenario_name)
    return render_template("scenario_created.html",
                            scenario = scenario)

# @bp.route("/runscenario/<scenario_name>", methods = ['GET', 'POST'])
# def runScenario(scenario_name):
#     scenarios.run(scenario_name)
#     return render_template("scenario_status.html",
#                             scenario_name = scenario_name)

# @bp.route("/runscenario/<scenario_name>", methods=['GET', 'POST'])
# def runScenario(scenario_name):
#     # Grab the actual Flask app to pass context to the thread
#     app = current_app._get_current_object()

#     def run_in_background(app, name):
#         with app.app_context():
#             scenarios.run(name)

#     # Start the process in a background thread
#     thread = threading.Thread(target=run_in_background, args=(app, scenario_name))
#     thread.start()

#     # Immediately return the page to the user while the model runs
#     return render_template("scenario_status.html", scenario_name=scenario_name)

# ACTIVE_TASKS = {}

# def add_log(scenario_name, message):
#     """Helper function to replace print() statements"""
#     print(message)  
#     if scenario_name in ACTIVE_TASKS:
#         ACTIVE_TASKS[scenario_name]["logs"].append(message)

@bp.route("/runscenario/<scenario_name>", methods=['GET', 'POST'])
def runScenario(scenario_name):
    app = current_app._get_current_object()

    # Register task
    ACTIVE_TASKS[scenario_name] = {
        "status": "running", 
        "logs": ["Starting process..."]
    }

    # Custom logging function to pass into dataManager
    def route_logger(message):
        print(message) # Still print to server console
        if scenario_name in ACTIVE_TASKS:
            ACTIVE_TASKS[scenario_name]["logs"].append(message)

    def run_in_background(app, name):
        with app.app_context():
            try:
                scenarios.run_and_save_scenario(name, log_callback=route_logger)
                ACTIVE_TASKS[name]["status"] = "completed"
                
            except Exception as e:
                error_trace = traceback.format_exc()
                print(error_trace) 
                ACTIVE_TASKS[name]["status"] = "failed"
                ACTIVE_TASKS[name]["logs"].append(f"CRITICAL ERROR: {str(e)}")

    # Start the background thread
    thread = threading.Thread(target=run_in_background, args=(app, scenario_name))
    thread.start()

    return render_template("scenario_status.html", scenario_name=scenario_name)

@bp.route("/check_status/<scenario_name>")
def check_status(scenario_name):
    # Fetch the task dictionary
    task = ACTIVE_TASKS.get(scenario_name)
    
    if task:
        return jsonify({
            "status": task["status"],
            "logs": task["logs"]
        })
    else:
        return jsonify({"status": "unknown", "logs": []})