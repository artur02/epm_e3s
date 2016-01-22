# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:02:36 2016

@author: Artur_Herczeg
"""

from utilities import loadJsonFile, createDir
import E3S.Employees.DSL as dsl
from E3S.Employees.data import EmployeeData
import E3S.connection as e3s
import E3S.Employees.stats as stats

from requests.auth import HTTPBasicAuth
import json
import os.path

dataFolder = 'data'

def getAuthData():
    config = loadJsonFile("password.cfg")    
    
    user=config["service"]["user"]
    pas =config["service"]["pass"]
    return (user, pas)
    


def getEmployees(auth, limit):
    
    
    query = e3s.getEmptyQuery()   
    #query = dsl.filterByTitle(query, "Software Engineer")
    query = dsl.filterByCountry(query, "Hungary")
    query = dsl.filterByPrimarySkill(query, ".NET")
    if(limit is not None):
        start, count = limit
        query = e3s.setLimits(query, start, count)
    
    fullQuery = {
            'metaType': 'meta:people-suite:people-api:com.epam.e3s.app.people.api.data.EmployeeEntity',
            'query': json.dumps(query)
        }

    rawDataPath = os.path.join(dataFolder, 'rawdata.json')
    
    if(not os.path.exists(rawDataPath)):
        print("No local data cache (rawdata.json) found, getting data from service...")    
        result = e3s.executeQuery(fullQuery, auth)
        empdata = EmployeeData(data=result)
        empdata.saveAsJson(rawDataPath)
    else:
        print("Local data cache (rawdata.json) found, reading...")
        result = loadJsonFile(rawDataPath)
        empdata = EmployeeData(data=result)

    empdata.saveAsSQlite()    
    
    print("Total number of employees: %d" % result["total"])
    return empdata.dataFrame
    
def printStat(df, title):
    print("================ %s ================ \n" % title)
    print(df)
    print("--- Count: %d" % len(df))
    print("\n")

createDir(dataFolder)

user, pas = getAuthData()
auth = HTTPBasicAuth(user, pas)


data = getEmployees(auth, (0, 200)) 
empstat = stats.EmployeeStats(data)

printStat(empstat.getNonbillables(), "Non-billables")
printStat(empstat.getRMs(), "RMs")
printStat(empstat.getCities(), "Cities")

#print("================ Non-billables ================ \n")
#nonbillables = empstat.getNonbillables()
#print(nonbillables)
#print("--- Count: %d" % nonbillables.name.count())
#print("\n\n")
#
#print("================ RMs ================ \n")
#rms = empstat.getRMs()
#print(rms)
#print("--- Count: %d" % rms.name.count())
#print("\n\n")
#
#print("================ Cities ================ \n")
#print(empstat.getCities())
#print("\n\n")

