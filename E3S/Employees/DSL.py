# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:52:41 2016

@author: Artur_Herczeg
"""

def filter_by_title(query, title):
    if title is not None:
        if 'statements' not in query:
            query["statements"] = []
        query_title = title = {
            "query": "title:\"" + title + "\""
        }
        query["statements"].append(query_title)
    return query

def filter_by_country(query, country):
    if country is not None:
        filter_qountry = {
            "field":"countrySum.untouchable",
            "values":[country]
        }
        query["filters"].append(filter_qountry)
    return query

def filter_by_primaryskill(query, skill):
    if skill is not None:
        filter_skill = {
            "field": "primarySkillSum.untouchable",
            "values":[skill]
        }
        query["filters"].append(filter_skill)
    return query



EMPLOYEE_STATUS = {
    'EXTENDEDLEAVE' : 'Extended leave',
    'FULLTIME_EMPLOYEE' :'Full-time employee',
    'PARTTIME_EMPLOYEE' :'Part-time employee',
}
