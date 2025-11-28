'''Scripts which deal with running the simulations, as well as storing the data and metadata. Takes results from CreateScenarioForm, creates a folder and metadata dict and runs the ABM model.

This functionality to be replaced with databasing in the deployment version'''

from digitalTwin.modelling import energyABMTEMP
import datetime, json
from pathlib import Path
import random
from digitalTwin import db
from digitalTwin.models import models
import sqlalchemy as sa
import sqlalchemy.orm as so

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

def run(scenario_name):
    scenario = db.first_or_404(sa.select(models.Scenario).where(models.Scenario.scenario_name == scenario_name))
    model, records = energyABMTEMP.run (scenario.data_source, scenario.days) # run the model
    
    # pass the energy time series to the database
    for entry in records:
        energy_ts = models.EnergyTimeSeries(scenario_id = scenario.id,
                                            step = entry["step"],
                                            hour = entry["hour"],
                                            day = entry["day"],
                                            total_energy = entry["total_energy"],
                                            average_energy = entry["avg_energy"]
                                            )
        db.session.add(energy_ts)
    db.session.commit()

    # pass the energy time series to the database
    model_df = model.datacollector.get_model_vars_dataframe()
    for row in model_df.iterrows():
        model_ts = models.ModelTimeSeries(scenario_id = scenario.id,
                                        mid_terraced_house = row["mid-terraced house"],
                                        semi_detached_house = row["semi-detached house"],
                                        flats_small = row["small block of flats/dwelling converted into flats"],
                                        flats_large = row["large block of flats"],
                                        flats_block = row["block of flats"],
                                        end_terrace_house = row["end-terrace house"],
                                        detached_house = row["detached house"],
                                        flat_mixed_use = row["flat in mixed use building"],
                                        high = row["high"],
                                        medium = row["medium"],
                                        low = row["low"],
                                        total_energy = row["total_energy"],
                                        cumulative_energy = row["cumulative_energy"])
        db.session.add(model_ts)
    db.session.commit()





    

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