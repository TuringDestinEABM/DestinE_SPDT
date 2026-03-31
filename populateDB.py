'''Check app.db exists. Check it contains initial data. if it doesn't, populate it'''

import geojson
import pandas as pd
import sqlite3
import csv
import pyarrow.parquet as pa

from digitalTwin import db
from digitalTwin.models import models
from digitalTwin.config import Config
from sqlalchemy import inspect




def checkPopulated(tableName, conn):
    cur = conn.cursor()
    cur.execute('SELECT id FROM ' +tableName + ' WHERE id =?', (1,))
    row = cur.fetchone()

    if row:
        print(str(tableName)+ " is already populated.")
        userInput = input("Overwrite? y/n: ")
        while userInput not in {'y', 'n'}:
            print("Invalid input.")
            userInput = input("Overwrite? y/n: ")
        if userInput == 'y':
            print("Clearing "+ str(tableName))
            clearTable(tableName, conn)
            print(str(tableName)+ " cleared")
            response = True
        else:
            response = False

    else:
        response = True
    
    return response
    

def clearTable(tableName, conn):
    cur = conn.cursor()
    sql = 'DELETE FROM ' + tableName
    cur.execute(sql)
    conn.commit()

def populateEPC(conn, schema):
    
    cur = conn.cursor()
    # First get the data into a geojson, then fix the row code (iterate ove att_keys)
    cities = [{'name':'newcastle', 'file':"/epc_abm_newcastle.geojson"},
              {'name':'newcastle', 'file':"/epc_abm_newcastle.geojson"}]

    for city in cities:
        filepath = Config.INITIAL_DATA_LOC + city['file']
        with open(filepath, "r") as file: 
            data = geojson.load(file)

        sql, att_keys =  generate_sql(schema, ) 
        cnt = 0
        for feature in data['features']:
            properties = feature['properties']
            row = [city['name']]
            
            # append features to row
            for att_key in att_keys:
                row.append(properties[att_key])
                
            #append geometry
            geometry = feature['geometry']
            row.append(geometry['type'])
            for i in range(2):
                row.append(geometry['coordinates'][i])
            row = tuple(row)
            cur.execute(sql, row)
            cnt+=1
            print(cnt)
    conn.commit()
        
def populateUPRN(conn):  
    cur = conn.cursor()
    keys = [{'att_key':'UPRN','key':'uprn_chr'},
            {'att_key':'lsoa_code','key':'lsoa_code'},
            {'att_key':'dwelling_bucket','key':'dwelling_bucket'},
            {'att_key':'tenure','key':'tenure'},
            {'att_key':'size_band','key':'size_band'},
            {'att_key':'hidp','key':'hidp'},
            {'att_key':'hh_n_people','key':'hh_n_people'},
            {'att_key':'hh_children','key':'hh_children'},
            {'att_key':'hh_income','key':'hh_income'},
            {'att_key':'hh_income_band','key':'hh_income_band'},
            {'att_key':'schedule_type','key':'schedule_type'},
            {'att_key':'hh_edu_detail','key':'hh_edu_detail'}
    ]
    
    
    # First get the data into a geojson, then fix the row code (iterate ove att_keys)
    filepath = Config.INITIAL_DATA_LOC + '/hidp_uprn_matches_tiered.csv'
    with open(filepath, "r") as file: 
        df = pd.read_csv(file)

    cnt = 0
    for index, entry in df.iterrows():
        msg ='(city,'
        row = ['newcastle']
        qmarks = 'VALUES(?,'

    
        sql = ''' INSERT INTO uprn_data''' +msg +'''VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        
        # append features to row
        for k in keys:
            if entry[k['key']]:
                row.append(entry[k['key']])
                msg += k['att_key'] + ','
                qmarks += '?,'

        msg = msg[:-1] + ')'
        qmarks = qmarks[:-1] + ')'
        sql = ''' INSERT INTO uprn_data''' + msg + qmarks

        row = tuple(row)
        cur.execute(sql, row)
        cnt+=1
        print(cnt)
    conn.commit()

# def populateTemperature(conn, schema):  
#     cur = conn.cursor()
#     filepath = Config.INITIAL_DATA_LOC + '/ncc_2t_timeseries_2010_2039.parquet'
#     msg = '(temp_c,timestamp, geometry_coordinates_lat, geometry_coordinates_lon, flag)'
#     sql = ''' INSERT INTO temperature_time_series''' +msg +'''VALUES(?,?,?,?,?) '''

#     df = pa.read_table(filepath).to_pandas()
#     for row in range(len(df['temp_C'])):
#         vals = [df['temp_C'][row],
#                 str(df['timestamp'][row]),
#                 df['latitude'][row],
#                 df['longitude'][row]]
#         print(vals)
#         vals.append('inbuilt')
#         print(vals)
#         # vals =tuple(vals)
#         cur.execute(sql, vals)

def generate_sql(schema):
    # Generate the correct sql string from the database model
    # In future, this will need to be redone with a dedicated gis database
    try:
        att_keys = []
        msg = '(city,'
        mapper = inspect(schema)
        for attribute in mapper.attrs:
            att_key = str(attribute.key)
            if (not att_key=='id') and not(att_key=='city'):
                msg += att_key + ','
                if not att_key in ['geometry_type', 'geometry_coordinates_lat', 'geometry_coordinates_lon']:
                    att_keys.append(att_key)
            
        
        msg = msg[:-1] + ')'
        sql = ''' INSERT INTO epc_abm_data''' +msg +'''VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        
        return sql, att_keys


    except:
        print("Could not match data to schema. Check that the data columns match the rows in digitalTwin.models.EPCAPMdata")

if __name__ == "__main__":

    with sqlite3.connect('digitalTwin/app.db') as conn:

        # EPC data
        tableName = models.EPCABMdata.__tablename__ 
        response = checkPopulated(tableName,conn)

        if response == True:
            print("Populating " + str(tableName))
            populateEPC(conn, models.EPCABMdata)
            print("Populated successfully :)")
        else:
            print("Failed to populate "+ str(tableName))

        # UPRN data
        tableName = models.UPRNdata.__tablename__
        response = checkPopulated(tableName,conn)

        if response == True:
            print("Populating " + str(tableName))
            populateUPRN(conn)
            print("Populated successfully :)")
        else:
            print("Failed to populate "+ str(tableName))

        #temperature time series
        # tableName = models.TemperatureTimeSeries.__tablename__ 
        # response = checkPopulated(tableName,conn)

        # if response == True:
        #     print("Populating " + str(tableName))
        #     populateTemperature(conn, models.TemperatureTimeSeries)
        #     print("Populated successfully :)")
        # else:
        #     print("Failed to populate "+ str(tableName))



        