import sqlalchemy as sa
import sqlalchemy.orm as so
from digitalTwin import db
from . import dataManager, scenarios, dataConv
from digitalTwin.models import models

def createPopulation(form):
    population = models.Population(user_name=scenarios.getUserName(),
                                   wards = form.Wards.data,
                                   property_types = form.PropertyTypes.data,
                                   occupant_types = form.OccupantTypes.data
    )
    db.session.add(population)
    db.session.commit()

def propertyTypes(city):
    query = sa.select(models.EPCABMdata.property_type).where(models.EPCABMdata.city==city).distinct()
    property_types = db.session.execute(query).scalars().all()
    return property_types

def wardNames(city):
    ward_codes = wardCodes(city)
    ward_names = dataConv.WardCodesToNames(ward_codes) 
   
    return ward_names

def wardCodes(city):
    query = sa.select(models.EPCABMdata.ward_code).where(models.EPCABMdata.city==city).distinct()
    ward_codes = db.session.execute(query).scalars().all()
    # print(ward_codes)
    return ward_codes

