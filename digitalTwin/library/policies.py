'''Scripts which deal with running the simulations, as well as storing the data and metadata. Takes results from CreateScenarioForm, creates a folder and metadata dict and runs the ABM model.

This functionality to be replaced with databasing in the deployment version'''

from ..models import models
from . import dataManager
import datetime
from digitalTwin import db

import sqlalchemy as sa
import sqlalchemy.orm as so


def savePolicy(policyForm, rules):

    policyName = policyForm.Name.data

    policy = models.PolicyChoices(policy_name = policyName,
                                  description = policyForm.Description.data,
                                  user_name = dataManager.getUserName(),
                                  timestamp = datetime.datetime.now(datetime.timezone.utc),
                                  rules = []            
                                ) 
    
    for rule in rules:
        print(rule['data'])
        keys = [
            {'old': "QualifyingCharacteristics",'new': "qualifying_characteristics"},
            {'old': "RequiredCharacteristics",'new': "required_characteristics"},
            {'old': "DisqualifyingCharacteristics",'new': "disqualifying_characteristics"},
            {'old': "Wards",'new': "wards"},
            {'old': "PropertyTypes",'new': "property_types"},
            {'old': "IncomeTypes",'new': "income_types"},
            {'old': "ScheduleTypes",'new': "schedule_types"},
            {'old': "AdoptionRate",'new': "adoption_rate"}
        ]

        mapping = {key['old']: key['new'] for key in keys}

        rule_args = {
            mapping[k]: v 
            for k, v in rule['data'].items() 
            if k in mapping and v
        }


        new_rule = models.Rules(**rule_args)

        # Append to the policy
        policy.rules.append(new_rule)

    # add model to database
    db.session.add(policy)
    db.session.commit()   

    policy_id = dataManager.getID(models.PolicyChoices, models.PolicyChoices.policy_name, policyName, 'one')

    return policy_id

def getPolicy(policy_id):
    policy = db.session.scalars(sa.select(models.PolicyChoices).where(models.PolicyChoices.id == policy_id)
                              ).first()
    rules = db.session.scalars(sa.select(models.Rules).where(models.Rules.policy_id == policy_id)
                              ).all()
    policy_data = {'policy': policy, 'rules': rules}

    return policy_data