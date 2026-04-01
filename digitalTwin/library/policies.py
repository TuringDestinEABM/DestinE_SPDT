'''Scripts which deal with running the simulations, as well as storing the data and metadata. Takes results from CreateScenarioForm, creates a folder and metadata dict and runs the ABM model.

This functionality to be replaced with databasing in the deployment version'''

from ..models import models
from . import dataManager, dataConv
import datetime
from digitalTwin import db

import sqlalchemy as sa
import sqlalchemy.orm as so
import pandas as pd


def savePolicy(policyForm, rules):

    policyName = policyForm.Name.data

    policy = models.PolicyChoices(policy_name = policyName,
                                  description = policyForm.Description.data,
                                  user_name = dataManager.getUserName(),
                                  timestamp = datetime.datetime.now(datetime.timezone.utc),
                                  adoption_rate = policyForm.AdoptionRate.data,
                                  candidate_classes =policyForm.CandidateClasses.data,
                                  rules = []            
                                ) 
    
    for rule in rules:
        print(rule['data'])
        keys = [
            {'old': "QualifyingCharacteristics",'new': "qualifying_characteristics"},
            {'old': "DisqualifyingCharacteristics",'new': "disqualifying_characteristics"},
            {'old': "Wards",'new': "wards"},
            {'old': "TenureTypes",'new': "tenure_types"},
            {'old': "IncomeTypes",'new': "income_types"},
            {'old': "ScheduleTypes",'new': "schedule_types"}
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

def applyPolicy(df, policyID, log_callback=print):
    policy = dataManager.findDBData('PolicyChoices', identifier=policyID)
    
    # adoption rate
    AR = float(policy.adoption_rate) / 100

    for rule in policy.rules:
        log_callback(f'Applying rule {rule.id}')
        # construct mask
        base_mask = pd.Series(True, index=df.index)
        mask = ruleMask(df, rule, base_mask)
        # apply candidate classes
        mask &= (df['heatpump_candidate_class'].isin(policy.candidate_classes))

        # sample
        indices_to_change = df[mask].sample(frac=AR).index

        # change
        df.loc[indices_to_change, 'main_heating_system'] = 'heat pump'

    return df

def ruleMask(df, rule, mask):
    ward_codes = [] 
    # replace ward_names with ward codes
    if rule.wards:
        ward_codes = dataConv.WardNamesToCodes(rule.wards)

    keys = [
        {'db_name': 'Ward', 'df_col': 'ward_code', 'db_list': ward_codes},
        {'db_name': 'Tenure', 'df_col': 'tenure', 'db_list': rule.tenure_types},
        {'db_name': 'Income', 'df_col': 'hh_income_band', 'db_list': rule.income_types},
        {'db_name': 'Schedule', 'df_col': 'schedule_type', 'db_list': rule.schedule_types}
    ]

    # construct mask
    if rule.qualifying_characteristics:
        for qc in rule.qualifying_characteristics:
            for key in keys:
                if qc == key['db_name']:
                    mask &= df[key['df_col']].isin(key['db_list'])

    if rule.disqualifying_characteristics:
        for dc in rule.disqualifying_characteristics:
            for key in keys:
                if dc == key['db_name']:
                    mask &= ~df[key['df_col']].isin(key['db_list'])

    return mask