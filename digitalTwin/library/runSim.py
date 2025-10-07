'''Scripts which deal with running the simulations, as well as storing the data and metadata. Takes results from CreateScenarioForm, creates a folder and metadata dict and runs the ABM model.

This functionality to be replaced with databasing in the deployment version'''

from ..modelling import energyABM
import datetime, json
from pathlib import Path

'''main script'''
def run(form):
    jobID = assignUniqueID(name = form.ScenarioName.data) 
    
    metadata, outdir = simMetadata(form, jobID)
    energyABM.run(metadata["DataSource"], metadata["Days"], outdir)
    
    file = outdir / "metadata.json"
    try:
        with open(file, 'w') as f:
            json.dump(metadata,f)
    except:
        with open(file, 'x') as f:
            json.dump(metadata,f)


    return jobID, outdir

'''Creates a dictionary containing the metadata describing the data'''
def simMetadata(form, jobID):

    now = datetime.datetime.now()
    outdir =makeOutdir(jobID)

    metadata={
        "id": str(jobID),
        "name": str(form.ScenarioName.data),
        "Days": int(form.Days.data),
        "DataSource": form.DataSource.data,
        "JobSubmitted": str(now),
        "UserName": str(getUserName()),
        "OutputLocation": str(outdir)
    }

    return metadata, outdir

'''Assigns a unique ID containing the submission date and job name
TODO: actually ensure uniqueness'''
def assignUniqueID(name):
    date = datetime.datetime.now()
    date = date.strftime("%Y%m%d")
    if len(name) >8:
        name = name[0:8]
    
    jobID = date + "_" + name
    return jobID

'''Creates a folder for the results (temporary solution until databasing implemented)'''
def makeOutdir(jobID):
    outdir = Path(__file__).parents[1] /"data/geo_data/results" / str(jobID)
    outdir.mkdir(exist_ok=True)
    return outdir

'''Get the user's login'''
def getUserName():
    # TODO: revisit when login functionality sorted
    username = "<username>"
    return username