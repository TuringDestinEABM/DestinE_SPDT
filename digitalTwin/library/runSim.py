from ..modelling import energyABM, analyze
import datetime, json
from pathlib import Path
from flask import url_for

def run(form):
    jobID = assignUniqueID(name = form.ScenarioName.data)
    outdir = makeOutdir(jobID)
    metadata = simMetadata(form, outdir)
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

def simMetadata(form, outdir):

    now = datetime.datetime.now()

    metadata={
        "Scenario Name": form.ScenarioName.data,
        "Days": int(form.Days.data),
        "DataSource": form.DataSource.data,
        "Job Submitted": str(now),
        "Output Location": str(outdir)
    }

    return metadata

def assignUniqueID(name):
    date = datetime.datetime.now()
    date = date.strftime("%Y%m%d")
    if len(name) >8:
        name = name[0:8]
    
    jobID = date + "_" + name
    return jobID

def makeOutdir(jobID):
    outdir = Path(__file__).parents[1] /"data/geo_data" / str(jobID)
    outdir.mkdir(exist_ok=True)
    return outdir
