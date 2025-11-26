'''Scripts which deal with running the simulations, as well as storing the data and metadata. Takes results from CreateScenarioForm, creates a folder and metadata dict and runs the ABM model.

This functionality to be replaced with databasing in the deployment version'''

from ..modelling import energyABM
import datetime, json
from pathlib import Path
import random
from digitalTwin import db
from digitalTwin.models import models

'''main script'''
def createNewScenario(form):
    days = form.Days.data
    scenario_name = form.ScenarioName.data

    scenario = models.Scenario(scenario_name = scenario_name,
                days = days,
                data_source = form.DataSource.data,
                user_name = getUserName(),
                timestamp = datetime.datetime.now(datetime.timezone.utc))
    db.session.add(scenario)
    db.session.commit()
    
    return scenario_name

# def run(form):
#     id = assignUniqueID() 
#     scenario_name = form.Days.data
#     days = form.ScenarioName.data
#     data_source = form.DataSource.data
#     job_name = form.ScenarioName.data
#     user_name = getUserName()
#     timestamp = datetime.datetime.now(datetime.timezone.utc)
#     results = dummyRunSim(days)
    
#     return id



'''Get the user's login'''
def getUserName():
    # TODO: revisit when login functionality sorted
    username = "<username>"
    return username

def dummyRunSim(days):
    results = []
    for day in range(days):
        results.append(random.randint(0,9))

    timesteps = list(range(days))
    data = {'timesteps': timesteps,
            'results': results}

    return data