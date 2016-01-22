# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:52:41 2016

@author: Artur_Herczeg
"""

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
    
    
    
class EmployeeStatus(object):
    EXTENDEDLEAVE = "Extended leave"
    FULLTIME_EMPLOYEE = 'Full-time employee'
    PARTTIME_EMPLOYEE = 'Part-time employee'