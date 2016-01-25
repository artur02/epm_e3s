# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:58:53 2016

@author: Artur_Herczeg
"""

import sys
import requests

def set_limits(query, limit):
    start, count = limit
    query["start"] = start
    query["limit"] = count
    return query

def get_empty_query():
    return {
        "statements":[{"query":"*"}],
        "filters":[],
        "start":0,
        "limit":10
    }

def execute_query(query_params, auth):
    url_base = 'https://telescope.epam.com/rest/e3s-eco-scripting-impl/0.1.0/data/searchFts'
    r = requests.get(url_base, params=query_params, auth=auth)
    print(r.url)

    if r.status_code != 200 or r.headers['content-type'] == "text/html":
        print("request failed")
        print(r.text)
        sys.exit(0)
    else:
        return  r.json()
