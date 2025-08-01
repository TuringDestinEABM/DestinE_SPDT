from ..modelling import energyABM
import datetime

def run(form):
    print('test3')
    jobID = assignUniqueID()
    metadata = simMetadata(form)
    outdir = energyABM.run(metadata["DataSource"], metadata["Days"], jobID)

    return jobID, outdir

def simMetadata(form):

    now = datetime.datetime.now()

    metadata={
        "Scenario Name": form.ScenarioName.data,
        "Days": int(form.Days.data),
        "DataSource": form.DataSource.data,
        "Job Submitted": str(now),
        "Output Location": ''
    }
    return metadata

def assignUniqueID():
    jobID = 4 #chosen by dice roll, guaranteed to be random
    return jobID