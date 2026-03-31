'''Functions to convert between different representations of data in different data sets'''
from digitalTwin.config import Config
import json

def WardNamesToCodes(ward_names):
    # read the WARD_CODES geojson
    with open(Config.WARD_CODES, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # map of ward codes to ward names
    name_to_code_map = {
        feature['properties']['WD25NM']: feature['properties']['WD25CD']
        for feature in data['features']
    }
    ward_codes = [
        name_to_code_map[name] if name in name_to_code_map else f'unavailable: {name}' 
        for name in ward_names
    ]
    return ward_codes
    

def WardCodesToNames(ward_codes):

    # read the WARD_CODES geojson
    with open(Config.WARD_CODES, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # map of ward codes to ward names
    code_to_name_map = {
        feature['properties']['WD25CD']: feature['properties']['WD25NM']
        for feature in data['features']
    }
    ward_names = [
        code_to_name_map[code] if code in code_to_name_map else f'unavailable: {code}' 
        for code in ward_codes
    ]
    return ward_names

def incomeBands(values, translate_to):

    mapping_list = [{'k_h': 'q1_lowest', 'k_d': 'lowest quintile'},
           {'k_h': 'q2_low', 'k_d': 'second lowest quintile'},
           {'k_h': 'q3_mid', 'k_d': 'median quintile'},
           {'k_h': 'q4_high', 'k_d': 'second highest quintile'},
           {'k_h': 'q5_highest', 'k_d': 'highest quintile'}]
    
    converted_vals = []

    if translate_to == 'hidp':
        lookup = {item['k_d']: item['k_h'] for item in mapping_list}

    elif translate_to == 'descriptor':
        lookup = {item['k_h']: item['k_d'] for item in mapping_list}
    
    for val in values:
        if lookup:
            converted_vals.append(lookup.get(val, val))
        else:
            print("Invalid translate_t, pick either 'hidp' or 'descriptor'")
    
    return converted_vals

def schedules(values, translate_to):

    mapping_list = [{'k_h': 'dual_earner_household', 'k_d': 'dual earner'},
           {'k_h': 'family_with_children', 'k_d': 'family with children'},
           {'k_h': 'retired_household', 'k_d': 'retired household'},
           {'k_h': 'single_parent_with_children', 'k_d': 'single parent with children'},
           {'k_h': 'student_household', 'k_d': 'student'},
           {'k_h': 'unemployed_or_inactive', 'k_d': 'unemployed_or_inactive'},
           {'k_h': 'working_adult_household', 'k_d': 'working adult'}]
    
    converted_vals = []

    if translate_to == 'hidp':
        lookup = {item['k_d']: item['k_h'] for item in mapping_list}

    elif translate_to == 'descriptor':
        lookup = {item['k_h']: item['k_d'] for item in mapping_list}
    
    for val in values:
        if lookup:
            converted_vals.append(lookup.get(val, val))
        else:
            print("Invalid translate_t, pick either 'hidp' or 'descriptor'")
    
    return converted_vals

# def properties(values, translate_to):

#     mapping_list = [{'k_h': 'dual_earner_household', 'k_d': 'block of flats'},
#            {'k_h': 'family_with_children', 'k_d': 'detached house'},
#            {'k_h': 'retired_household', 'k_d': 'end-terraced house'},
#            {'k_h': 'single_parent_with_children', 'k_d': 'large block of flats'},
#            {'k_h': 'student_household', 'k_d': 'mid-terraced house'},
#            {'k_h': 'unemployed_or_inactive', 'k_d': 'semi-detached house'},
#            {'k_h': 'working_adult_household', 'k_d': 'small block of flats/dwelling converted in to flats'}]
#     converted_vals = []

#     if translate_to == 'hidp':
#         lookup = {item['k_d']: item['k_h'] for item in mapping_list}

#     elif translate_to == 'descriptor':
#         lookup = {item['k_h']: item['k_d'] for item in mapping_list}
    
#     for val in values:
#         if lookup:
#             converted_vals.append(lookup.get(val, val))
#         else:
#             print("Invalid translate_t, pick either 'hidp' or 'descriptor'")
    
#     return converted_vals