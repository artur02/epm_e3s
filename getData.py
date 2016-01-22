# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:02:36 2016

@author: Artur_Herczeg
"""

import sys
import requests
from requests.auth import HTTPBasicAuth
import json
import os.path

import pandas as pd

class EmployeeStatus(object):
    EXTENDEDLEAVE = "Extended leave"


def loadConfig(fileName):
    f = open(fileName)
    return json.load(f)

def getEmptyQuery():
    return {
            "statements":[{"query":"*"}],
            "filters":[],
            "start":0,
            "limit":10
        }

def getAuthData():
    config = loadConfig("password.cfg")    
    
    user=config["service"]["user"]
    pas =config["service"]["pass"]
    return (user, pas)

def filterByTitle(query, title):
    if(title is not None):
        if('statements' not in query):
            query["statements"] = []
        titleQuery = title = {
                    "query": "title:\"" + title + "\""
                }
        query["statements"].append(titleQuery)
    return query
    
def filterByCountry(query, country):
    if(country is not None):
        countryFilter = {
                "field":"countrySum.untouchable",
                "values":[country]
            }
        query["filters"].append(countryFilter)
    return query
    
def filterByPrimarySkill(query, skill):
    if(skill is not None):
        skillFilter = {
                "field": "primarySkillSum.untouchable",
                "values":[skill]
            }
        query["filters"].append(skillFilter)
    return query
    
def setLimits(query, start = 0, limit = 10):
    query["start"] = start
    query["limit"] = limit
    return query

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
    
    def saveDataCache(data):
        raw_file = open("rawdata.json", 'w')
        raw_file.truncate()
        raw_file.write(json.dumps(data))
        raw_file.close()
        
    def loadDataCache():
        f = open("rawdata.json")
        return json.load(f)
    
    query = getEmptyQuery()   
    #query = filterByTitle(query, "Software Engineer")
    query = filterByCountry(query, "Hungary")
    query = filterByPrimarySkill(query, ".NET")
    if(limit is not None):
        query = setLimits(query, limit['start'], limit['limit'])
    
    fullQuery = {
            'metaType': 'meta:people-suite:people-api:com.epam.e3s.app.people.api.data.EmployeeEntity',
            'query': json.dumps(query)
        }
    

    if(not os.path.exists("rawdata.json")):
        print("No local data cache (rawdata.json) found, getting data from service...")    
        result = executeQuery(fullQuery, auth)
        saveDataCache(result)
    else:
        print("Local data cache (rawdata.json) found, reading...")
        result = loadDataCache()
        
    print("Total number of employees: %d" % result["total"])
    return getDataFrame(result)
    
def executeQuery(queryParam, auth):
    baseUrl = 'https://telescope.epam.com/rest/e3s-eco-scripting-impl/0.1.0/data/searchFts'
    r = requests.get(baseUrl,  params=queryParam, auth=auth)
    print(r.url)
    
    if r.status_code != 200 or r.headers['content-type'] == "text/html":
        print("request failed")
        print(r.text)
        sys.exit(0)
    else:
        return  r.json()

user, pas = getAuthData()
auth = HTTPBasicAuth(user, pas)


data = getEmployees(auth, { 'start': 0, 'limit': 200 }) 
        

#print(data)
data.to_pickle('dump/data.pickle')
data.to_excel('dump/data.xlsx')


print("================ Non-billables ================ \n")
nonbillables = data[(data.billable == False) & (data.status != EmployeeStatus.EXTENDEDLEAVE)][['name', 'title']]
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

