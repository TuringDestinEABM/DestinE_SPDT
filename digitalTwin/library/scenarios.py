'''Scripts which deal with running the simulations, as well as storing the data and metadata. Takes results from CreateScenarioForm, creates a folder and metadata dict and runs the ABM model.

This functionality to be replaced with databasing in the deployment version'''

from ..modelling import energyABM, climate
from ..models import models
from . import dataManager, populations
import datetime
from digitalTwin import db
from flask import session
from digitalTwin.config import Config

import sqlalchemy as sa
import sqlalchemy.orm as so

def run_and_save_scenario(scenario_name, log_callback=print):
    """
    Runs the Energy ABM model and bulk-saves all outputs to the database.
    log_callback allows external functions to intercept print statements.
    """
    # Fetch scenario
    log_callback(f"Fetching scenario: {scenario_name} from database...")
    scenario = db.first_or_404(sa.select(models.Scenario).where(models.Scenario.scenario_name == scenario_name))
    
    # Run model
    log_callback("Initializing EnergyABM model...")
    model, records = energyABM.run(scenario, log_callback=log_callback) 
    log_callback("Model run complete. Preparing database records...")

    # Save energy time series
    energy_objects = []
    for entry in records:
        energy_ts = models.EnergyTimeSeries(
            scenario_id=scenario.id,
            step=entry["step"],
            hour=entry["hour"],
            day=entry["day"],
            total_energy=entry["total_energy"],
            average_energy=entry["avg_energy"]
        )
        energy_objects.append(energy_ts)
    db.session.bulk_save_objects(energy_objects)
    db.session.commit()
    log_callback('Energy time series saved.')

    # Save model time series
    model_df = model.datacollector.get_model_vars_dataframe() 
    model_dict = model_df.to_dict('records') 
    
    model_objects = []
    for row in model_dict:
        model_ts = models.ModelTimeSeries(
            scenario_id=scenario.id,
            mid_terraced_house=row["mid-terraced house"],
            semi_detached_house=row["semi-detached house"],
            flats_small=row["small block of flats/dwelling converted in to flats"],
            flats_large=row["large block of flats"],
            flats_block=row["block of flats"],
            end_terrace_house=row["end-terraced house"],
            detached_house=row["detached house"],
            flat_mixed_use=row["flat in mixed use building"],
            high=row["high"],
            medium=row["medium"],
            low=row["low"],
            total_energy=row["total_energy"],
            cumulative_energy=row["cumulative_energy"]
        )
        model_objects.append(model_ts)
    db.session.bulk_save_objects(model_objects)
    db.session.commit()
    log_callback('Model time series saved.')

    # Save agent time series
    agent_df = model.agent_dc.get_agent_vars_dataframe() 
    agent_dict = agent_df.reset_index().values.tolist()
    
    agent_objects = []
    for row in agent_dict:
        agent_ts = models.AgentTimeSeries(
            scenario_id=scenario.id,
            step=row[0],
            Agent_id=row[1],
            energy=row[2],
            energy_consumption=row[3]
        )
        agent_objects.append(agent_ts)
        
    db.session.bulk_save_objects(agent_objects)
    db.session.commit()
    log_callback('Agent time series saved. Process entirely finished!')

# def run(scenario_name):
#     scenario = db.first_or_404(sa.select(models.Scenario).where(models.Scenario.scenario_name == scenario_name))
#     model, records = energyABM.run(scenario) # run the model
#     print('model run')
#     add_log(scenario_name, 'model run')
#     # pass the energy time series to the database
#     energy_objects = []
#     for entry in records:
#         energy_ts = models.EnergyTimeSeries(
#             scenario_id=scenario.id,
#             step=entry["step"],
#             hour=entry["hour"],
#             day=entry["day"],
#             total_energy=entry["total_energy"],
#             average_energy=entry["avg_energy"]
#         )
#         energy_objects.append(energy_ts)
        
#     db.session.bulk_save_objects(energy_objects)
#     db.session.commit()
#     print('energy_ts saved')
#     # pass the model time series to the database
#     model_df = model.datacollector.get_model_vars_dataframe() 
#     model_dict = model_df.to_dict('records') 
    
#     model_objects = []
#     for row in model_dict:
#         model_ts = models.ModelTimeSeries(
#             scenario_id=scenario.id,
#             mid_terraced_house=row["mid-terraced house"],
#             semi_detached_house=row["semi-detached house"],
#             flats_small=row["small block of flats/dwelling converted in to flats"],
#             flats_large=row["large block of flats"],
#             flats_block=row["block of flats"],
#             end_terrace_house=row["end-terraced house"],
#             detached_house=row["detached house"],
#             flat_mixed_use=row["flat in mixed use building"],
#             high=row["high"],
#             medium=row["medium"],
#             low=row["low"],
#             total_energy=row["total_energy"],
#             cumulative_energy=row["cumulative_energy"]
#         )
#         model_objects.append(model_ts)
        
#     db.session.bulk_save_objects(model_objects)
#     db.session.commit()
#     print('model_ts saved')

#    # pass the agent time series to the database
#     agent_df = model.agent_dc.get_agent_vars_dataframe() 
#     agent_list = agent_df.reset_index().values.tolist()# convert to list for quicker iteration
#     print('---')
#     print(agent_list[0])
#     print(agent_list[1])
#     print('---')
#     # Create a list of objects in memory
#     agent_objects = []
#     for row in agent_list:
#         # Assuming row order: [step, Agent_id, energy, energy_consumption] based on your code
#         agent_ts = models.AgentTimeSeries(
#             scenario_id=scenario.id,
#             step=row[0],
#             Agent_id=row[1],
#             energy=row[2],
#             energy_consumption=row[3]
#         )
#         agent_objects.append(agent_ts)
        
#     # Bulk save to the database (much faster!)
#     db.session.bulk_save_objects(agent_objects)
#     db.session.commit()
#     print('agent_ts saved')


def saveScenario(session):

    # get session data
    mainScenarioData = session.get('main_scenario_data', {})

    # create population entry
    popData = session.get('population_data', {})
    popID = createPopulation(popData)
    
    # either get ID for climate data, or create a new entry
    # if session['climate_mode'] == 'preset':
    #     climateID = session.get('selected_preset_id', {})
    # elif session['climate_mode'] == 'new':
    #     climateData = session.get('climate_data', {})
    #     climateID = createClimateModel(climateData)

    # either get ID for policy data, or create a new entry
    if session['policy_mode'] == 'preset':
        policyID = session.get('selected_policy_id', {})
    elif session['policy_mode'] == 'new':
        policyData = session.get('policy_data', {})
        technology = mainScenarioData.get('Technology')
        policyID = createPolicyChoices(policyData, technology)
    
    # create scenario model
    scenario_name = mainScenarioData.get('Name')
    init_lat_lon = setInitLatLon(mainScenarioData.get('City'))

    scenario = models.Scenario(scenario_name = scenario_name,
                days = mainScenarioData.get('Days'),
                city = mainScenarioData.get('City'),
                subset = popData.get('Subset'),
                user_name = dataManager.getUserName(),
                timestamp = datetime.datetime.now(datetime.timezone.utc),
                init_lat = init_lat_lon[0],
                init_lon = init_lat_lon[1],
                policy_id = policyID,
                population_id = popID              
                ) 

    # add model to database
    db.session.add(scenario)
    db.session.commit()   

    # clear session
    clearSession(session)

    return scenario_name

def createPopulation(formData):

    # create model
    population = models.Population(timestamp = datetime.datetime.now(datetime.timezone.utc),
                    user_name=dataManager.getUserName(),
                    wards=formData.get('Wards'),
                    property_types=formData.get('PropertyTypes'), 
                    income_types=formData.get('IncomeTypes'),        
                    schedule_types=formData.get('ScheduleTypes'),            
                )      

    # add model to database
    db.session.add(population)
    db.session.commit()

    #get id
    stmt = sa.select(models.Population.id).order_by(models.Population.id.desc()).limit(1)
    ID = db.session.scalar(stmt)   
    return ID

def createClimateModel(formData):
    model_name= formData.get('Name')

    ### Deprecated, for extension
    # climateModel = models.ClimateModel(model_name=model_name,
    #                 user_name=dataManager.getUserName(),
    #                 base_data=formData.get('BaseData'),
    #                 temp_var_Type=formData.get('TemperatureVar'),
    #                 temp_scale=formData.get('temp_scale'),           
    #             )      

    # create model from form
    climateModel = models.ClimateModel(model_name=model_name,
        user_name=dataManager.getUserName(),
        base_data="ncc_2t_timeseries",
        temp_var_Type="base",
        temp_scale=float(0),           
    )  

    # add model to database
    db.session.add(climateModel)
    db.session.commit()

    #get id
    ID = dataManager.getID(models.ClimateModel,
                           models.ClimateModel.model_name,
                           model_name,
                           'one')
    
    return ID

def createPolicyChoices(formData, technology):
    policy_name = formData.get('Name')
    # create model from form
    policyChoices = models.PolicyChoices(policy_name=policy_name,
                    user_name=dataManager.getUserName(),
                    technology=technology,
                    base_cost=formData.get('BaseCost'),
                    cost_mod_type=formData.get('CostMod'),
                    cost_mod_val=formData.get('CostModVal'),
                    funding_type=formData.get('FundingMethod'),
                    funding_total=formData.get('FundingVal')
                    # pop_preference=formData.get(''),
                    # pop_preference_modifier=formData.get(''),
                    # build_prefence=formData.get(''),
                    # build_preference_modifier=formData.get(''),
                    # loc_preference=formData.get(''),
                    # loc_preference_modifier=formData.get('')
                )      

    # add model to database
    db.session.add(policyChoices)
    db.session.commit()

    #get id
    ID = dataManager.getID(models.PolicyChoices,
                           models.PolicyChoices.policy_name,
                           policy_name,
                           'one')
    
    return ID


def clearSession(session):
    data = ['main_scenario_data',
            'population_data',
            'climate_mode',
            'selected_preset_id',
            'climate_data',
            'policy_mode',
            'selected_policy_id',
            'policy_data',
            'scenario_progress']
    
    for item in data:
        if session.get(item): 
            session[item] = None



def setInitLatLon(city):
    print(city)
    if city == 'newcastle':
        lon = -1.65260
        lat = 55.01802

    elif city == 'sunderland':
        lon = -1.401567
        lat = 54.901682
    
    else:
        lon = 0.0
        lat = 0.0

    return [lon, lat]