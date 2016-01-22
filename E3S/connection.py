# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:58:53 2016

@author: Artur_Herczeg
"""

import requests
import sys

def setLimits(query, start = 0, limit = 10):
    query["start"] = start
    query["limit"] = limit
    return query
    
def getEmptyQuery():
    return {
            "statements":[{"query":"*"}],
            "filters":[],
            "start":0,
            "limit":10
        }
        
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