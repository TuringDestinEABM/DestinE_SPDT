'''Check app.db exists. Check it contains initial data. if it doesn't, populate it'''

import json
import sqlite3

from digitalTwin import db
from digitalTwin.models import models
from digitalTwin.config import Config
from sqlalchemy import inspect


def checkPopulated(conn):
    cur = conn.cursor()
    cur.execute('SELECT id FROM temp_table WHERE id =?', (1,))
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

    with open(Config.INITIAL_DATA_LOC, "r") as jsonfile: 
        data = json.load(jsonfile)

    for key in range(len(data['data_set'])):
        key =str(key)
        row = (data['data_set'][key] ,data['var1'][key],data['var2'][key])
        cur.execute(sql, row)
    conn.commit()

def generate_sql(schema):
    # Generate the correct sql string from the database model
    try:
        att_keys = []
        msg = '('
        mapper = inspect(schema)
        for attribute in mapper.attrs:
            att_key = str(attribute.key)
            if not att_key == 'id':
                att_keys.append(att_key)
                msg += att_key + ','
        
        msg = msg[:-1] + ')'
        sql = ''' INSERT INTO epc_abm_data''' +msg +'''VALUES(?,?,?) '''
        
        return sql, att_keys


    except:
        print("Could not match data to schema. Check that the data columns match the rows in digitalTwin.models.EPCAPMdata")

if __name__ == "__main__":
    with sqlite3.connect('digitalTwin/app.db') as conn:
        schema = models.EPCABMdata
        load_data(schema)
        
        # response = checkPopulated(conn)

        # if response == True:
        #     print("Populating table")
        #     populate(conn)
        #     print("Populated successfully :)")
        # else:
        #     print("Failed to populate")

        # populate(conn)