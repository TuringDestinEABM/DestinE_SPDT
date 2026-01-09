'''Check app.db exists. Check it contains initial data. if it doesn't, populate it'''

import geojson
import sqlite3

from digitalTwin import db
from digitalTwin.models import models
from digitalTwin.config import Config
from sqlalchemy import inspect


def checkPopulated(tableName, conn):
    cur = conn.cursor()
    cur.execute('SELECT id FROM ' +tableName + ' WHERE id =?', (1,))
    row = cur.fetchone()

    if row:
        print("Table is already populated.")
        userInput = input("Overwrite? y/n")
        while userInput not in {'y', 'n'}:
            print("Invalid input.")
            userInput = input("Overwrite? y/n")
        if userInput == 'y':
            print("Clearing table")
            clearTable(conn)
            print("Table cleared")
            response = True
        else:
            response = False

    else:
        response = True
    
    return response
    

def clearTable(conn):
    cur = conn.cursor()
    sql = 'DELETE FROM temp_table'
    cur.execute(sql)
    conn.commit()

def populate(conn, schema):  
    cur = conn.cursor()
    sql, att_keys = generate_sql(schema)
    
    # First get the data into a geojson, then fix the row code (iterate ove att_keys)

    with open(Config.INITIAL_DATA_LOC, "r") as file: 
        data = geojson.load(file)
    cnt = 0
    for feature in data['features']:
        properties = feature['properties']
        row = []
        
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
        

def generate_sql(schema):
    # Generate the correct sql string from the database model
    # In future, this will need to be redone with a dedicated gis database
    try:
        att_keys = []
        msg = '('
        mapper = inspect(schema)
        for attribute in mapper.attrs:
            att_key = str(attribute.key)
            if not att_key=='id':
                msg += att_key + ','
                if not att_key in ['geometry_type', 'geometry_coordinates_lat', 'geometry_coordinates_lon']:
                    att_keys.append(att_key)
        
        msg = msg[:-1] + ')'
        sql = ''' INSERT INTO epc_abm_data''' +msg +'''VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        
        return sql, att_keys


    except:
        print("Could not match data to schema. Check that the data columns match the rows in digitalTwin.models.EPCAPMdata")

if __name__ == "__main__":
    with sqlite3.connect('digitalTwin/app.db') as conn:
        schema = models.EPCABMdata
        tableName = schema.__tablename__ 
        response = checkPopulated(tableName,conn)

        if response == True:
            print("Populating table")
            populate(conn,schema)
            print("Populated successfully :)")
        else:
            print("Failed to populate")

        