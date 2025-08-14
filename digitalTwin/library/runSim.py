from ..modelling import energyABM, analyze
import datetime, json
from pathlib import Path
from flask import url_for

def run(form):
    jobID = assignUniqueID(name = form.ScenarioName.data)
    
    metadata, outdir = simMetadata(form, jobID)
    energyABM.run(metadata["DataSource"], metadata["Days"], outdir)
    analyze.analyze(metadata["DataSource"], outdir, jitterRadius=25, map =True)

    file = outdir / "metadata.json"
    try:
        with open(file, 'w') as f:
            json.dump(metadata,f)
    except:
        with open(file, 'x') as f:
            json.dump(metadata,f)


    return jobID, outdir

def simMetadata(form, jobID):

    now = datetime.datetime.now()
    outdir =makeOutdir(jobID)

    metadata={
        "id": str(jobID),
        "Days": int(form.Days.data),
        "DataSource": form.DataSource.data,
        "JobSubmitted": str(now),
        "UserName": str(getUserName()),
        "OutputLocation": str(outdir)
    }

    return metadata, outdir

def assignUniqueID(name):
    date = datetime.datetime.now()
    date = date.strftime("%Y%m%d")
    if len(name) >8:
        name = name[0:8]
    
    jobID = date + "_" + name
    return jobID

def makeOutdir(jobID):
    outdir = Path(__file__).parents[1] /"data/geo_data/results" / str(jobID)
    outdir.mkdir(exist_ok=True)
    return outdir

def getUserName():
    # TODO: revisit when login functionality sorted
    username = "Stacy Fakename"
    return username