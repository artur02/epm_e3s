# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:02:36 2016

@author: Artur_Herczeg
"""

import json
import os.path

from requests.auth import HTTPBasicAuth

from utilities import loadJsonFile, createDir
import E3S.Employees.DSL as dsl
from E3S.Employees.data import EmployeeData
import E3S.connection as e3s
import E3S.Employees.stats as stats

dataFolder = 'data'

def getAuthData():
    config = loadJsonFile("password.cfg")

    user = config["service"]["user"]
    pas = config["service"]["pass"]
    return (user, pas)



def getEmployees(auth, filters):

    def evaluateFilters(query):
        for f in filters:
            query = f(query)
        return query

    query = e3s.getEmptyQuery()
    evaluateFilters(query)

    fullQuery = {
        'metaType': 'meta:people-suite:people-api:com.epam.e3s.app.people.api.data.EmployeeEntity',
        'query': json.dumps(query)
    }

    rawDataPath = os.path.join(dataFolder, 'rawdata.json')

    if not os.path.exists(rawDataPath):
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

def printStat(df, title, plot=None):
    print("================ %s ================ \n" % title)
    print(df)
    print("--- Count: %d" % len(df))
    if plot is not None:
        df.plot(kind=plot)
    print("\n")

createDir(dataFolder)

user, pas = getAuthData()
auth = HTTPBasicAuth(user, pas)

filters = [
    lambda x: dsl.filterByCountry(x, "Hungary"),
    lambda x: dsl.filterByPrimarySkill(x, "Java"),
    lambda x: e3s.setLimits(x, (0, 1000))
]
data = getEmployees(auth, filters=filters)
empstat = stats.EmployeeStats(data)

printStat(empstat.getNonbillables(), "Non-billables")
printStat(empstat.getRMs(), "RMs")
printStat(empstat.getCities(), "Cities")
printStat(empstat.getTitleCount(), "Titles", plot='barh')

