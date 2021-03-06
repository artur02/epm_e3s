# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:02:36 2016

@author: Artur_Herczeg
"""

import json
import os.path

from requests.auth import HTTPBasicAuth

import matplotlib
matplotlib.style.use('ggplot')

from utilities import load_json_file, create_dir, isFileStale
import E3S.Employees.DSL as dsl
from E3S.Employees.data import EmployeeData
import E3S.connection as e3s

from config import DATA_PATH

def get_auth_data():
    config = load_json_file("password.cfg")

    user = config["service"]["user"]
    pas = config["service"]["pass"]
    return (user, pas)



def get_employees(auth, name, filters):

    def evaluate_filters(query):
        for f in filters:
            query = f(query)
        return query

    def is_cache_available(path):
        file_exists = os.path.exists(raw_data_path)
        if file_exists:
            return not isFileStale(path)
        else:
            return False

    query = e3s.get_empty_query()
    evaluate_filters(query)

    query_full = {
        'metaType': 'meta:people-suite:people-api:com.epam.e3s.app.people.api.data.EmployeeEntity',
        'query': json.dumps(query)
    }

    raw_data_path = os.path.join(DATA_PATH, 'rawdata_%s.json' % name)

    if not is_cache_available(raw_data_path):
        print("No local data cache (%s) found (or outdated), getting data from service..." % raw_data_path)
        result = e3s.execute_query(query_full, auth)
        empdata = EmployeeData(data=result)
        empdata.save_as_json(raw_data_path)
    else:
        print("Local data cache (%s) found, reading..." % raw_data_path)
        result = load_json_file(raw_data_path)
        empdata = EmployeeData(data=result)

    empdata.save_as_sqlite(name)

    print("Total number of employees: %d" % result["total"])
    return empdata.data_frame

def process_java_hungary_employees(auth):
    NAME = 'JavaHungary'

    java_hungary_filters = [
        lambda x: dsl.filter_by_country(x, "Hungary"),
        lambda x: dsl.filter_by_primaryskill(x, "Java"),
        lambda x: e3s.set_limits(x, (0, 1000))
    ]
    data = get_employees(auth, name=NAME, filters=java_hungary_filters)

    return (NAME, data)

def process_dotnet_hungary_employees(auth):
    NAME = 'DotNetHungary'

    dotnet_hungary_filters = [
        lambda x: dsl.filter_by_country(x, "Hungary"),
        lambda x: dsl.filter_by_primaryskill(x, ".NET"),
        lambda x: e3s.set_limits(x, (0, 1000))
    ]
    data = get_employees(auth, name=NAME, filters=dotnet_hungary_filters)

    return (NAME, data)

create_dir(DATA_PATH)

USER, PASSWORD = get_auth_data()
AUTH = HTTPBasicAuth(USER, PASSWORD)
