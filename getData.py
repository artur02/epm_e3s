# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:02:36 2016

@author: Artur_Herczeg
"""

from utilities import loadJsonFile, createDir
import E3S.Employees.DSL as dsl
import E3S.connection as e3s

from requests.auth import HTTPBasicAuth
import json
import os.path
import datetime

import pandas as pd

from sqlalchemy import create_engine

dataFolder = 'data'

def getAuthData():
    config = loadJsonFile("password.cfg")    
    
    user=config["service"]["user"]
    pas =config["service"]["pass"]
    return (user, pas)
    


def getEmployees(auth, limit):
    def getDataFrame(data):
        idx = pd.Series([item['data']['upsaidSum'] for item in data['items']])    
        d = { 
                'name': pd.Series([item['data']['fullNameSum']['full'] for item in data['items']], index=idx),
                'city': pd.Series([item['data']['citySum'] for item in data['items']], index=idx),
                'country': pd.Series([item['data']['countrySum'] for item in data['items']], index=idx),
                'email': pd.Series([item['data']['emailSum'] for item in data['items']], index=idx),
                'manager': pd.Series([item['data']['manager'] for item in data['items']], index=idx),
                'native name': pd.Series([item['data']['nativename'] for item in data['items']], index=idx),
                'primary skill': pd.Series([item['data']['primarySkillSum'] for item in data['items']], index=idx),
                'start work date': pd.Series([item['data']['startworkdate'] for item in data['items']], index=idx),
                'superior': pd.Series([item['data']['superior'] for item in data['items']], index=idx),
                'unit': pd.Series([item['data']['unit'] for item in data['items']], index=idx),
                'upsaid': pd.Series([item['data']['upsaidSum'] for item in data['items']], index=idx),
                'billable': pd.Series([item['data']['billable']>0 for item in data['items']], index=idx),
                'title': pd.Series([item['data']['titleSum'] for item in data['items']], index=idx),
                'orgcategory': pd.Series([item['data'].get('orgcategory') for item in data['items']], index=idx),
                'project': pd.Series([item['data'].get('project') for item in data['items']], index=idx),
                'isRM': pd.Series([item['data'].get('isRm') for item in data['items']], index=idx, dtype=bool),
                'status': pd.Series([item['data'].get('status') for item in data['items']], index=idx),
        }
        
        df = pd.DataFrame(d, index=idx)
        return df
    
    def saveDataCache(path, data):
        raw_file = open(path, 'w')
        raw_file.truncate()
        raw_file.write(json.dumps(data))
        raw_file.close()
    
    query = e3s.getEmptyQuery()   
    #query = dsl.filterByTitle(query, "Software Engineer")
    query = dsl.filterByCountry(query, "Hungary")
    query = dsl.filterByPrimarySkill(query, ".NET")
    if(limit is not None):
        query = e3s.setLimits(query, limit['start'], limit['limit'])
    
    fullQuery = {
            'metaType': 'meta:people-suite:people-api:com.epam.e3s.app.people.api.data.EmployeeEntity',
            'query': json.dumps(query)
        }

    rawDataPath = os.path.join(dataFolder, 'rawdata.json')
    

    if(not os.path.exists(rawDataPath)):
        print("No local data cache (rawdata.json) found, getting data from service...")    
        result = e3s.executeQuery(fullQuery, auth)
        saveDataCache(rawDataPath, result)
    else:
        print("Local data cache (rawdata.json) found, reading...")
        result = loadJsonFile(rawDataPath)
        
    print("Total number of employees: %d" % result["total"])
    return getDataFrame(result)
        
def persistData(data):
    logging = False
    
    engine = create_engine('sqlite:///' + dataFolder + '/e3s.db', echo=logging)
    data.to_sql("employees_"+str(datetime.date.today()), engine, if_exists='replace')

createDir(dataFolder)

user, pas = getAuthData()
auth = HTTPBasicAuth(user, pas)


data = getEmployees(auth, { 'start': 0, 'limit': 200 }) 
persistData(data)



print("================ Non-billables ================ \n")
nonbillables = data[(data.billable == False) & (data.status != dsl.EmployeeStatus.EXTENDEDLEAVE)][['name', 'title']]
print(nonbillables)
print("--- Count: %d" % nonbillables.name.count())
print("\n\n")

print("================ RMs ================ \n")
rms = data[data.isRM == True][['name', 'title']]
print(rms)
print("--- Count: %d" % rms.name.count())
print("\n\n")

print("================ Cities ================ \n")
print(data.city.unique())
print("\n\n")

